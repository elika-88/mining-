# AI Mine Safety Incident Prevention Assistant

Backend prototype for the HACK ALEM AI 2026 Extractive Industry challenge.

## Frontend handoff

The backend contract is ready for frontend development. Until real CSV processing is added,
the API returns clearly documented mock data.

- Swagger UI after starting the backend: `http://127.0.0.1:8000/docs`
- OpenAPI JSON after starting the backend: `http://127.0.0.1:8000/openapi.json`
- Frontend mock payload: [`docs/frontend-contract.json`](docs/frontend-contract.json)
- Demo analysis ID: `demo-analysis-001`
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
