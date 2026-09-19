import hashlib
from collections.abc import Iterable
from datetime import datetime, timedelta

from app.core.config import RiskThresholds, THRESHOLDS
from app.models.normalized import NormalizedRecord
from app.models.responses import (
    AffectedEntity,
    EntityType,
    Evidence,
    Language,
    Priority,
    Risk,
    ScoreBreakdown,
)
from app.services.localization import field_display, localize_diagnostics, tr

HIGH_EVENT_SEVERITIES = {"high", "critical", "severe", "emergency"}
CRITICAL_EVENT_SEVERITIES = {"critical", "emergency"}
SAFETY_CRITICAL_EVENT_TERMS = {
    "collision",
    "near_miss",
    "near miss",
    "gas_alarm",
    "gas alarm",
    "fire",
    "explosion",
    "restricted_area",
    "restricted area",
    "unauthorized",
    "rollover",
    "rockfall",
    "rock fall",
    "injury",
    "emergency",
}
ABNORMAL_WORKER_STATUSES = {
    "distress",
    "emergency",
    "injured",
    "missing",
    "unauthorized",
}
ABNORMAL_EQUIPMENT_STATUSES = {
    "fault",
    "emergency",
    "maintenance required",
    "maintenance_required",
    "out of service",
    "out_of_service",
    "maintenance",
}
STOPPED_STATUSES = {"stopped", "inactive", "offline", "out of service", "out_of_service"}
INACTIVE_WORKER_STATUSES = {"inactive", "off_shift", "off shift", "offline", "absent"}
INACTIVE_EQUIPMENT_STATUSES = {
    "inactive",
    "offline",
    "out_of_service",
    "out of service",
    "maintenance",
}


def normalized_status(record: NormalizedRecord) -> str:
    value = record.values.get("status")
    return str(value).strip().lower() if value is not None else ""


def normalized_event_severity(value: object) -> str:
    normalized = str(value or "").strip().lower()
    try:
        numeric = float(normalized)
    except ValueError:
        return normalized
    if numeric >= 5:
        return "critical"
    if numeric >= 4:
        return "high"
    return normalized


def record_evidence(record: NormalizedRecord, language: Language) -> Evidence:
    return Evidence(
        evidence_id=record.evidence_id,
        source_file=record.source_file,
        source_row=record.source_row,
        timestamp=record.timestamp,
        zone_id=record.zone_id,
        facts=record.values,
        validation_issues=localize_diagnostics(record.validation_issues, language),
    )


def unique_evidence(
    records: Iterable[NormalizedRecord], language: Language
) -> list[Evidence]:
    by_id = {
        record.evidence_id: record_evidence(record, language) for record in records
    }
    return sorted(
        by_id.values(),
        key=lambda evidence: (evidence.timestamp or datetime.min, evidence.source_file, evidence.source_row),
    )


def stable_risk_id(rule: str, evidence: list[Evidence]) -> str:
    material = f"{rule}|{'|'.join(sorted(item.evidence_id for item in evidence))}"
    return f"risk-{hashlib.sha256(material.encode('utf-8')).hexdigest()[:16]}"


def priority_for(score: int) -> Priority:
    if score >= 85:
        return Priority.CRITICAL
    if score >= 65:
        return Priority.HIGH
    if score >= 40:
        return Priority.MEDIUM
    return Priority.LOW


def immediacy_score(detected_at: datetime, dataset_now: datetime) -> int:
    age_minutes = max(0.0, (dataset_now - detected_at).total_seconds() / 60)
    if age_minutes <= 5:
        return 20
    if age_minutes <= 15:
        return 17
    if age_minutes <= 30:
        return 12
    if age_minutes <= 60:
        return 7
    return 3


