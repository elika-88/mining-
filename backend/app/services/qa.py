import json
import os
import re
from collections import defaultdict
from datetime import datetime, timedelta
from enum import StrEnum

from pydantic import BaseModel, ConfigDict

from app.models.normalized import NormalizedRecord
from app.models.responses import GroundedFact, Language, QuestionAnswer, Risk
from app.services.localization import field_display, qtr, tr
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


def display_timestamp(timestamp: datetime) -> str:
    if timestamp.year == 2000 and timestamp.month == 1 and timestamp.day == 1:
        return timestamp.strftime("%H:%M:%S")
    return timestamp.isoformat()


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

    minutes_match = re.search(
        r"(?:last|past|最近|последние|соңғы)\s*(\d{1,3})\s*"
        r"(?:minutes?|mins?|分钟|минут(?:ы|у)?|минут)",
        lowered,
    )
    minutes = min(240, max(1, int(minutes_match.group(1)))) if minutes_match else 30
    unknown_zone_requested = bool(re.search(r"\bzone\s+[a-z0-9_-]+", lowered)) and zone_id is None
    requested_entity = re.search(
        r"\b(?:worker|equipment|truck|vehicle)\s+([a-z0-9_-]+)|\b[a-z]{1,4}-\d+\b",
        lowered,
    )
    unknown_entity_requested = requested_entity is not None and entity_id is None

    if unknown_zone_requested or unknown_entity_requested:
        intent = QuestionIntent.INSUFFICIENT
    elif any(term in lowered for term in ("changed", "change", "last ", "past ", "变化", "最近", "измен", "последн", "өзгер", "соңғы")):
        intent = QuestionIntent.RECENT_CHANGES
    elif any(term in lowered for term in ("evidence", "support", "alert", "证据", "依据", "доказат", "подтверж", "дәлел", "раста")):
        intent = QuestionIntent.RISK_EVIDENCE
    elif any(term in lowered for term in ("affected", "which workers", "which vehicles", "哪些人员", "哪些设备", "影响", "затронут", "какие работник", "әсер ет", "қандай жұмысшы")):
        intent = QuestionIntent.AFFECTED_ENTITIES
    elif zone_id and any(term in lowered for term in ("why", "danger", "risk", "危险", "风险", "почему", "опас", "риск", "неге", "қауіп")):
        intent = QuestionIntent.ZONE_RISK
    elif any(term in lowered for term in ("immediate", "first", "highest", "top", "priority", "最紧急", "优先", "立即", "немедлен", "перв", "приорит", "дереу", "бірінші", "басым")):
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
    base_url = os.getenv("AI_BASE_URL")
    if not api_key or not model:
        return None
    try:
        from openai import OpenAI

        client_options = {
            "api_key": api_key,
            "timeout": 8.0,
            "max_retries": 0,
        }
        if base_url:
            client_options["base_url"] = base_url.rstrip("/")
        client = OpenAI(**client_options)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Classify a mine-shift supervisor question. Select only from the provided "
                        "zones, entities, and risk IDs. Do not invent identifiers. Use 30 minutes "
                        "when no time window is stated. Return only one JSON object with keys "
                        "intent, zone_id, entity_id, risk_id, and minutes. Valid intents are "
                        f"{', '.join(intent.value for intent in QuestionIntent)}."
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
        )
        content = response.choices[0].message.content
        if not content:
            return None
        json_start = content.find("{")
        json_end = content.rfind("}")
        if json_start < 0 or json_end < json_start:
            return None
        route = QuestionRoute.model_validate_json(content[json_start : json_end + 1])
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


def evidence_statement(record: NormalizedRecord, language: Language) -> str:
    details = []
    for key, value in record.values.items():
        if value is not None and key not in {"worker_id", "equipment_id", "event_id", "zone_id"}:
            details.append(f"{field_display(key, language)}={value}")
    subject = record.entity_id or record.record_type.rstrip("s")
    zone = qtr(language, "zone_suffix", zone=record.zone_id) if record.zone_id else ""
    return qtr(
        language,
        "record",
        timestamp=display_timestamp(record.timestamp),
        zone=zone,
        details=f"{subject}; {', '.join(details)}" if details else subject,
    )


