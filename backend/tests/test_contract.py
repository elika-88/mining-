from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_analysis_contract() -> None:
    response = client.post("/api/analyses")
    assert response.status_code == 201
    payload = response.json()
    assert payload["analysis_id"] == "demo-analysis-001"
    assert payload["risks"][0]["priority"] == "HIGH"
    assert payload["risks"][0]["observed_data"][0]["source_file"] == "workers.csv"


def test_question_is_grounded_in_evidence_ids() -> None:
    response = client.post(
        "/api/analyses/demo-analysis-001/questions",
        json={"question": "Why is Zone B dangerous?"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["observed_facts"]
    assert all(fact["evidence_ids"] for fact in payload["observed_facts"])


def test_unknown_analysis_returns_404() -> None:
    response = client.get("/api/analyses/unknown/overview")
    assert response.status_code == 404

