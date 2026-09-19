from io import BytesIO
from pathlib import Path
from types import SimpleNamespace

from fastapi.testclient import TestClient

from app.main import app
from app.services import qa

client = TestClient(app)
SAMPLE_ROOT = Path(__file__).parents[2] / "sample_data" / "mock_shift"


def create_analysis() -> dict:
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


def ask(analysis_id: str, question: str, **context: str) -> dict:
    response = client.post(
        f"/api/analyses/{analysis_id}/questions",
        json={"question": question, **context},
    )
    assert response.status_code == 200
    return response.json()


def assert_grounded(payload: dict, analysis_id: str) -> None:
    for fact in payload["observed_facts"]:
        assert fact["evidence_ids"]
        for evidence_id in fact["evidence_ids"]:
            response = client.get(
                f"/api/analyses/{analysis_id}/evidence/{evidence_id}"
            )
            assert response.status_code == 200


def test_immediate_attention_question_returns_top_risk() -> None:
    analysis = create_analysis()
    payload = ask(analysis["analysis_id"], "Which risk requires immediate attention?")
    assert payload["answer_mode"] == "deterministic_fallback"
    assert "High-severity recorded event" in payload["answer"]
    assert "CRITICAL" in payload["answer"]
    assert "score 91" in payload["answer"]
    assert payload["recommended_action"]
    assert_grounded(payload, analysis["analysis_id"])


def test_zone_question_combines_multiple_sources() -> None:
    analysis = create_analysis()
    payload = ask(analysis["analysis_id"], "Why is Zone B dangerous?")
    assert "Zone B has 4 detected risk(s)" in payload["answer"]
    assert "Potential worker–vehicle conflict" in payload["answer"]
    evidence_ids = {
        evidence_id
        for fact in payload["observed_facts"]
        for evidence_id in fact["evidence_ids"]
    }
    source_files = {
        evidence["source_file"]
        for risk in analysis["risks"]
        for evidence in risk["observed_data"]
        if evidence["evidence_id"] in evidence_ids
    }
    assert {"workers.csv", "equipment.csv", "environment.csv", "events.csv"} <= source_files
    assert_grounded(payload, analysis["analysis_id"])


def test_affected_entities_question_names_real_entities() -> None:
    analysis = create_analysis()
    payload = ask(analysis["analysis_id"], "Which workers or vehicles are affected?")
    assert "worker W-001" in payload["answer"]
    assert "equipment T-01" in payload["answer"]
    assert "E-002" not in payload["answer"]
    assert_grounded(payload, analysis["analysis_id"])


def test_evidence_question_returns_citable_facts() -> None:
    analysis = create_analysis()
    payload = ask(analysis["analysis_id"], "What evidence supports this alert?")
    assert "source record(s) support" in payload["answer"]
    assert payload["observed_facts"]
    assert_grounded(payload, analysis["analysis_id"])


def test_selected_risk_context_controls_this_alert_question() -> None:
    analysis = create_analysis()
    conflict = next(
        risk
        for risk in analysis["risks"]
        if risk["title"] == "Potential worker–vehicle conflict"
    )
    payload = ask(
        analysis["analysis_id"],
        "What evidence supports this alert?",
        risk_id=conflict["risk_id"],
    )
    assert "support Potential worker–vehicle conflict" in payload["answer"]
    returned_ids = {
        evidence_id
        for fact in payload["observed_facts"]
        for evidence_id in fact["evidence_ids"]
    }
    assert returned_ids == {
        evidence["evidence_id"] for evidence in conflict["observed_data"]
    }


def test_invalid_question_context_is_rejected() -> None:
    analysis = create_analysis()
    payload = ask(
        analysis["analysis_id"],
        "What evidence supports this alert?",
        risk_id="risk-from-another-analysis",
    )
    assert "not found in this analysis" in payload["answer"]
    assert payload["observed_facts"] == []


