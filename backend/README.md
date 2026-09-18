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

To exercise the complete ingestion endpoint with the included fixtures:

```powershell
curl.exe -X POST http://127.0.0.1:8000/api/analyses `
  -F "workers=@tests/fixtures/workers.csv" `
  -F "equipment=@tests/fixtures/equipment.csv" `
  -F "environment=@tests/fixtures/environment.csv" `
  -F "events=@tests/fixtures/events.csv"
```

## Current phase

`POST /api/analyses` performs real CSV ingestion, header normalization, type coercion,
row-level rejection, duplicate removal, evidence provenance, and shift overview calculation.
Malformed individual rows do not stop the analysis. Deterministic risk detection is the next
implementation phase, so uploaded analyses currently return an empty risk list.

## Frontend integration

Use `docs/frontend-contract.json` in the repository for a stable UI fixture. To test live data,
send one or more files using the `workers`, `equipment`, `environment`, and `events` multipart
fields. At least one file is required. The latest valid dataset timestamp is treated as now;
active entity counts use each entity's latest record within that final 30-minute window.

## Test

```powershell
pytest
```