def make_risk(
    *,
    rule: str,
    title: str,
    zone_id: str | None,
    detected_at: datetime,
    entities: list[AffectedEntity],
    records: list[NormalizedRecord],
    interpretation: str,
    recommended_action: str,
    limitations: list[str],
    severity: int,
    immediacy: int,
    exposure: int,
    corroboration: int,
    magnitude: int,
    language: Language,
) -> Risk:
    breakdown = ScoreBreakdown(
        severity=min(40, max(0, severity)),
        immediacy=min(20, max(0, immediacy)),
        exposure=min(15, max(0, exposure)),
        corroboration=min(15, max(0, corroboration)),
        magnitude=min(10, max(0, magnitude)),
    )
    score = sum(breakdown.model_dump().values())
    evidence = unique_evidence(records, language)
    priority_reasons = [
        tr(language, "score.severity", score=breakdown.severity),
        tr(language, "score.immediacy", score=breakdown.immediacy),
        tr(language, "score.exposure", score=breakdown.exposure),
        tr(language, "score.corroboration", score=breakdown.corroboration),
        tr(language, "score.magnitude", score=breakdown.magnitude),
    ]
    return Risk(
        risk_id=stable_risk_id(rule, evidence),
        title=title,
        priority=priority_for(score),
        score=score,
        zone_id=zone_id,
        detected_at=detected_at,
        affected_entities=entities,
        observed_data=evidence,
        interpretation=interpretation,
        recommended_action=recommended_action,
        limitations=limitations,
        score_breakdown=breakdown,
        priority_reasons=priority_reasons,
    )


def latest_by_entity(records: list[NormalizedRecord], record_type: str) -> list[NormalizedRecord]:
    latest: dict[str, NormalizedRecord] = {}
    for record in records:
        if record.record_type != record_type or record.entity_id is None:
            continue
        previous = latest.get(record.entity_id)
        if previous is None or (record.timestamp, record.source_row) > (
            previous.timestamp,
            previous.source_row,
        ):
            latest[record.entity_id] = record
    return list(latest.values())


def records_near(
    records: list[NormalizedRecord],
    *,
    zone_id: str | None,
    timestamp: datetime,
    minutes: float,
    types: set[str] | None = None,
) -> list[NormalizedRecord]:
    if zone_id is None:
        return []
    window = timedelta(minutes=minutes)
    return [
        record
        for record in records
        if record.zone_id == zone_id
        and abs(record.timestamp - timestamp) <= window
        and (types is None or record.record_type in types)
    ]


def affected_from_context(records: list[NormalizedRecord]) -> list[AffectedEntity]:
    entities: dict[tuple[EntityType, str], AffectedEntity] = {}
    for record in records:
        if record.entity_id is None:
            continue
        if record.record_type == "workers":
            entity_type = EntityType.WORKER
        elif record.record_type == "equipment":
            entity_type = EntityType.EQUIPMENT
        else:
            continue
        entities[(entity_type, record.entity_id)] = AffectedEntity(type=entity_type, id=record.entity_id)
    return sorted(entities.values(), key=lambda item: (item.type.value, item.id))


def detect_event_risks(
    records: list[NormalizedRecord], dataset_now: datetime, thresholds: RiskThresholds, language: Language
) -> list[Risk]:
    risks: list[Risk] = []
    for event in records:
        if event.record_type != "events":
            continue
        severity_value = normalized_event_severity(event.values.get("severity"))
        event_type = str(event.values.get("event_type") or "").strip()
        description = str(event.values.get("description") or "").strip()
        event_search_text = f"{event_type} {description}".casefold().replace("-", "_")
        safety_critical_type = any(
            term in event_search_text for term in SAFETY_CRITICAL_EVENT_TERMS
        )
        high_severity = severity_value in HIGH_EVENT_SEVERITIES
        if not high_severity and not safety_critical_type:
            continue
        context = records_near(
            records,
            zone_id=event.zone_id,
            timestamp=event.timestamp,
            minutes=thresholds.context_minutes,
            types={"workers", "equipment", "environment"},
        )
        affected = affected_from_context(context)
        source_types = {record.record_type for record in context} | {"events"}
        displayed_event_type = event.values.get("event_type") or "—"
        displayed_severity = severity_value or "—"
        severity_score = (
            40
            if severity_value in CRITICAL_EVENT_SEVERITIES
            else 32
            if high_severity
            else 26
        )
        risks.append(
            make_risk(
                rule="high_severity_event" if high_severity else "safety_critical_event",
                title=tr(
                    language,
                    "risk.event.title"
                    if high_severity
                    else "risk.event.investigation.title",
                ),
                zone_id=event.zone_id,
                detected_at=event.timestamp,
                entities=affected,
                records=[event, *context],
                interpretation=(
                    tr(
                        language,
                        "risk.event.interpretation",
                        event_id=event.entity_id,
                        severity=displayed_severity,
                        event_type=displayed_event_type,
                    )
                    if high_severity
                    else tr(
                        language,
                        "risk.event.investigation.interpretation",
                        event_id=event.entity_id,
                        severity=displayed_severity,
                        event_type=displayed_event_type,
                    )
                ),
                recommended_action=tr(language, "risk.event.action"),
                limitations=[
                    tr(language, "risk.event.limit.cause"),
                    tr(language, "risk.event.limit.context"),
                ],
                severity=severity_score,
                immediacy=immediacy_score(event.timestamp, dataset_now),
                exposure=min(15, len(affected) * 3),
                corroboration=min(15, len(source_types) * 5),
                magnitude=(
                    10
                    if severity_value in CRITICAL_EVENT_SEVERITIES
                    else 7
                    if high_severity
                    else 6
                ),
                language=language,
            )
        )
    return risks


