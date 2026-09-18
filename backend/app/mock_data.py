from datetime import datetime

from app.models.responses import (
    AffectedEntity,
    AnalysisResponse,
    EntityType,
    Evidence,
    GroundedFact,
    Overview,
    Priority,
    ProcessingSummary,
    QuestionAnswer,
    Risk,
    ScoreBreakdown,
)

ANALYSIS_ID = "demo-analysis-001"

WORKER_EVIDENCE = Evidence(
    evidence_id="ev-worker-001",
    source_file="workers.csv",
    source_row=28,
    timestamp=datetime.fromisoformat("2026-09-19T15:21:00"),
    zone_id="Zone B",
    facts={"worker_id": "W-17", "zone_id": "Zone B", "status": "active"},
)

TRUCK_EVIDENCE = Evidence(
    evidence_id="ev-equipment-001",
    source_file="equipment.csv",
    source_row=14,
    timestamp=datetime.fromisoformat("2026-09-19T15:24:00"),
    zone_id="Zone B",
    facts={
        "equipment_id": "T-04",
        "equipment_type": "truck",
        "zone_id": "Zone B",
        "speed": 27.0,
    },
)

DEMO_RISK = Risk(
    risk_id="risk-001",
    title="Potential worker–vehicle conflict",
    priority=Priority.HIGH,
    score=82,
    zone_id="Zone B",
    detected_at=datetime.fromisoformat("2026-09-19T15:24:00"),
    affected_entities=[
        AffectedEntity(type=EntityType.WORKER, id="W-17"),
        AffectedEntity(type=EntityType.EQUIPMENT, id="T-04"),
    ],
    observed_data=[WORKER_EVIDENCE, TRUCK_EVIDENCE],
    interpretation=(
        "A worker and moving equipment were recorded in the same zone within "
        "three minutes. This indicates a potential conflict requiring verification."
    ),
    recommended_action=(
        "Verify the current positions of W-17 and T-04 and contact the Zone B coordinator."
    ),
    limitations=[
        "Precise coordinates are unavailable.",
        "Physical distance between the worker and equipment cannot be determined.",
    ],
    score_breakdown=ScoreBreakdown(
        severity=30,
        immediacy=18,
        exposure=12,
        corroboration=15,
        magnitude=7,
    ),
)

DEMO_OVERVIEW = Overview(
    analysis_id=ANALYSIS_ID,
    status="completed",
    shift_started_at=datetime.fromisoformat("2026-09-19T07:00:00"),
    shift_ended_at=datetime.fromisoformat("2026-09-19T15:30:00"),
    active_workers=42,
    active_equipment=18,
    shift_events=6,
    high_priority_risks=1,
    processing_summary=ProcessingSummary(
        received_records=1000,
        valid_records=974,
        rejected_records=26,
        warnings=["26 malformed records were isolated and excluded from analysis."],
    ),
)

DEMO_ANALYSIS = AnalysisResponse(
    analysis_id=ANALYSIS_ID,
    overview=DEMO_OVERVIEW,
    risks=[DEMO_RISK],
)


def build_demo_answer(question: str) -> QuestionAnswer:
    return QuestionAnswer(
        question=question,
        answer=(
            "Zone B requires attention because W-17 and moving truck T-04 were "
            "recorded there within three minutes."
        ),
        answer_mode="deterministic_mock",
        observed_facts=[
            GroundedFact(
                statement="W-17 was recorded in Zone B at 15:21.",
                evidence_ids=[WORKER_EVIDENCE.evidence_id],
            ),
            GroundedFact(
                statement="T-04 was recorded in Zone B at 15:24 with speed 27.",
                evidence_ids=[TRUCK_EVIDENCE.evidence_id],
            ),
        ],
        interpretation=DEMO_RISK.interpretation,
        recommended_action=DEMO_RISK.recommended_action,
        limitations=DEMO_RISK.limitations,
    )

