from io import BytesIO
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)
SAMPLE_ROOT = Path(__file__).parents[2] / "sample_data" / "mock_shift"


def upload_sample_shift() -> dict:
    files = {
        field: (
            f"{field}.csv",
            BytesIO((SAMPLE_ROOT / f"{field}.csv").read_bytes()),
            "text/csv",
        )
        for field in ("workers", "equipment", "environment", "events")
    }
    response = client.post("/api/analyses", files=files)
    assert response.status_code == 201
    return response.json()


def test_sample_shift_detects_and_prioritizes_expected_risks() -> None:
    payload = upload_sample_shift()
    risks = payload["risks"]
    assert len(risks) == 6
    assert payload["overview"]["high_priority_risks"] == 5
    assert [risk["score"] for risk in risks] == sorted(
        (risk["score"] for risk in risks), reverse=True
    )
    assert risks[0]["title"] == "Compound zone risk escalation"
    assert risks[0]["priority"] == "CRITICAL"
    assert risks[0]["score"] == 95
    assert all(
        entity["type"] in {"worker", "equipment"}
        for risk in risks
        for entity in risk["affected_entities"]
    )
    assert any(risk["title"] == "Potential worker–vehicle conflict" for risk in risks)
    assert any(risk["title"] == "Adverse environmental conditions" for risk in risks)
    assert any(risk["title"] == "Abnormal equipment status" for risk in risks)
    assert any(risk["title"] == "High-severity recorded event" for risk in risks)


def test_every_risk_is_explainable_and_score_is_auditable() -> None:
    risks = upload_sample_shift()["risks"]
    for risk in risks:
        assert risk["observed_data"]
        assert risk["interpretation"]
        assert risk["recommended_action"]
        assert risk["limitations"]
        assert risk["score"] == sum(risk["score_breakdown"].values())
        assert len(risk["priority_reasons"]) == 5
        assert len({item["evidence_id"] for item in risk["observed_data"]}) == len(
            risk["observed_data"]
        )
        assert all(item["source_file"].endswith(".csv") for item in risk["observed_data"])
        assert all(item["source_row"] >= 2 for item in risk["observed_data"])


def test_environment_risk_explains_worsening_recorded_trend() -> None:
    risks = upload_sample_shift()["risks"]
    environment_risk = next(
        risk for risk in risks if risk["title"] == "Adverse environmental conditions"
    )
    assert "recorded trend" in environment_risk["interpretation"]
    assert "gas_level (gas level) increased from 4.2 to 12.8" in environment_risk["interpretation"]
    environment_rows = [
        evidence
        for evidence in environment_risk["observed_data"]
        if evidence["source_file"] == "environment.csv"
    ]
    assert len(environment_rows) == 3


def test_risk_detail_and_evidence_are_retrievable() -> None:
    payload = upload_sample_shift()
    analysis_id = payload["analysis_id"]
    expected_risk = payload["risks"][0]
    risk_response = client.get(
        f"/api/analyses/{analysis_id}/risks/{expected_risk['risk_id']}"
    )
    assert risk_response.status_code == 200
    assert risk_response.json() == expected_risk

    expected_evidence = expected_risk["observed_data"][0]
    evidence_response = client.get(
        f"/api/analyses/{analysis_id}/evidence/{expected_evidence['evidence_id']}"
    )
    assert evidence_response.status_code == 200
    assert evidence_response.json() == expected_evidence


def test_risk_filters_support_operational_workflow() -> None:
    payload = upload_sample_shift()
    analysis_id = payload["analysis_id"]
    critical = client.get(
        f"/api/analyses/{analysis_id}/risks", params={"priority": "CRITICAL"}
    )
    zone_b = client.get(
        f"/api/analyses/{analysis_id}/risks", params={"zone_id": "Zone B"}
    )
    worker = client.get(
        f"/api/analyses/{analysis_id}/risks", params={"entity_id": "W-001"}
    )
    assert critical.status_code == 200
    assert len(critical.json()) == 2
    assert all(risk["priority"] == "CRITICAL" for risk in critical.json())
    assert len(zone_b.json()) == 5
    assert all(risk["zone_id"] == "Zone B" for risk in zone_b.json())
    assert len(worker.json()) == 5


