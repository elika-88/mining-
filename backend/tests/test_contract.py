from io import BytesIO

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def csv_upload(name: str, content: str) -> tuple[str, BytesIO, str]:
    return name, BytesIO(content.encode("utf-8")), "text/csv"


def create_valid_analysis() -> dict:
    response = client.post(
        "/api/analyses",
        files={
            "workers": csv_upload(
                "workers.csv",
                "worker_id,timestamp,zone_id,status\n"
                "W-1,2026-09-19T08:00:00,Zone A,active\n"
                "W-2,2026-09-19T08:05:00,Zone B,off_shift\n",
            ),
            "equipment": csv_upload(
                "equipment.csv",
                "equipment_id,equipment_type,timestamp,zone_id,status,speed\n"
                "T-1,truck,2026-09-19T08:10:00,Zone A,active,12.5\n",
            ),
            "environment": csv_upload(
                "environment.csv",
                "timestamp,zone_id,gas_level,temperature,visibility\n"
                "2026-09-19T08:15:00,Zone A,4.2,22,80\n",
            ),
            "events": csv_upload(
                "events.csv",
                "event_id,timestamp,zone_id,event_type,severity,description\n"
                "E-1,2026-09-19T08:20:00,Zone A,inspection,low,Routine check\n",
            ),
        },
    )
    assert response.status_code == 201
    return response.json()


def test_health() -> None:
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "version": "0.5.0"}


def test_requires_at_least_one_file() -> None:
    response = client.post("/api/analyses")
    assert response.status_code == 422
    assert response.json()["detail"] == "At least one CSV file must be provided."


def test_frontend_local_origins_are_allowed_by_cors() -> None:
    for origin in ("http://localhost:5173", "http://127.0.0.1:5173"):
        response = client.options(
            "/api/analyses",
            headers={
                "Origin": origin,
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "content-type",
            },
        )
        assert response.status_code == 200
        assert response.headers["access-control-allow-origin"] == origin


def test_valid_files_create_real_overview() -> None:
    payload = create_valid_analysis()
    overview = payload["overview"]
    assert payload["analysis_id"].startswith("analysis-")
    assert payload["risks"] == []
    assert overview["active_workers"] == 1
    assert overview["active_equipment"] == 1
    assert overview["shift_events"] == 1
    assert overview["shift_started_at"] == "2026-09-19T08:00:00"
    assert overview["shift_ended_at"] == "2026-09-19T08:20:00"
    assert overview["processing_summary"]["valid_records"] == 5
    assert overview["processing_summary"]["rejected_records"] == 0


def test_analysis_can_be_retrieved() -> None:
    created = create_valid_analysis()
    response = client.get(f"/api/analyses/{created['analysis_id']}/overview")
    assert response.status_code == 200
    assert response.json() == created["overview"]


def test_invalid_rows_are_isolated_without_crashing() -> None:
    response = client.post(
        "/api/analyses",
        files={
            "workers": csv_upload(
                "workers.csv",
                "worker_id,timestamp,zone_id,status\n"
                "W-1,not-a-time,Zone A,active\n"
                ",2026-09-19T08:01:00,Zone A,active\n"
                "W-2,2026-09-19T08:02:00,Zone B,active\n",
            )
        },
    )
    assert response.status_code == 201
    summary = response.json()["overview"]["processing_summary"]
    assert summary["received_records"] == 3
    assert summary["valid_records"] == 1
    assert summary["rejected_records"] == 2
    assert any("invalid timestamp" in warning for warning in summary["warnings"])


@pytest.mark.parametrize(
    "timestamp",
    [
        "2026/09/19 08:02:00",
        "2026.09.19 08:02",
        "19-09-2026 08:02:00",
        "09/19/2026 08:02 AM",
        "2026年09月19日 08:02",
        "2026-09-19 08:02:00 UTC",
        "08:02",
        "08:02:30",
        "46384.3347222222",
        "1789804920",
        "1789804920000",
    ],
)
def test_common_ai_and_spreadsheet_timestamps_are_accepted(timestamp: str) -> None:
    response = client.post(
        "/api/analyses",
        files={
            "workers": csv_upload(
                "workers.csv",
                "worker_id,timestamp,zone_id,status\n"
                f'W-2,"{timestamp}",Zone B,active\n',
            )
        },
    )
    assert response.status_code == 201
    summary = response.json()["overview"]["processing_summary"]
    assert summary["valid_records"] == 1
    assert summary["rejected_records"] == 0


def test_time_only_timestamp_is_disclosed_without_inventing_a_source_date() -> None:
    response = client.post(
        "/api/analyses",
        files={
            "workers": csv_upload(
                "workers.csv",
                "worker_id,timestamp,zone_id,status\n"
                "W-2,08:02,Zone B,active\n",
            )
        },
    )
    payload = response.json()
    summary = payload["overview"]["processing_summary"]
    assert summary["valid_records"] == 1
    assert any("source date is unavailable" in warning for warning in summary["warnings"])


def test_time_only_shift_can_generate_and_sort_risks() -> None:
    response = client.post(
        "/api/analyses",
        files={
            "workers": csv_upload(
                "workers.csv",
                "worker_id,timestamp,zone_id,status\n"
                "W-17,08:00,Zone B,active\n"
                "W-17,15:21,Zone B,active\n",
            ),
            "equipment": csv_upload(
                "equipment.csv",
                "equipment_id,equipment_type,timestamp,zone_id,status\n"
                "T-04,truck,15:23,Zone B,active\n",
            ),
            "environment": csv_upload(
                "environment.csv",
                "timestamp,zone_id,gas_level\n"
                "08:00,Zone B,4\n"
                "15:20,Zone B,22\n",
            ),
            "events": csv_upload(
                "events.csv",
                "event_id,timestamp,zone_id,event_type,severity,description\n"
                "E-1,15:24,Zone B,restricted_area_entry,high,Vehicle in restricted area\n",
            ),
        },
    )
    assert response.status_code == 201
    payload = response.json()
    assert payload["overview"]["processing_summary"]["valid_records"] == 6
    assert payload["overview"]["processing_summary"]["rejected_records"] == 0
    assert payload["risks"]


