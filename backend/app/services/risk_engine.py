import hashlib
from collections.abc import Iterable
from datetime import datetime, timedelta

from app.core.config import RiskThresholds, THRESHOLDS
from app.models.normalized import NormalizedRecord
from app.models.responses import (
    AffectedEntity,
    EntityType,
    Evidence,
    Priority,
    Risk,
    ScoreBreakdown,
)

HIGH_EVENT_SEVERITIES = {"high", "critical", "severe", "emergency"}
CRITICAL_EVENT_SEVERITIES = {"critical", "emergency"}
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


def record_evidence(record: NormalizedRecord) -> Evidence:
    return Evidence(
        evidence_id=record.evidence_id,
        source_file=record.source_file,
        source_row=record.source_row,
        timestamp=record.timestamp,
        zone_id=record.zone_id,
        facts=record.values,
        validation_issues=record.validation_issues,
    )


def unique_evidence(records: Iterable[NormalizedRecord]) -> list[Evidence]:
    by_id = {record.evidence_id: record_evidence(record) for record in records}
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
) -> Risk:
    breakdown = ScoreBreakdown(
        severity=min(40, max(0, severity)),
        immediacy=min(20, max(0, immediacy)),
        exposure=min(15, max(0, exposure)),
        corroboration=min(15, max(0, corroboration)),
        magnitude=min(10, max(0, magnitude)),
    )
    score = sum(breakdown.model_dump().values())
    evidence = unique_evidence(records)
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
    records: list[NormalizedRecord], dataset_now: datetime, thresholds: RiskThresholds
) -> list[Risk]:
    risks: list[Risk] = []
    for event in records:
        if event.record_type != "events":
            continue
        severity_value = normalized_event_severity(event.values.get("severity"))
        if severity_value not in HIGH_EVENT_SEVERITIES:
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
        event_type = event.values.get("event_type") or "unspecified event"
        severity_score = 40 if severity_value in CRITICAL_EVENT_SEVERITIES else 32
        risks.append(
            make_risk(
                rule="high_severity_event",
                title="High-severity recorded event",
                zone_id=event.zone_id,
                detected_at=event.timestamp,
                entities=affected,
                records=[event, *context],
                interpretation=(
                    f"Event {event.entity_id} is recorded as {severity_value} with type "
                    f"{event_type}. Nearby records are included as context, not proof of causation."
                ),
                recommended_action=(
                    "Verify the recorded event, contact the responsible zone supervisor, and follow "
                    "the site's escalation procedure."
                ),
                limitations=[
                    "The event record does not prove its root cause.",
                    "Nearby entities are time-and-zone context only; precise distance is unavailable.",
                ],
                severity=severity_score,
                immediacy=immediacy_score(event.timestamp, dataset_now),
                exposure=min(15, len(affected) * 3),
                corroboration=min(15, len(source_types) * 5),
                magnitude=10 if severity_value in CRITICAL_EVENT_SEVERITIES else 7,
            )
        )
    return risks