def facts_from_risks(
    risks: list[Risk], language: Language, limit: int = 12
) -> list[GroundedFact]:
    facts: list[GroundedFact] = []
    seen: set[str] = set()
    for risk in risks:
        for evidence in risk.observed_data:
            if evidence.evidence_id in seen:
                continue
            seen.add(evidence.evidence_id)
            details = [
                f"{field_display(key, language)}={value}"
                for key, value in evidence.facts.items()
                if value is not None and key != "zone_id"
            ]
            zone = qtr(language, "zone_suffix", zone=evidence.zone_id) if evidence.zone_id else ""
            facts.append(
                GroundedFact(
                    statement=qtr(
                        language,
                        "record",
                        timestamp=display_timestamp(evidence.timestamp) if evidence.timestamp else "—",
                        zone=zone,
                        details=", ".join(details) if details else "—",
                    ),
                    evidence_ids=[evidence.evidence_id],
                )
            )
            if len(facts) >= limit:
                return facts
    return facts


def insufficient_answer(
    question: str, message: str, limitation: str, language: Language
) -> QuestionAnswer:
    return QuestionAnswer(
        question=question,
        language=language,
        answer=message,
        answer_mode="deterministic_fallback",
        fallback_reason="insufficient_grounded_data",
        observed_facts=[],
        interpretation=None,
        recommended_action=None,
        limitations=[limitation],
    )


def answer_top_risk(
    question: str, risks: list[Risk], mode: str, language: Language
) -> QuestionAnswer:
    if not risks:
        return insufficient_answer(
            question,
            qtr(language, "no_risks"),
            qtr(language, "no_risks_limit"),
            language,
        )
    risk = risks[0]
    return QuestionAnswer(
        question=question,
        language=language,
        answer=qtr(
            language,
            "top",
            title=risk.title,
            zone=risk.zone_id or qtr(language, "unspecified_zone"),
            priority=tr(language, f"priority.{risk.priority.value.lower()}"),
            score=risk.score,
            interpretation=risk.interpretation,
        ),
        answer_mode=mode,
        observed_facts=facts_from_risks([risk], language),
        interpretation=risk.interpretation,
        recommended_action=risk.recommended_action,
        limitations=risk.limitations,
    )


def answer_zone(
    question: str, route: QuestionRoute, risks: list[Risk], mode: str, language: Language
) -> QuestionAnswer:
    if route.zone_id is None:
        return insufficient_answer(
            question,
            qtr(language, "zone_missing"),
            qtr(language, "zone_missing_limit"),
            language,
        )
    if not risks:
        return insufficient_answer(
            question,
            qtr(language, "zone_none", zone=route.zone_id),
            qtr(language, "zone_none_limit"),
            language,
        )
    top = risks[0]
    titles = ", ".join(
        f"{risk.title} ({tr(language, f'priority.{risk.priority.value.lower()}')})"
        for risk in risks[:4]
    )
    return QuestionAnswer(
        question=question,
        language=language,
        answer=qtr(
            language,
            "zone_answer",
            zone=route.zone_id,
            count=len(risks),
            titles=titles,
            top=top.title,
            score=top.score,
        ),
        answer_mode=mode,
        observed_facts=facts_from_risks(risks, language),
        interpretation=top.interpretation,
        recommended_action=top.recommended_action,
        limitations=list(dict.fromkeys(item for risk in risks for item in risk.limitations)),
    )