def detect_worker_equipment_conflicts(
    records: list[NormalizedRecord], dataset_now: datetime, thresholds: RiskThresholds, language: Language
) -> list[Risk]:
    cutoff = dataset_now - timedelta(minutes=thresholds.active_window_minutes)
    workers = [
        record
        for record in latest_by_entity(records, "workers")
        if record.timestamp >= cutoff
        and record.zone_id is not None
        and normalized_status(record) not in INACTIVE_WORKER_STATUSES
    ]
    equipment = [
        record
        for record in latest_by_entity(records, "equipment")
        if record.timestamp >= cutoff
        and record.zone_id is not None
        and normalized_status(record) not in INACTIVE_EQUIPMENT_STATUSES
        and isinstance(record.values.get("speed"), (int, float))
        and float(record.values["speed"]) > 0
    ]
    risks: list[Risk] = []
    window = timedelta(minutes=thresholds.co_presence_minutes)
    for worker in workers:
        for machine in equipment:
            if worker.zone_id != machine.zone_id or abs(worker.timestamp - machine.timestamp) > window:
                continue
            detected_at = max(worker.timestamp, machine.timestamp)
            context = records_near(
                records,
                zone_id=worker.zone_id,
                timestamp=detected_at,
                minutes=thresholds.context_minutes,
                types={"environment", "events"},
            )
            source_types = {"workers", "equipment", *(record.record_type for record in context)}
            speed = float(machine.values["speed"])
            risks.append(
                make_risk(
                    rule="worker_equipment_conflict",
                    title=tr(language, "risk.conflict.title"),
                    zone_id=worker.zone_id,
                    detected_at=detected_at,
                    entities=affected_from_context([worker, machine]),
                    records=[worker, machine, *context],
                    interpretation=tr(
                        language,
                        "risk.conflict.interpretation",
                        worker_id=worker.entity_id,
                        equipment_id=machine.entity_id,
                        zone_id=worker.zone_id,
                        minutes=f"{thresholds.co_presence_minutes:g}",
                        speed=machine.values["speed"],
                    ),
                    recommended_action=tr(
                        language,
                        "risk.conflict.action",
                        worker_id=worker.entity_id,
                        equipment_id=machine.entity_id,
                    ),
                    limitations=[
                        tr(language, "risk.conflict.limit.coordinates"),
                        tr(language, "risk.conflict.limit.speed"),
                        tr(language, "risk.conflict.limit.inference"),
                    ],
                    severity=25,
                    immediacy=immediacy_score(detected_at, dataset_now),
                    exposure=10,
                    corroboration=min(15, len(source_types) * 5),
                    magnitude=10 if speed >= 25 else 7 if speed >= 10 else 4,
                    language=language,
                )
            )
    return risks