def test_recent_changes_use_dataset_time_and_comparable_records() -> None:
    analysis = create_analysis()
    payload = ask(analysis["analysis_id"], "What changed during the last 30 minutes?")
    assert "last 30 minutes of dataset time" in payload["answer"]
    statements = " ".join(fact["statement"] for fact in payload["observed_facts"])
    assert "W-001 changed" in statements
    assert "L-02 changed" in statements
    assert "Zone B environmental readings changed" in statements
    assert "E-002" in statements
    assert_grounded(payload, analysis["analysis_id"])


def test_unknown_zone_returns_insufficient_data_without_invention() -> None:
    analysis = create_analysis()
    payload = ask(analysis["analysis_id"], "Why is Zone Z dangerous?")
    assert "not found in the uploaded data" in payload["answer"]
    assert payload["observed_facts"] == []
    assert payload["interpretation"] is None
    assert "does not infer identifiers" in payload["limitations"][0]


def test_unknown_entity_returns_insufficient_data_without_invention() -> None:
    analysis = create_analysis()
    payload = ask(analysis["analysis_id"], "What happened to worker W-999?")
    assert "not found in the uploaded data" in payload["answer"]
    assert payload["observed_facts"] == []


def test_recent_changes_can_be_filtered_by_zone() -> None:
    analysis = create_analysis()
    payload = ask(
        analysis["analysis_id"],
        "What changed in Zone B during the last 30 minutes?",
    )
    assert "in Zone B during the last 30 minutes" in payload["answer"]
    statements = " ".join(fact["statement"] for fact in payload["observed_facts"])
    assert "Zone B environmental readings changed" in statements
    assert "L-02" not in statements
    assert_grounded(payload, analysis["analysis_id"])


def test_ai_api_failure_falls_back_to_deterministic_grounded_answer(monkeypatch) -> None:
    analysis = create_analysis()

    def failed_router(question, stored_analysis):
        return None

    monkeypatch.setattr(qa, "route_with_openai", failed_router)
    payload = ask(analysis["analysis_id"], "Why is Zone B risky?")
    assert payload["answer_mode"] == "deterministic_fallback"
    assert "Zone B has 4 detected risk(s)" in payload["answer"]
    assert_grounded(payload, analysis["analysis_id"])


def test_openai_structured_route_is_used_without_generating_facts(monkeypatch) -> None:
    analysis = create_analysis()

    class FakeCompletions:
        def create(self, **kwargs):
            assert kwargs["model"] == "test-model"
            assert kwargs["messages"][0]["role"] == "system"
            return SimpleNamespace(
                choices=[
                    SimpleNamespace(
                        message=SimpleNamespace(
                            content='{"intent":"zone_risk","zone_id":"Zone B","entity_id":null,"risk_id":null,"minutes":30}'
                        )
                    )
                ]
            )

    class FakeOpenAI:
        def __init__(self, **kwargs):
            assert kwargs["api_key"] == "test-key"
            assert kwargs["base_url"] == "https://relay.example/v1"
            self.chat = SimpleNamespace(completions=FakeCompletions())

    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("AI_MODEL", "test-model")
    monkeypatch.setenv("AI_BASE_URL", "https://relay.example/v1/")
    monkeypatch.setattr("openai.OpenAI", FakeOpenAI)
    payload = ask(analysis["analysis_id"], "Tell me about Zone B")
    assert payload["answer_mode"] == "llm_routed"
    assert "Zone B has 4 detected risk(s)" in payload["answer"]
    assert_grounded(payload, analysis["analysis_id"])


def test_ai_configuration_never_exposes_key(monkeypatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "secret-value")
    monkeypatch.setenv("AI_MODEL", "test-model")
    monkeypatch.setenv("AI_BASE_URL", "https://api.openai.com/v1?token=base-url-secret")
    response = client.get("/api/config/ai")
    assert response.status_code == 200
    payload = response.json()
    assert payload == {
        "configured": True,
        "model": "test-model",
        "base_url": "https://api.openai.com/v1",
        "fallback_available": True,
    }
    assert "secret-value" not in response.text
    assert "base-url-secret" not in response.text
