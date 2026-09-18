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
row-level rejection, duplicate removal, evidence provenance, shift overview calculation,
deterministic risk detection, and priority scoring. Malformed individual rows do not stop the
analysis.

Implemented risk families:

- high-severity recorded events;
- worker and moving-equipment co-presence;
- adverse environmental conditions;
- abnormal worker or equipment status;
- stopped-equipment telemetry inconsistencies.

Every risk includes source rows, observed facts, interpretation, recommended action,
limitations, affected entities, and a score breakdown. Natural-language question answering is
the next implementation phase; the current question endpoint returns a deterministic summary.

## Frontend integration

Use `docs/frontend-contract.json` in the repository for a stable UI fixture. To test live data,
send one or more files using the `workers`, `equipment`, `environment`, and `events` multipart
fields. At least one file is required. The latest valid dataset timestamp is treated as now;
active entity counts use each entity's latest record within that final 30-minute window.

## Priority model

Risk scores are deterministic and auditable:

```text
score = severity (0-40)
      + immediacy (0-20)
      + exposure (0-15)
      + corroboration (0-15)
      + magnitude (0-10)
```

- `85-100`: CRITICAL
- `65-84`: HIGH
- `40-64`: MEDIUM
- `0-39`: LOW

Environmental and time-window thresholds are configured through `.env.example`. Because the
challenge schema does not define sensor or speed units, the application never invents units or
claims that a prototype threshold is a regulatory limit.

The active values are available at `GET /api/config/risk-thresholds`. Event severities accept
text labels and the common numeric `4 = high`, `5 = critical` convention; this mapping is a
documented prototype assumption.

## Test

```powershell
pytest
```