def environmental_conditions(
    record: NormalizedRecord, thresholds: RiskThresholds
) -> list[tuple[str, float, str, float, bool]]:
    conditions: list[tuple[str, float, str, float, bool]] = []
    gas = record.values.get("gas_level")
    if isinstance(gas, (int, float)) and gas >= thresholds.gas_warning:
        conditions.append(("gas_level", float(gas), ">=", thresholds.gas_warning, gas >= thresholds.gas_critical))
    temperature = record.values.get("temperature")
    if isinstance(temperature, (int, float)) and temperature >= thresholds.temperature_warning:
        conditions.append(
            (
                "temperature",
                float(temperature),
                ">=",
                thresholds.temperature_warning,
                temperature >= thresholds.temperature_critical,
            )
        )
    visibility = record.values.get("visibility")
    if isinstance(visibility, (int, float)) and visibility <= thresholds.visibility_warning:
        conditions.append(
            (
                "visibility",
                float(visibility),
                "<=",
                thresholds.visibility_warning,
                visibility <= thresholds.visibility_critical,
            )
        )
    return conditions


def environmental_trends(
    records: list[NormalizedRecord], language: Language
) -> tuple[list[str], list[NormalizedRecord]]:
    if len(records) < 2:
        return [], []
    ordered = sorted(records, key=lambda record: (record.timestamp, record.source_row))
    first, last = ordered[0], ordered[-1]
    trends: list[str] = []
    for field in ("gas_level", "temperature"):
        first_value = first.values.get(field)
        last_value = last.values.get(field)
        if (
            isinstance(first_value, (int, float))
            and isinstance(last_value, (int, float))
            and last_value > first_value
        ):
            trends.append(
                tr(
                    language,
                    "trend.increased",
                    field=field_display(field, language),
                    first=f"{first_value:g}",
                    last=f"{last_value:g}",
                )
            )
    first_visibility = first.values.get("visibility")
    last_visibility = last.values.get("visibility")
    if (
        isinstance(first_visibility, (int, float))
        and isinstance(last_visibility, (int, float))
        and last_visibility < first_visibility
    ):
        trends.append(
            tr(
                language,
                "trend.decreased",
                field=field_display("visibility", language),
                first=f"{first_visibility:g}",
                last=f"{last_visibility:g}",
            )
        )
    return trends, ordered if trends else []


def detect_environment_risks(
    records: list[NormalizedRecord], dataset_now: datetime, thresholds: RiskThresholds, language: Language
) -> list[Risk]:
    cutoff = dataset_now - timedelta(minutes=thresholds.active_window_minutes)
    records_by_zone: dict[str, list[NormalizedRecord]] = {}
    for record in records:
        if (
            record.record_type != "environment"
            or record.zone_id is None
            or record.timestamp < cutoff
        ):
            continue
        records_by_zone.setdefault(record.zone_id, []).append(record)

    risks: list[Risk] = []
    for zone_id, zone_records in records_by_zone.items():
        environment = max(zone_records, key=lambda record: (record.timestamp, record.source_row))
        conditions = environmental_conditions(environment, thresholds)
        if not conditions:
            continue
        trends, trend_records = environmental_trends(zone_records, language)
        context = records_near(
            records,
            zone_id=zone_id,
            timestamp=environment.timestamp,
            minutes=thresholds.context_minutes,
            types={"workers", "equipment", "events"},
        )
        critical = any(item[4] for item in conditions)
        descriptions = [
            tr(
                language,
                "risk.environment.condition",
                name=field_display(name, language),
                value=f"{value:g}",
                operator=operator,
                threshold=f"{threshold:g}",
            )
            for name, value, operator, threshold, _ in conditions
        ]
        if trends:
            descriptions.append(
                tr(language, "risk.environment.trend", details="; ".join(trends))
            )
        source_types = {"environment", *(record.record_type for record in context)}
        entities = affected_from_context(context)
        risks.append(
            make_risk(
                rule="environment_anomaly",
                title=tr(language, "risk.environment.title"),
                zone_id=zone_id,
                detected_at=environment.timestamp,
                entities=entities,
                records=[environment, *trend_records, *context],
                interpretation=tr(
                    language, "risk.environment.interpretation", details="; ".join(descriptions)
                ),
                recommended_action=tr(language, "risk.environment.action"),
                limitations=[
                    tr(language, "risk.environment.limit.units"),
                    tr(language, "risk.environment.limit.thresholds"),
                    tr(language, "risk.environment.limit.cause"),
                ],
                severity=38 if critical else 30 if len(conditions) >= 2 else 24,
                immediacy=immediacy_score(environment.timestamp, dataset_now),
                exposure=min(15, len(entities) * 3),
                corroboration=min(15, len(source_types) * 5),
                magnitude=10 if critical else 8 if len(conditions) >= 2 else 5,
                language=language,
            )
        )
    return risks


