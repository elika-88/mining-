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
    assert payload["risks"][0]["title"] == "Зарегистрировано событие высокой тяжести"
    assert "зарегистрировано" in payload["risks"][0]["interpretation"]
    assert "Проверьте" in payload["risks"][0]["recommended_action"]
    assert "первопричину" in payload["risks"][0]["limitations"][0]
    assert payload["risks"][0]["observed_data"][0]["facts"]["worker_id"] == "W-001"


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
    assert chinese["risks"][0]["title"] == "记录到高严重度事件"
    assert chinese["risks"][0]["recommended_action"].startswith("核实")
    assert chinese["overview"] == english["overview"]
    assert chinese["metadata"]["data_fingerprint"] == english["metadata"]["data_fingerprint"]
    assert [risk["risk_id"] for risk in chinese["risks"]] == [
        risk["risk_id"] for risk in english["risks"]
    ]


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
    assert "记录到高严重度事件" in payload["answer"]


def test_kazakh_localization_is_available() -> None:
    english = upload("en")
    response = client.post(
        f"/api/analyses/{english['analysis_id']}/localize",
        json={"language": "kk"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["language"] == "kk"
    assert payload["risks"][0]["title"] == "Жоғары ауырлықтағы оқиға тіркелді"
    assert "Тіркелген оқиғаны тексеріп" in payload["risks"][0]["recommended_action"]


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
