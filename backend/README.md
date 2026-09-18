# Mine Safety Backend

Contract-first FastAPI backend for the HACK ALEM AI 2026 mock challenge.

## Run locally

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for Swagger UI.

## Current phase

The API contract and mock responses are implemented. `POST /api/analyses` accepts the four
CSV upload fields but intentionally returns documented demo data until CSV ingestion and the
deterministic rule engine are added. Mock content must never be presented as analyzed upload
content in a production or judging build.

## Frontend integration

Use `POST /api/analyses` without files to obtain the complete mock payload. The demo analysis
ID is `demo-analysis-001`. The response separates observed evidence, interpretation,
recommendation, and limitations.

## Test

```powershell
pytest
```