def detect_status_risks(
    records: list[NormalizedRecord], dataset_now: datetime, thresholds: RiskThresholds, language: Language
) -> list[Risk]:
    cutoff = dataset_now - timedelta(minutes=thresholds.active_window_minutes)
    candidates = [
        *latest_by_entity(records, "workers"),
        *latest_by_entity(records, "equipment"),
    ]
    risks: list[Risk] = []
    for record in candidates:
        if record.timestamp < cutoff:
            continue
        status_value = normalized_status(record)
        abnormal_statuses = (
            ABNORMAL_WORKER_STATUSES if record.record_type == "workers" else ABNORMAL_EQUIPMENT_STATUSES
        )
        if status_value not in abnormal_statuses:
            continue
        context = records_near(
            records,
            zone_id=record.zone_id,
            timestamp=record.timestamp,
            minutes=thresholds.context_minutes,
            types={"events", "environment"},
        )
        entity_kind = "worker" if record.record_type == "workers" else "equipment"
        localized_entity_kind = tr(language, f"entity.{entity_kind}")
        urgent = status_value in {"emergency", "injured", "distress", "missing", "fault"}
        risks.append(
            make_risk(
                rule=f"abnormal_{entity_kind}_status",
                title=tr(language, "risk.status.title", entity_kind=localized_entity_kind),
                zone_id=record.zone_id,
                detected_at=record.timestamp,
                entities=affected_from_context([record]),
                records=[record, *context],
                interpretation=tr(
                    language,
                    "risk.status.interpretation",
                    entity_kind=localized_entity_kind,
                    entity_kind_title=tr(language, f"entity.{entity_kind}.title"),
                    entity_id=record.entity_id,
                    status=record.values.get("status"),
                ),
                recommended_action=tr(
                    language,
                    "risk.status.action",
                    entity_id=record.entity_id,
                    entity_kind=localized_entity_kind,
                ),
                limitations=[
                    tr(language, "risk.status.limit")
                ],
                severity=35 if urgent else 20,
                immediacy=immediacy_score(record.timestamp, dataset_now),
                exposure=5,
                corroboration=min(15, 5 + len({item.record_type for item in context}) * 5),
                magnitude=8 if urgent else 3,
                language=language,
            )
        )
    return risks


def detect_telemetry_inconsistencies(
    records: list[NormalizedRecord], dataset_now: datetime, thresholds: RiskThresholds, language: Language
) -> list[Risk]:
    cutoff = dataset_now - timedelta(minutes=thresholds.active_window_minutes)
    risks: list[Risk] = []
    for equipment in latest_by_entity(records, "equipment"):
        speed = equipment.values.get("speed")
        if (
            equipment.timestamp < cutoff
            or normalized_status(equipment) not in STOPPED_STATUSES
            or not isinstance(speed, (int, float))
            or speed <= 0
        ):
            continue
        risks.append(
            make_risk(
                rule="telemetry_inconsistency",
                title=tr(language, "risk.telemetry.title"),
                zone_id=equipment.zone_id,
                detected_at=equipment.timestamp,
                entities=affected_from_context([equipment]),
                records=[equipment],
                interpretation=tr(
                    language,
                    "risk.telemetry.interpretation",
                    entity_id=equipment.entity_id,
                    status=equipment.values.get("status"),
                    speed=speed,
                ),
                recommended_action=tr(language, "risk.telemetry.action"),
                limitations=[
                    tr(language, "risk.telemetry.limit")
                ],
                severity=18,
                immediacy=immediacy_score(equipment.timestamp, dataset_now),
                exposure=5,
                corroboration=5,
                magnitude=5,
                language=language,
            )
        )
    return risks


