import json
import os
import re
from collections import defaultdict
from datetime import datetime, timedelta
from enum import StrEnum

from pydantic import BaseModel, ConfigDict

from app.models.normalized import NormalizedRecord
from app.models.responses import GroundedFact, QuestionAnswer, Risk
from app.store.memory import StoredAnalysis


class QuestionIntent(StrEnum):
    TOP_RISK = "top_risk"
    ZONE_RISK = "zone_risk"
    AFFECTED_ENTITIES = "affected_entities"
    RISK_EVIDENCE = "risk_evidence"
    RECENT_CHANGES = "recent_changes"
    GENERAL_OVERVIEW = "general_overview"
    INSUFFICIENT = "insufficient"


class QuestionRoute(BaseModel):
    model_config = ConfigDict(extra="forbid")

    intent: QuestionIntent
    zone_id: str | None = None
    entity_id: str | None = None
    risk_id: str | None = None
    minutes: int = 30


def available_zones(analysis: StoredAnalysis) -> list[str]:
    return sorted({record.zone_id for record in analysis.records if record.zone_id})


def available_entities(analysis: StoredAnalysis) -> list[str]:
    return sorted({record.entity_id for record in analysis.records if record.entity_id})


def extract_known_value(question: str, values: list[str]) -> str | None:
    lowered = question.casefold()
    return next((value for value in values if value.casefold() in lowered), None)


def deterministic_route(question: str, analysis: StoredAnalysis) -> QuestionRoute:
    lowered = question.casefold()
    zones = available_zones(analysis)
    entities = available_entities(analysis)
    risk_ids = [risk.risk_id for risk in analysis.response.risks]
    zone_id = extract_known_value(question, zones)
    entity_id = extract_known_value(question, entities)
    risk_id = extract_known_value(question, risk_ids)

    minutes_match = re.search(r"(?:last|past|最近)\s*(\d{1,3})\s*(?:minutes?|mins?|分钟)", lowered)
    minutes = min(240, max(1, int(minutes_match.group(1)))) if minutes_match else 30
    unknown_zone_requested = bool(re.search(r"\bzone\s+[a-z0-9_-]+", lowered)) and zone_id is None
    requested_entity = re.search(
        r"\b(?:worker|equipment|truck|vehicle)\s+([a-z0-9_-]+)|\b[a-z]{1,4}-\d+\b",
        lowered,
    )
    unknown_entity_requested = requested_entity is not None and entity_id is None

    if unknown_zone_requested or unknown_entity_requested:
        intent = QuestionIntent.INSUFFICIENT
    elif any(term in lowered for term in ("changed", "change", "last ", "past ", "变化", "最近")):
        intent = QuestionIntent.RECENT_CHANGES
    elif any(term in lowered for term in ("evidence", "support", "alert", "证据", "依据")):
        intent = QuestionIntent.RISK_EVIDENCE
    elif any(term in lowered for term in ("affected", "which workers", "which vehicles", "哪些人员", "哪些设备", "影响")):
        intent = QuestionIntent.AFFECTED_ENTITIES
    elif zone_id and any(term in lowered for term in ("why", "danger", "risk", "危险", "风险")):
        intent = QuestionIntent.ZONE_RISK
    elif any(term in lowered for term in ("immediate", "first", "highest", "top", "priority", "最紧急", "优先")):
        intent = QuestionIntent.TOP_RISK
    elif any(term in lowered for term in ("overview", "situation", "summary", "概况", "情况")):
        intent = QuestionIntent.GENERAL_OVERVIEW
    elif zone_id:
        intent = QuestionIntent.ZONE_RISK
    elif entity_id or risk_id:
        intent = QuestionIntent.RISK_EVIDENCE
    else:
        intent = QuestionIntent.GENERAL_OVERVIEW

    return QuestionRoute(
        intent=intent,
        zone_id=zone_id,
        entity_id=entity_id,
        risk_id=risk_id,
        minutes=minutes,
    )