def test_risk_ids_are_stable_for_identical_source_data() -> None:
    first = upload_sample_shift()
    second = upload_sample_shift()
    assert [risk["risk_id"] for risk in first["risks"]] == [
        risk["risk_id"] for risk in second["risks"]
    ]


def test_no_worker_vehicle_conflict_without_temporal_proximity() -> None:
    response = client.post(
        "/api/analyses",
        files={
            "workers": (
                "workers.csv",
                BytesIO(
                    b"worker_id,timestamp,zone_id,status\n"
                    b"W-1,2026-09-19T15:00:00,Zone A,active\n"
                ),
                "text/csv",
            ),
            "equipment": (
                "equipment.csv",
                BytesIO(
                    b"equipment_id,equipment_type,timestamp,zone_id,status,speed\n"
                    b"T-1,truck,2026-09-19T15:20:00,Zone A,active,30\n"
                ),
                "text/csv",
            ),
        },
    )
    assert response.status_code == 201
    assert not any(
        risk["title"] == "Potential worker–vehicle conflict"
        for risk in response.json()["risks"]
    )


def test_invalid_speed_does_not_create_worker_vehicle_conflict() -> None:
    response = client.post(
        "/api/analyses",
        files={
            "workers": (
                "workers.csv",
                BytesIO(
                    b"worker_id,timestamp,zone_id,status\n"
                    b"W-1,2026-09-19T15:20:00,Zone A,active\n"
                ),
                "text/csv",
            ),
            "equipment": (
                "equipment.csv",
                BytesIO(
                    b"equipment_id,equipment_type,timestamp,zone_id,status,speed\n"
                    b"T-1,truck,2026-09-19T15:21:00,Zone A,active,unknown\n"
                ),
                "text/csv",
            ),
        },
    )
    assert response.status_code == 201
    assert response.json()["risks"] == []


def test_stopped_equipment_with_positive_speed_creates_data_quality_risk() -> None:
    response = client.post(
        "/api/analyses",
        files={
            "equipment": (
                "equipment.csv",
                BytesIO(
                    b"equipment_id,equipment_type,timestamp,zone_id,status,speed\n"
                    b"T-1,truck,2026-09-19T15:21:00,Zone A,stopped,12\n"
                ),
                "text/csv",
            )
        },
    )
    assert response.status_code == 201
    risks = response.json()["risks"]
    assert len(risks) == 1
    assert risks[0]["title"] == "Equipment telemetry inconsistency"
    assert "cause is unknown" in risks[0]["limitations"][0]


def test_numeric_event_severity_is_supported() -> None:
    response = client.post(
        "/api/analyses",
        files={
            "events": (
                "events.csv",
                BytesIO(
                    b"event_id,timestamp,zone_id,event_type,severity,description\n"
                    b"E-1,2026-09-19T15:21:00,Zone A,alarm,5,Recorded alarm\n"
                ),
                "text/csv",
            )
        },
    )
    assert response.status_code == 201
    risk = response.json()["risks"][0]
    assert risk["title"] == "High-severity recorded event"
    assert "recorded as critical" in risk["interpretation"]


def test_safety_critical_event_type_is_detected_without_high_severity() -> None:
    response = client.post(
        "/api/analyses",
        files={
            "events": (
                "events.csv",
                BytesIO(
                    b"event_id,timestamp,zone_id,event_type,severity,description\n"
                    b"E-1,2026-09-19T15:21:00,Zone A,restricted_area_entry,medium,Entry recorded\n"
                ),
                "text/csv",
            )
        },
    )
    assert response.status_code == 201
    risk = response.json()["risks"][0]
    assert risk["title"] == "Recorded safety event requiring investigation"
    assert "restricted_area_entry" in risk["interpretation"]


def test_thresholds_are_visible_to_the_frontend() -> None:
    response = client.get("/api/config/risk-thresholds")
    assert response.status_code == 200
    payload = response.json()
    assert payload["gas_warning"] == 10
    assert payload["co_presence_minutes"] == 5
