from datetime import timedelta
from uuid import uuid4

from app.core.config import THRESHOLDS
from app.models.normalized import NormalizedRecord
from app.models.responses import AnalysisResponse, Overview, Priority, ProcessingSummary
from app.services.ingestion import IngestionResult
from app.services.risk_engine import detect_risks

INACTIVE_WORKER_STATUSES = {"inactive", "off_shift", "off shift", "offline", "absent"}
INACTIVE_EQUIPMENT_STATUSES = {
    "inactive",
    "offline",
    "out_of_service",
    "out of service",
    "maintenance",
}


def latest_entity_records(records: list[NormalizedRecord], record_type: str) -> dict[str, NormalizedRecord]:
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
    return latest


def is_active(record: NormalizedRecord, inactive_statuses: set[str]) -> bool:
    status = record.values.get("status")
    if status is None:
        return True
    return str(status).strip().lower() not in inactive_statuses


def build_analysis(ingestion: IngestionResult) -> tuple[AnalysisResponse, list[NormalizedRecord]]:
    analysis_id = f"analysis-{uuid4().hex[:12]}"
    timestamps = [record.timestamp for record in ingestion.records]
    latest_workers = latest_entity_records(ingestion.records, "workers")
    latest_equipment = latest_entity_records(ingestion.records, "equipment")
    dataset_now = max(timestamps) if timestamps else None
    active_window = timedelta(minutes=THRESHOLDS.active_window_minutes)
    active_workers = sum(
        is_active(record, INACTIVE_WORKER_STATUSES)
        and dataset_now is not None
        and record.timestamp >= dataset_now - active_window
        for record in latest_workers.values()
    )
    active_equipment = sum(
        is_active(record, INACTIVE_EQUIPMENT_STATUSES)
        and dataset_now is not None
        and record.timestamp >= dataset_now - active_window
        for record in latest_equipment.values()
    )
    event_count = sum(record.record_type == "events" for record in ingestion.records)
    risks = detect_risks(ingestion.records)
    summary = ProcessingSummary(
        received_records=ingestion.received_records,
        valid_records=len(ingestion.records),
        rejected_records=ingestion.rejected_records,
        warnings=ingestion.warnings,
    )
    overview = Overview(
        analysis_id=analysis_id,
        status="completed_with_warnings" if ingestion.warnings else "completed",
        shift_started_at=min(timestamps) if timestamps else None,
        shift_ended_at=dataset_now,
        active_workers=active_workers,
        active_equipment=active_equipment,
        shift_events=event_count,
        high_priority_risks=sum(
            risk.priority in {Priority.HIGH, Priority.CRITICAL} for risk in risks
        ),
        processing_summary=summary,
        files=ingestion.files,
    )
    return AnalysisResponse(analysis_id=analysis_id, overview=overview, risks=risks), ingestion.records