def route_with_openai(question: str, analysis: StoredAnalysis) -> QuestionRoute | None:
    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("AI_API_KEY")
    model = os.getenv("AI_MODEL")
    if not api_key or not model:
        return None
    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key, timeout=8.0, max_retries=0)
        response = client.responses.parse(
            model=model,
            input=[
                {
                    "role": "system",
                    "content": (
                        "Classify a mine-shift supervisor question. Select only from the provided "
                        "zones, entities, and risk IDs. Do not invent identifiers. Use 30 minutes "
                        "when no time window is stated. Return only the structured route."
                    ),
                },
                {
                    "role": "user",
                    "content": json.dumps(
                        {
                            "question": question,
                            "available_zones": available_zones(analysis),
                            "available_entities": available_entities(analysis),
                            "available_risk_ids": [
                                risk.risk_id for risk in analysis.response.risks
                            ],
                        }
                    ),
                },
            ],
            text_format=QuestionRoute,
        )
        route = response.output_parsed
        if route is None:
            return None
        if route.zone_id and route.zone_id not in available_zones(analysis):
            return None
        if route.entity_id and route.entity_id not in available_entities(analysis):
            return None
        risk_ids = {risk.risk_id for risk in analysis.response.risks}
        if route.risk_id and route.risk_id not in risk_ids:
            return None
        route.minutes = min(240, max(1, route.minutes))
        return route
    except Exception:
        return None


def matching_risks(route: QuestionRoute, risks: list[Risk]) -> list[Risk]:
    selected = risks
    if route.risk_id:
        selected = [risk for risk in selected if risk.risk_id == route.risk_id]
    if route.zone_id:
        selected = [risk for risk in selected if risk.zone_id == route.zone_id]
    if route.entity_id:
        selected = [
            risk
            for risk in selected
            if any(entity.id == route.entity_id for entity in risk.affected_entities)
        ]
    return selected


def evidence_statement(record: NormalizedRecord) -> str:
    details = []
    for key, value in record.values.items():
        if value is not None and key not in {"worker_id", "equipment_id", "event_id", "zone_id"}:
            details.append(f"{key}={value}")
    subject = record.entity_id or record.record_type.rstrip("s")
    zone = f" in {record.zone_id}" if record.zone_id else ""
    suffix = f"; {', '.join(details)}" if details else ""
    return f"{subject} was recorded at {record.timestamp.isoformat()}{zone}{suffix}."


def facts_from_risks(risks: list[Risk], limit: int = 12) -> list[GroundedFact]:
    facts: list[GroundedFact] = []
    seen: set[str] = set()
    for risk in risks:
        for evidence in risk.observed_data:
            if evidence.evidence_id in seen:
                continue
            seen.add(evidence.evidence_id)
            details = [
                f"{key}={value}"
                for key, value in evidence.facts.items()
                if value is not None and key != "zone_id"
            ]
            zone = f" in {evidence.zone_id}" if evidence.zone_id else ""
            suffix = f"; {', '.join(details)}" if details else ""
            facts.append(
                GroundedFact(
                    statement=(
                        f"Record at {evidence.timestamp.isoformat() if evidence.timestamp else 'unknown time'}"
                        f"{zone}{suffix}."
                    ),
                    evidence_ids=[evidence.evidence_id],
                )
            )
            if len(facts) >= limit:
                return facts
    return facts


def insufficient_answer(question: str, message: str, limitation: str) -> QuestionAnswer:
    return QuestionAnswer(
        question=question,
        answer=message,
        answer_mode="deterministic_fallback",
        observed_facts=[],
        interpretation=None,
        recommended_action=None,
        limitations=[limitation],
    )


def answer_top_risk(question: str, risks: list[Risk], mode: str) -> QuestionAnswer:
    if not risks:
        return insufficient_answer(
            question,
            "No risks were detected in the valid uploaded records.",
            "No detected risks does not prove that the shift is safe; unavailable or rejected data may limit coverage.",
        )
    risk = risks[0]
    return QuestionAnswer(
        question=question,
        answer=(
            f"Investigate {risk.title} in {risk.zone_id or 'an unspecified zone'} first. "
            f"It is {risk.priority.value} priority with score {risk.score}. {risk.interpretation}"
        ),
        answer_mode=mode,
        observed_facts=facts_from_risks([risk]),
        interpretation=risk.interpretation,
        recommended_action=risk.recommended_action,
        limitations=risk.limitations,
    )


def answer_zone(question: str, route: QuestionRoute, risks: list[Risk], mode: str) -> QuestionAnswer:
    if route.zone_id is None:
        return insufficient_answer(
            question,
            "I could not identify a zone from the question.",
            "Ask using a zone identifier present in the uploaded records.",
        )
    if not risks:
        return insufficient_answer(
            question,
            f"No detected risk is associated with {route.zone_id} in the available records.",
            "This does not prove the zone is safe; data may be missing or outside the analysis window.",
        )
    top = risks[0]
    titles = ", ".join(f"{risk.title} ({risk.priority.value})" for risk in risks[:4])
    return QuestionAnswer(
        question=question,
        answer=(
            f"{route.zone_id} has {len(risks)} detected risk(s): {titles}. "
            f"The highest is {top.title} with score {top.score}."
        ),
        answer_mode=mode,
        observed_facts=facts_from_risks(risks),
        interpretation=top.interpretation,
        recommended_action=top.recommended_action,
        limitations=list(dict.fromkeys(item for risk in risks for item in risk.limitations)),
    )