def test_invalid_timestamp_warning_includes_the_original_value() -> None:
    response = client.post(
        "/api/analyses",
        files={
            "workers": csv_upload(
                "workers.csv",
                "worker_id,timestamp,zone_id,status\n"
                "W-2,September someday,Zone B,active\n",
            )
        },
    )
    warnings = response.json()["overview"]["processing_summary"]["warnings"]
    assert any("invalid timestamp 'September someday'" in warning for warning in warnings)


def test_invalid_numeric_is_null_but_record_remains_valid() -> None:
    response = client.post(
        "/api/analyses",
        files={
            "equipment": csv_upload(
                "equipment.csv",
                "equipment_id,equipment_type,timestamp,zone_id,status,speed\n"
                "T-1,truck,2026-09-19T08:10:00,Zone A,active,fast\n",
            )
        },
    )
    assert response.status_code == 201
    summary = response.json()["overview"]["processing_summary"]
    assert summary["valid_records"] == 1
    assert summary["rejected_records"] == 0
    assert any("Invalid numeric value for speed" in warning for warning in summary["warnings"])
    assert not any("Missing speed" in warning for warning in summary["warnings"])


def test_missing_columns_are_reported_and_partial_row_is_retained() -> None:
    response = client.post(
        "/api/analyses",
        files={
            "environment": csv_upload(
                "environment.csv",
                "timestamp,zone_id,gas_level\n"
                "2026-09-19T08:15:00,Zone A,4.2\n",
            )
        },
    )
    assert response.status_code == 201
    file_summary = response.json()["overview"]["files"][2]
    assert file_summary["valid_records"] == 1
    assert any("Missing expected columns" in warning for warning in file_summary["warnings"])


def test_duplicate_and_extra_field_rows_are_rejected() -> None:
    response = client.post(
        "/api/analyses",
        files={
            "events": csv_upload(
                "events.csv",
                "event_id,timestamp,zone_id,event_type,severity,description\n"
                "E-1,2026-09-19T08:20:00,Zone A,inspection,low,check\n"
                "E-1,2026-09-19T08:20:00,Zone A,inspection,low,check\n"
                "E-2,2026-09-19T08:21:00,Zone A,inspection,low,check,extra\n",
            )
        },
    )
    assert response.status_code == 201
    summary = response.json()["overview"]["processing_summary"]
    assert summary["valid_records"] == 1
    assert summary["rejected_records"] == 2


def test_empty_file_returns_completed_analysis_with_warning() -> None:
    response = client.post(
        "/api/analyses",
        files={"workers": csv_upload("workers.csv", "")},
    )
    assert response.status_code == 201
    overview = response.json()["overview"]
    assert overview["shift_started_at"] is None
    assert overview["processing_summary"]["valid_records"] == 0
    assert any("File is empty" in warning for warning in overview["processing_summary"]["warnings"])


def test_header_only_file_is_reported() -> None:
    response = client.post(
        "/api/analyses",
        files={
            "workers": csv_upload(
                "workers.csv",
                "worker_id,timestamp,zone_id,status\n",
            )
        },
    )
    assert response.status_code == 201
    warnings = response.json()["overview"]["processing_summary"]["warnings"]
    assert any("header but no data rows" in warning for warning in warnings)


def test_malformed_csv_row_does_not_hide_later_valid_rows() -> None:
    response = client.post(
        "/api/analyses",
        files={
            "workers": csv_upload(
                "workers.csv",
                "worker_id,timestamp,zone_id,status\n"
                'W-1,2026-09-19T08:00:00,Zone A,"broken\n'
                "W-2,2026-09-19T08:02:00,Zone B,active\n",
            )
        },
    )
    assert response.status_code == 201
    summary = response.json()["overview"]["processing_summary"]
    assert summary["received_records"] == 2
    assert summary["valid_records"] == 1
    assert summary["rejected_records"] == 1


def test_active_counts_use_latest_status_and_dataset_time_window() -> None:
    response = client.post(
        "/api/analyses",
        files={
            "workers": csv_upload(
                "workers.csv",
                "worker_id,timestamp,zone_id,status\n"
                "W-1,2026-09-19T07:00:00,Zone A,active\n"
                "W-1,2026-09-19T08:50:00,Zone A,off_shift\n"
                "W-2,2026-09-19T08:20:00,Zone A,active\n"
                "W-3,2026-09-19T08:45:00,Zone A,active\n",
            ),
            "events": csv_upload(
                "events.csv",
                "event_id,timestamp,zone_id,event_type,severity,description\n"
                "E-1,2026-09-19T09:00:00,Zone A,inspection,low,check\n",
            ),
        },
    )
    assert response.status_code == 201
    overview = response.json()["overview"]
    assert overview["shift_ended_at"] == "2026-09-19T09:00:00"
    assert overview["active_workers"] == 1


def test_question_handles_analysis_with_no_detected_risks() -> None:
    created = create_valid_analysis()
    response = client.post(
        f"/api/analyses/{created['analysis_id']}/questions",
        json={"question": "What is dangerous?"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["answer_mode"] == "deterministic_fallback"
    assert "No risks were detected" in payload["answer"]
    assert payload["observed_facts"] == []


def test_unknown_analysis_returns_404() -> None:
    response = client.get("/api/analyses/unknown/overview")
    assert response.status_code == 404
