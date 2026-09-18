# AI Mine Safety Incident Prevention Assistant

Backend prototype for the HACK ALEM AI 2026 Extractive Industry challenge.

## Frontend handoff

The backend contract and real CSV ingestion pipeline are ready for frontend development.
The committed JSON file remains a stable UI fixture; uploaded files are processed dynamically.

- Swagger UI after starting the backend: `http://127.0.0.1:8000/docs`
- OpenAPI JSON after starting the backend: `http://127.0.0.1:8000/openapi.json`
- Frontend mock payload: [`docs/frontend-contract.json`](docs/frontend-contract.json)
- Backend instructions: [`backend/README.md`](backend/README.md)

GitHub hosts the source code but does not run this API. Start the backend locally before using
the Swagger or OpenAPI URLs.

## Quick start

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Available endpoints

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `GET` | `/api/health` | Service health |
| `GET` | `/api/config/risk-thresholds` | Active prototype policy thresholds |
| `POST` | `/api/analyses` | Upload four CSV files and start analysis |
| `GET` | `/api/analyses/{analysis_id}/overview` | Shift overview |
| `GET` | `/api/analyses/{analysis_id}/risks` | Prioritized risks |
| `GET` | `/api/analyses/{analysis_id}/risks/{risk_id}` | Risk details |
| `GET` | `/api/analyses/{analysis_id}/evidence/{evidence_id}` | Evidence details |
| `POST` | `/api/analyses/{analysis_id}/questions` | Grounded assistant answer |

## Contract guarantees

- Observed data is separated from interpretation and recommendations.
- Every grounded fact references one or more evidence IDs.
- Risk scores are constrained to `0–100`.
- Priority is one of `CRITICAL`, `HIGH`, `MEDIUM`, or `LOW`.
- Unknown analysis, risk, and evidence IDs return `404`.
- The dataset's latest valid timestamp is treated as the current shift time.
- Active workers and equipment use their latest record within the final 30 minutes of the dataset.
- Deterministic risk detection covers severe events, worker-equipment co-presence, environmental conditions, abnormal statuses, and telemetry inconsistencies.
- Every risk exposes its score breakdown, source evidence, interpretation, action, and limitations.
- Natural-language grounded question answering is the next implementation phase.