def answer_affected(question: str, risks: list[Risk], mode: str) -> QuestionAnswer:
    if not risks:
        return insufficient_answer(
            question,
            "No affected workers or equipment can be identified from the selected scope.",
            "The available records do not support an affected-entity conclusion.",
        )
    entities = sorted(
        {(entity.type.value, entity.id) for risk in risks for entity in risk.affected_entities}
    )
    if not entities:
        return insufficient_answer(
            question,
            "The selected risks do not identify affected workers or equipment.",
            "An event or environmental risk may have no entity record within the context window.",
        )
    entity_text = ", ".join(f"{entity_type} {entity_id}" for entity_type, entity_id in entities)
    return QuestionAnswer(
        question=question,
        answer=f"The selected risk context identifies: {entity_text}.",
        answer_mode=mode,
        observed_facts=facts_from_risks(risks),
        interpretation="Entities are listed only when they occur in the selected risk evidence context.",
        recommended_action=risks[0].recommended_action,
        limitations=[
            "Zone-level co-presence does not establish precise distance or direct involvement."
        ],
    )


def answer_evidence(question: str, risks: list[Risk], mode: str) -> QuestionAnswer:
    if not risks:
        return insufficient_answer(
            question,
            "No matching alert was found, so supporting evidence cannot be shown.",
            "Specify a valid risk ID, zone, or affected entity from this analysis.",
        )
    risk = risks[0]
    facts = facts_from_risks([risk])
    return QuestionAnswer(
        question=question,
        answer=f"{len(facts)} source record(s) support {risk.title}. Each fact includes its evidence ID.",
        answer_mode=mode,
        observed_facts=facts,
        interpretation=risk.interpretation,
        recommended_action=risk.recommended_action,
        limitations=risk.limitations,
    )


def change_facts(
    records: tuple[NormalizedRecord, ...], minutes: int, zone_id: str | None = None
) -> list[GroundedFact]:
    if not records:
        return []
    dataset_now = max(record.timestamp for record in records)
    cutoff = dataset_now - timedelta(minutes=minutes)
    facts: list[GroundedFact] = []

    for event in sorted(
        (
            record
            for record in records
            if record.record_type == "events"
            and record.timestamp >= cutoff
            and (zone_id is None or record.zone_id == zone_id)
        ),
        key=lambda item: item.timestamp,
    ):
        facts.append(GroundedFact(statement=evidence_statement(event), evidence_ids=[event.evidence_id]))

    grouped_entities: dict[tuple[str, str], list[NormalizedRecord]] = defaultdict(list)
    for record in records:
        if record.entity_id and record.record_type in {"workers", "equipment"}:
            grouped_entities[(record.record_type, record.entity_id)].append(record)
    for (_, entity_id), entity_records in grouped_entities.items():
        ordered = sorted(entity_records, key=lambda item: (item.timestamp, item.source_row))
        for index, current in enumerate(ordered):
            if current.timestamp < cutoff or index == 0:
                continue
            previous = ordered[index - 1]
            if zone_id is not None and zone_id not in {previous.zone_id, current.zone_id}:
                continue
            changes = []
            if previous.zone_id != current.zone_id:
                changes.append(f"zone {previous.zone_id} -> {current.zone_id}")
            previous_status = previous.values.get("status")
            current_status = current.values.get("status")
            if previous_status != current_status:
                changes.append(f"status {previous_status} -> {current_status}")
            if current.record_type == "equipment" and previous.values.get("speed") != current.values.get("speed"):
                changes.append(
                    f"speed {previous.values.get('speed')} -> {current.values.get('speed')}"
                )
            if changes:
                facts.append(
                    GroundedFact(
                        statement=(
                            f"{entity_id} changed at {current.timestamp.isoformat()}: "
                            f"{'; '.join(changes)}."
                        ),
                        evidence_ids=[previous.evidence_id, current.evidence_id],
                    )
                )

    by_zone: dict[str, list[NormalizedRecord]] = defaultdict(list)
    for record in records:
        if (
            record.record_type == "environment"
            and record.zone_id
            and record.timestamp >= cutoff
            and (zone_id is None or record.zone_id == zone_id)
        ):
            by_zone[record.zone_id].append(record)
    for zone_id, environment_records in by_zone.items():
        ordered = sorted(environment_records, key=lambda item: item.timestamp)
        if len(ordered) < 2:
            continue
        first, last = ordered[0], ordered[-1]
        changes = []
        for field in ("gas_level", "temperature", "visibility"):
            if first.values.get(field) != last.values.get(field):
                changes.append(f"{field} {first.values.get(field)} -> {last.values.get(field)}")
        if changes:
            facts.append(
                GroundedFact(
                    statement=(
                        f"{zone_id} environmental readings changed between "
                        f"{first.timestamp.isoformat()} and {last.timestamp.isoformat()}: "
                        f"{'; '.join(changes)}."
                    ),
                    evidence_ids=[first.evidence_id, last.evidence_id],
                )
            )
    return facts[:15]