def answer_affected(
    question: str, risks: list[Risk], mode: str, language: Language
) -> QuestionAnswer:
    if not risks:
        return insufficient_answer(
            question,
            qtr(language, "affected_none"),
            qtr(language, "affected_none_limit"),
            language,
        )
    entities = sorted(
        {(entity.type.value, entity.id) for risk in risks for entity in risk.affected_entities}
    )
    if not entities:
        return insufficient_answer(
            question,
            qtr(language, "affected_empty"),
            qtr(language, "affected_empty_limit"),
            language,
        )
    entity_text = ", ".join(
        f"{tr(language, f'entity.{entity_type}')} {entity_id}"
        for entity_type, entity_id in entities
    )
    return QuestionAnswer(
        question=question,
        language=language,
        answer=qtr(language, "affected_answer", entities=entity_text),
        answer_mode=mode,
        observed_facts=facts_from_risks(risks, language),
        interpretation=qtr(language, "affected_interpretation"),
        recommended_action=risks[0].recommended_action,
        limitations=[qtr(language, "affected_limit")],
    )


def answer_evidence(
    question: str, risks: list[Risk], mode: str, language: Language
) -> QuestionAnswer:
    if not risks:
        return insufficient_answer(
            question,
            qtr(language, "evidence_none"),
            qtr(language, "evidence_none_limit"),
            language,
        )
    risk = risks[0]
    facts = facts_from_risks([risk], language)
    return QuestionAnswer(
        question=question,
        language=language,
        answer=qtr(language, "evidence_answer", count=len(facts), title=risk.title),
        answer_mode=mode,
        observed_facts=facts,
        interpretation=risk.interpretation,
        recommended_action=risk.recommended_action,
        limitations=risk.limitations,
    )


