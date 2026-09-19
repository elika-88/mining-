from io import BytesIO
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)
SAMPLE_ROOT = Path(__file__).parents[2] / "sample_data" / "mock_shift"


def upload(language: str = "en") -> dict:
    files = {
        field: (
            f"{field}.csv",
            BytesIO((SAMPLE_ROOT / f"{field}.csv").read_bytes()),
            "text/csv",
        )
        for field in ("workers", "equipment", "environment", "events")
    }
    response = client.post("/api/analyses", files=files, data={"language": language})
    assert response.status_code == 201
    return response.json()


def test_russian_analysis_localizes_all_interpretive_risk_text() -> None:
    payload = upload("ru")
    assert payload["language"] == "ru"
    assert payload["risks"][0]["title"] == "Комплексное обострение риска в зоне"
    assert "одновременно" in payload["risks"][0]["interpretation"]
    assert "Приостановите" in payload["risks"][0]["recommended_action"]
    assert "первопричину" in payload["risks"][0]["limitations"][0]
    assert any(
        evidence["facts"].get("worker_id") == "W-001"
        for evidence in payload["risks"][0]["observed_data"]
    )
    assert payload["risks"][0]["priority_reasons"][0].startswith("Тяжесть")
    warnings = payload["overview"]["processing_summary"]["warnings"]
    assert any("Строка 7" in warning for warning in warnings)
    assert any("speed (скорость)" in warning for warning in warnings)
    assert all("row was rejected" not in warning for warning in warnings)


def test_analysis_can_be_relocalized_without_uploading_files_again() -> None:
    english = upload("en")
    chinese_response = client.post(
        f"/api/analyses/{english['analysis_id']}/localize",
        json={"language": "zh"},
    )
    assert chinese_response.status_code == 200
    chinese = chinese_response.json()
    assert chinese["analysis_id"] == english["analysis_id"]
    assert chinese["language"] == "zh"
    assert chinese["risks"][0]["title"] == "区域复合风险升级"
    assert chinese["risks"][0]["recommended_action"].startswith("暂停")
    for key in (
        "analysis_id",
        "status",
        "shift_started_at",
        "shift_ended_at",
        "active_workers",
        "active_equipment",
        "shift_events",
        "high_priority_risks",
    ):
        assert chinese["overview"][key] == english["overview"][key]
    for key in ("received_records", "valid_records", "rejected_records"):
        assert (
            chinese["overview"]["processing_summary"][key]
            == english["overview"]["processing_summary"][key]
        )
    assert chinese["metadata"]["data_fingerprint"] == english["metadata"]["data_fingerprint"]
    assert [risk["risk_id"] for risk in chinese["risks"]] == [
        risk["risk_id"] for risk in english["risks"]
    ]
    assert any(
        "第 7 行" in warning
        for warning in chinese["overview"]["processing_summary"]["warnings"]
    )


def test_russian_question_returns_russian_grounded_answer() -> None:
    analysis = upload("ru")
    response = client.post(
        f"/api/analyses/{analysis['analysis_id']}/questions",
        json={"question": "Какой риск требует немедленного внимания?"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["language"] == "ru"
    assert payload["answer"].startswith("Сначала проверьте")
    assert "КРИТИЧЕСКИЙ" in payload["answer"]
    assert "CRITICAL" not in payload["answer"]
    assert payload["observed_facts"]
    assert all("Record at" not in fact["statement"] for fact in payload["observed_facts"])


def test_question_language_override_rebuilds_risk_text_consistently() -> None:
    analysis = upload("en")
    response = client.post(
        f"/api/analyses/{analysis['analysis_id']}/questions",
        json={
            "question": "哪个风险需要立即处理？",
            "language": "zh",
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["language"] == "zh"
    assert payload["answer"].startswith("应首先调查")
    assert "区域复合风险升级" in payload["answer"]
    assert any(
        "worker_id (人员 ID)" in fact["statement"]
        for fact in payload["observed_facts"]
    )


def test_kazakh_localization_is_available() -> None:
    english = upload("en")
    response = client.post(
        f"/api/analyses/{english['analysis_id']}/localize",
        json={"language": "kk"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["language"] == "kk"
    assert payload["risks"][0]["title"] == "Аймақтағы кешенді қауіптің күшеюі"
    assert "міндетті емес жұмысты тоқтатып" in payload["risks"][0]["recommended_action"]


def test_unsupported_language_is_rejected() -> None:
    response = client.post(
        "/api/analyses",
        files={
            "workers": (
                "workers.csv",
                BytesIO((SAMPLE_ROOT / "workers.csv").read_bytes()),
                "text/csv",
            )
        },
        data={"language": "de"},
    )
    assert response.status_code == 422