def answer_changes(
    question: str, analysis: StoredAnalysis, route: QuestionRoute, mode: str
) -> QuestionAnswer:
    facts = change_facts(analysis.records, route.minutes, route.zone_id)
    if not facts:
        return insufficient_answer(
            question,
            f"No supported changes were found during the last {route.minutes} minutes of dataset time.",
            "A change requires comparable records; a single observation cannot establish a trend.",
        )
    return QuestionAnswer(
        question=question,
        answer=(
            f"{len(facts)} supported change(s) were found"
            f"{f' in {route.zone_id}' if route.zone_id else ''} during the last "
            f"{route.minutes} minutes of dataset time."
        ),
        answer_mode=mode,
        observed_facts=facts,
        interpretation="Changes are comparisons of timestamped uploaded records, not inferred causes.",
        recommended_action="Review the cited changes alongside the prioritized risk list.",
        limitations=[
            "Only recorded observations are compared; unrecorded intermediate changes are unknown."
        ],
    )


def answer_overview(question: str, analysis: StoredAnalysis, mode: str) -> QuestionAnswer:
    risks = analysis.response.risks
    overview = analysis.response.overview
    if not risks:
        return answer_top_risk(question, risks, mode)
    top = risks[0]
    return QuestionAnswer(
        question=question,
        answer=(
            f"The shift has {overview.active_workers} active worker(s), "
            f"{overview.active_equipment} active equipment item(s), {overview.shift_events} "
            f"event(s), and {len(risks)} detected risk(s). The first priority is {top.title} "
            f"in {top.zone_id or 'an unspecified zone'} with score {top.score}."
        ),
        answer_mode=mode,
        observed_facts=facts_from_risks([top]),
        interpretation=top.interpretation,
        recommended_action=top.recommended_action,
        limitations=top.limitations,
    )


def answer_question(
    question: str,
    analysis: StoredAnalysis,
    *,
    risk_id: str | None = None,
    zone_id: str | None = None,
    entity_id: str | None = None,
) -> QuestionAnswer:
    ai_route = route_with_openai(question, analysis)
    route = ai_route or deterministic_route(question, analysis)
    mode = "llm_routed" if ai_route else "deterministic_fallback"

    valid_risk_ids = {risk.risk_id for risk in analysis.response.risks}
    if risk_id is not None and risk_id not in valid_risk_ids:
        return insufficient_answer(
            question,
            "The requested risk was not found in this analysis.",
            "The system does not use risk identifiers from another analysis.",
        )
    if zone_id is not None and zone_id not in available_zones(analysis):
        return insufficient_answer(
            question,
            "The requested zone was not found in the uploaded data.",
            "The system does not infer zone identifiers that are absent from the dataset.",
        )
    if entity_id is not None and entity_id not in available_entities(analysis):
        return insufficient_answer(
            question,
            "The requested entity was not found in the uploaded data.",
            "The system does not infer entity identifiers that are absent from the dataset.",
        )
    route.risk_id = risk_id or route.risk_id
    route.zone_id = zone_id or route.zone_id
    route.entity_id = entity_id or route.entity_id
    risks = matching_risks(route, analysis.response.risks)

    if route.intent == QuestionIntent.TOP_RISK:
        return answer_top_risk(question, risks, mode)
    if route.intent == QuestionIntent.ZONE_RISK:
        return answer_zone(question, route, risks, mode)
    if route.intent == QuestionIntent.AFFECTED_ENTITIES:
        return answer_affected(question, risks, mode)
    if route.intent == QuestionIntent.RISK_EVIDENCE:
        return answer_evidence(question, risks, mode)
    if route.intent == QuestionIntent.RECENT_CHANGES:
        return answer_changes(question, analysis, route, mode)
    if route.intent == QuestionIntent.INSUFFICIENT:
        return insufficient_answer(
            question,
            "The requested zone, entity, or risk was not found in the uploaded data.",
            "The system does not infer identifiers that are absent from the dataset.",
        )
    return answer_overview(question, analysis, mode)
