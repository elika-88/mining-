from datetime import datetime, timezone

from app.models.responses import (
    AnalysisMetadata,
    AnalysisResponse,
    Overview,
    ProcessingSummary,
)
from app.store.memory import AnalysisStore


def response(analysis_id: str) -> AnalysisResponse:
    return AnalysisResponse(
        analysis_id=analysis_id,
        overview=Overview(
            analysis_id=analysis_id,
            status="completed",
            shift_started_at=None,
            shift_ended_at=None,
            active_workers=0,
            active_equipment=0,
            shift_events=0,
            high_priority_risks=0,
            processing_summary=ProcessingSummary(
                received_records=0,
                valid_records=0,
                rejected_records=0,
                warnings=[],
            ),
        ),
        risks=[],
        metadata=AnalysisMetadata(
            engine_version="test",
            analyzed_at=datetime.now(timezone.utc),
            source_of_truth="uploaded_csv",
            data_fingerprint="0" * 64,
            thresholds={},
        ),
    )


def test_store_evicts_oldest_analysis() -> None:
    store = AnalysisStore(max_analyses=2)
    store.save(response("analysis-1"), [])
    store.save(response("analysis-2"), [])
    store.save(response("analysis-3"), [])

    assert store.get("analysis-1") is None
    assert store.get("analysis-2") is not None
    assert store.get("analysis-3") is not None