def detect_worker_equipment_conflicts(
    records: list[NormalizedRecord], dataset_now: datetime, thresholds: RiskThresholds
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
                    title="Potential worker–vehicle conflict",
                    zone_id=worker.zone_id,
                    detected_at=detected_at,
                    entities=affected_from_context([worker, machine]),
                    records=[worker, machine, *context],
                    interpretation=(
                        f"Worker {worker.entity_id} and moving equipment {machine.entity_id} were "
                        f"recorded in {worker.zone_id} within {thresholds.co_presence_minutes:g} minutes. "
                        f"The recorded equipment speed value is {machine.values['speed']}."
                    ),
                    recommended_action=(
                        f"Verify the current positions of {worker.entity_id} and {machine.entity_id}, "
                        "contact the zone coordinator, and apply the site's traffic-control procedure."
                    ),
                    limitations=[
                        "The dataset contains zones but no precise coordinates or physical distance.",
                        "The speed unit and site speed limit are not provided.",
                        "Co-presence indicates potential conflict, not a confirmed near miss.",
                    ],
                    severity=25,
                    immediacy=immediacy_score(detected_at, dataset_now),
                    exposure=10,
                    corroboration=min(15, len(source_types) * 5),
                    magnitude=10 if speed >= 25 else 7 if speed >= 10 else 4,
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


def environmental_trends(records: list[NormalizedRecord]) -> tuple[list[str], list[NormalizedRecord]]:
    if len(records) < 2:
        return [], []
    ordered = sorted(records, key=lambda record: (record.timestamp, record.source_row))
    first, last = ordered[0], ordered[-1]
    trends: list[str] = []
    for field, direction in (("gas_level", "increased"), ("temperature", "increased")):
        first_value = first.values.get(field)
        last_value = last.values.get(field)
        if (
            isinstance(first_value, (int, float))
            and isinstance(last_value, (int, float))
            and last_value > first_value
        ):
            trends.append(f"{field} {direction} from {first_value:g} to {last_value:g}")
    first_visibility = first.values.get("visibility")
    last_visibility = last.values.get("visibility")
    if (
        isinstance(first_visibility, (int, float))
        and isinstance(last_visibility, (int, float))
        and last_visibility < first_visibility
    ):
        trends.append(f"visibility decreased from {first_visibility:g} to {last_visibility:g}")
    return trends, ordered if trends else []


def detect_environment_risks(
    records: list[NormalizedRecord], dataset_now: datetime, thresholds: RiskThresholds
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
        trends, trend_records = environmental_trends(zone_records)
        context = records_near(
            records,
            zone_id=zone_id,
            timestamp=environment.timestamp,
            minutes=thresholds.context_minutes,
            types={"workers", "equipment", "events"},
        )
        critical = any(item[4] for item in conditions)
        descriptions = [
            f"{name} {value:g} {operator} configured warning threshold {threshold:g}"
            for name, value, operator, threshold, _ in conditions
        ]
        if trends:
            descriptions.append("recorded trend: " + "; ".join(trends))
        source_types = {"environment", *(record.record_type for record in context)}
        entities = affected_from_context(context)
        risks.append(
            make_risk(
                rule="environment_anomaly",
                title="Adverse environmental conditions",
                zone_id=zone_id,
                detected_at=environment.timestamp,
                entities=entities,
                records=[environment, *trend_records, *context],
                interpretation="; ".join(descriptions) + ".",
                recommended_action=(
                    "Verify the environmental sensor readings, restrict exposure if required by "
                    "site procedure, and notify the zone safety lead."
                ),
                limitations=[
                    "The dataset does not provide sensor units or official site thresholds.",
                    "Thresholds are configurable prototype policy values, not regulatory limits.",
                    "A sensor reading alone does not establish the root cause.",
                ],
                severity=38 if critical else 30 if len(conditions) >= 2 else 24,
                immediacy=immediacy_score(environment.timestamp, dataset_now),
                exposure=min(15, len(entities) * 3),
                corroboration=min(15, len(source_types) * 5),
                magnitude=10 if critical else 8 if len(conditions) >= 2 else 5,
            )
        )
    return risks


def detect_status_risks(
    records: list[NormalizedRecord], dataset_now: datetime, thresholds: RiskThresholds
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
        urgent = status_value in {"emergency", "injured", "distress", "missing", "fault"}
        risks.append(
            make_risk(
                rule=f"abnormal_{entity_kind}_status",
                title=f"Abnormal {entity_kind} status",
                zone_id=record.zone_id,
                detected_at=record.timestamp,
                entities=affected_from_context([record]),
                records=[record, *context],
                interpretation=(
                    f"{entity_kind.capitalize()} {record.entity_id} has recorded status "
                    f"'{record.values.get('status')}'."
                ),
                recommended_action=(
                    f"Verify {record.entity_id}'s current condition and follow the site's "
                    f"{entity_kind} response procedure."
                ),
                limitations=[
                    "The status label is observed data; its cause is not available in the dataset."
                ],
                severity=35 if urgent else 20,
                immediacy=immediacy_score(record.timestamp, dataset_now),
                exposure=5,
                corroboration=min(15, 5 + len({item.record_type for item in context}) * 5),
                magnitude=8 if urgent else 3,
            )
        )
    return risks


def detect_telemetry_inconsistencies(
    records: list[NormalizedRecord], dataset_now: datetime, thresholds: RiskThresholds
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
                title="Equipment telemetry inconsistency",
                zone_id=equipment.zone_id,
                detected_at=equipment.timestamp,
                entities=affected_from_context([equipment]),
                records=[equipment],
                interpretation=(
                    f"Equipment {equipment.entity_id} is recorded with status "
                    f"'{equipment.values.get('status')}' and speed value {speed}."
                ),
                recommended_action=(
                    "Verify equipment state and telemetry integrity before using this record for "
                    "operational decisions."
                ),
                limitations=[
                    "The record may indicate a telemetry issue or a status timing mismatch; the cause is unknown."
                ],
                severity=18,
                immediacy=immediacy_score(equipment.timestamp, dataset_now),
                exposure=5,
                corroboration=5,
                magnitude=5,
            )
        )
    return risks


def detect_risks(
    records: list[NormalizedRecord], thresholds: RiskThresholds = THRESHOLDS
) -> list[Risk]:
    if not records:
        return []
    dataset_now = max(record.timestamp for record in records)
    risks = [
        *detect_event_risks(records, dataset_now, thresholds),
        *detect_worker_equipment_conflicts(records, dataset_now, thresholds),
        *detect_environment_risks(records, dataset_now, thresholds),
        *detect_status_risks(records, dataset_now, thresholds),
        *detect_telemetry_inconsistencies(records, dataset_now, thresholds),
    ]
    unique = {risk.risk_id: risk for risk in risks}
    return sorted(
        unique.values(),
        key=lambda risk: (-risk.score, -risk.detected_at.timestamp(), risk.risk_id),
    )