def detect_compound_zone_risks(
    categorized_risks: dict[str, list[Risk]],
    records: list[NormalizedRecord],
    dataset_now: datetime,
    thresholds: RiskThresholds,
    language: Language,
) -> list[Risk]:
    cutoff = dataset_now - timedelta(minutes=thresholds.active_window_minutes)
    zones = {
        risk.zone_id
        for risks in categorized_risks.values()
        for risk in risks
        if risk.zone_id is not None and risk.detected_at >= cutoff
    }
    record_by_evidence = {record.evidence_id: record for record in records}
    compound: list[Risk] = []
    for zone_id in sorted(zones):
        by_category = {
            category: [
                risk
                for risk in risks
                if risk.zone_id == zone_id and risk.detected_at >= cutoff
            ]
            for category, risks in categorized_risks.items()
        }
        active_categories = {
            category: risks for category, risks in by_category.items() if risks
        }
        if len(active_categories) < 3:
            continue
        supporting_risks = [
            risk for risks in active_categories.values() for risk in risks
        ]
        evidence_ids = {
            evidence.evidence_id
            for risk in supporting_risks
            for evidence in risk.observed_data
        }
        supporting_records = [
            record_by_evidence[evidence_id]
            for evidence_id in sorted(evidence_ids)
            if evidence_id in record_by_evidence
        ]
        entities = {
            (entity.type, entity.id): entity
            for risk in supporting_risks
            for entity in risk.affected_entities
        }
        affected = sorted(
            entities.values(), key=lambda item: (item.type.value, item.id)
        )
        category_titles = "; ".join(
            dict.fromkeys(
                risk.title
                for category in sorted(active_categories)
                for risk in active_categories[category]
            )
        )
        detected_at = max(risk.detected_at for risk in supporting_risks)
        has_critical = any(
            risk.priority == Priority.CRITICAL for risk in supporting_risks
        )
        compound.append(
            make_risk(
                rule="compound_zone_escalation",
                title=tr(language, "risk.compound.title"),
                zone_id=zone_id,
                detected_at=detected_at,
                entities=affected,
                records=supporting_records,
                interpretation=tr(
                    language,
                    "risk.compound.interpretation",
                    zone_id=zone_id,
                    categories=category_titles,
                ),
                recommended_action=tr(
                    language, "risk.compound.action", zone_id=zone_id
                ),
                limitations=[
                    tr(language, "risk.compound.limit.cause"),
                    tr(language, "risk.compound.limit.context"),
                ],
                severity=40 if has_critical else 34,
                immediacy=immediacy_score(detected_at, dataset_now),
                exposure=min(15, len(affected) * 5),
                corroboration=15,
                magnitude=10 if has_critical else 8,
                language=language,
            )
        )
    return compound


def detect_risks(
    records: list[NormalizedRecord], thresholds: RiskThresholds = THRESHOLDS,
    language: Language = Language.EN,
) -> list[Risk]:
    if not records:
        return []
    dataset_now = max(record.timestamp for record in records)
    event_risks = detect_event_risks(records, dataset_now, thresholds, language)
    conflict_risks = detect_worker_equipment_conflicts(
        records, dataset_now, thresholds, language
    )
    environment_risks = detect_environment_risks(
        records, dataset_now, thresholds, language
    )
    status_risks = detect_status_risks(records, dataset_now, thresholds, language)
    telemetry_risks = detect_telemetry_inconsistencies(
        records, dataset_now, thresholds, language
    )
    compound_risks = detect_compound_zone_risks(
        {
            "event": event_risks,
            "conflict": conflict_risks,
            "environment": environment_risks,
            "status": status_risks,
        },
        records,
        dataset_now,
        thresholds,
        language,
    )
    risks = [
        *compound_risks,
        *event_risks,
        *conflict_risks,
        *environment_risks,
        *status_risks,
        *telemetry_risks,
    ]
    unique = {risk.risk_id: risk for risk in risks}
    return sorted(
        unique.values(),
        key=lambda risk: (-risk.score, -risk.detected_at.timestamp(), risk.risk_id),
    )