def change_facts(
    records: tuple[NormalizedRecord, ...],
    minutes: int,
    language: Language,
    zone_id: str | None = None,
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
        facts.append(
            GroundedFact(
                statement=evidence_statement(event, language),
                evidence_ids=[event.evidence_id],
            )
        )

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
                changes.append(
                    qtr(
                        language,
                        "change_zone",
                        first=previous.zone_id,
                        last=current.zone_id,
                    )
                )
            previous_status = previous.values.get("status")
            current_status = current.values.get("status")
            if previous_status != current_status:
                changes.append(
                    qtr(
                        language,
                        "change_status",
                        first=previous_status,
                        last=current_status,
                    )
                )
            if current.record_type == "equipment" and previous.values.get("speed") != current.values.get("speed"):
                changes.append(
                    qtr(
                        language,
                        "change_speed",
                        first=previous.values.get("speed"),
                        last=current.values.get("speed"),
                    )
                )
            if changes:
                facts.append(
                    GroundedFact(
                        statement=qtr(
                            language,
                            "change_entity",
                            entity_id=entity_id,
                            timestamp=display_timestamp(current.timestamp),
                            changes="; ".join(changes),
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
                changes.append(
                    f"{field_display(field, language)} "
                    f"{first.values.get(field)} -> {last.values.get(field)}"
                )
        if changes:
            facts.append(
                GroundedFact(
                    statement=qtr(
                        language,
                        "change_environment",
                        zone=zone_id,
                        first=display_timestamp(first.timestamp),
                        last=display_timestamp(last.timestamp),
                        changes="; ".join(changes),
                    ),
                    evidence_ids=[first.evidence_id, last.evidence_id],
                )
            )
    return facts[:15]


def answer_changes(
    question: str,
    analysis: StoredAnalysis,
    route: QuestionRoute,
    mode: str,
    language: Language,
) -> QuestionAnswer:
    facts = change_facts(analysis.records, route.minutes, language, route.zone_id)
    if not facts:
        return insufficient_answer(
            question,
            qtr(language, "changes_none", minutes=route.minutes),
            qtr(language, "changes_none_limit"),
            language,
        )
    return QuestionAnswer(
        question=question,
        language=language,
        answer=qtr(
            language,
            "changes_answer",
            count=len(facts),
            zone_suffix=qtr(language, "zone_suffix", zone=route.zone_id)
            if route.zone_id
            else "",
            minutes=route.minutes,
        ),
        answer_mode=mode,
        observed_facts=facts,
        interpretation=qtr(language, "changes_interpretation"),
        recommended_action=qtr(language, "changes_action"),
        limitations=[qtr(language, "changes_limit")],
    )


def answer_overview(
    question: str, analysis: StoredAnalysis, mode: str, language: Language
) -> QuestionAnswer:
    risks = analysis.response.risks
    overview = analysis.response.overview
    if not risks:
        return answer_top_risk(question, risks, mode, language)
    top = risks[0]
    return QuestionAnswer(
        question=question,
        language=language,
        answer=qtr(
            language,
            "overview",
            workers=overview.active_workers,
            equipment=overview.active_equipment,
            events=overview.shift_events,
            risks=len(risks),
            title=top.title,
            zone=top.zone_id or qtr(language, "unspecified_zone"),
            score=top.score,
        ),
        answer_mode=mode,
        observed_facts=facts_from_risks([top], language),
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
    language: Language = Language.EN,
) -> QuestionAnswer:
    ai_route = route_with_openai(question, analysis)
    route = ai_route or deterministic_route(question, analysis)
    mode = "llm_routed" if ai_route else "deterministic_fallback"
    model_used = os.getenv("AI_MODEL") if ai_route else None
    ai_configured = bool(
        (os.getenv("OPENAI_API_KEY") or os.getenv("AI_API_KEY")) and os.getenv("AI_MODEL")
    )
    fallback_reason = None if ai_route else (
        "ai_route_unavailable" if ai_configured else "ai_not_configured"
    )

    valid_risk_ids = {risk.risk_id for risk in analysis.response.risks}
    if risk_id is not None and risk_id not in valid_risk_ids:
        return insufficient_answer(
            question,
            qtr(language, "unknown_risk"),
            qtr(language, "unknown_risk_limit"),
            language,
        )
    if zone_id is not None and zone_id not in available_zones(analysis):
        return insufficient_answer(
            question,
            qtr(language, "unknown_zone"),
            qtr(language, "unknown_zone_limit"),
            language,
        )
    if entity_id is not None and entity_id not in available_entities(analysis):
        return insufficient_answer(
            question,
            qtr(language, "unknown_entity"),
            qtr(language, "unknown_entity_limit"),
            language,
        )
    route.risk_id = risk_id or route.risk_id
    route.zone_id = zone_id or route.zone_id
    route.entity_id = entity_id or route.entity_id
    lowered_question = question.casefold()
    if risk_id and any(
        term in lowered_question
        for term in ("evidence", "support", "alert", "证据", "依据", "доказат", "подтверж", "дәлел")
    ):
        route.intent = QuestionIntent.RISK_EVIDENCE
    elif zone_id and any(
        term in lowered_question
        for term in ("why", "danger", "risk", "危险", "风险", "почему", "опас", "неге", "қауіп")
    ):
        route.intent = QuestionIntent.ZONE_RISK
    elif entity_id and any(
        term in lowered_question
        for term in ("affected", "worker", "vehicle", "equipment", "人员", "车辆", "设备", "затронут", "работник", "әсер", "жұмысшы")
    ):
        route.intent = QuestionIntent.AFFECTED_ENTITIES
    risks = matching_risks(route, analysis.response.risks)

    if route.intent == QuestionIntent.TOP_RISK:
        answer = answer_top_risk(question, risks, mode, language)
    elif route.intent == QuestionIntent.ZONE_RISK:
        answer = answer_zone(question, route, risks, mode, language)
    elif route.intent == QuestionIntent.AFFECTED_ENTITIES:
        answer = answer_affected(question, risks, mode, language)
    elif route.intent == QuestionIntent.RISK_EVIDENCE:
        answer = answer_evidence(question, risks, mode, language)
    elif route.intent == QuestionIntent.RECENT_CHANGES:
        answer = answer_changes(question, analysis, route, mode, language)
    elif route.intent == QuestionIntent.INSUFFICIENT:
        answer = insufficient_answer(
            question,
            qtr(language, "unknown_scope"),
            qtr(language, "unknown_scope_limit"),
            language,
        )
    else:
        answer = answer_overview(question, analysis, mode, language)
    answer.model_used = model_used
    if answer.answer_mode == "deterministic_fallback" and answer.fallback_reason is None:
        answer.fallback_reason = fallback_reason
    return answer
