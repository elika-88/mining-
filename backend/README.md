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

Add multipart field `language=en|ru|kk|zh` to select the analysis language. To change
an existing analysis without uploading the files again, call:

```http
POST /api/analyses/{analysis_id}/localize
Content-Type: application/json

{"language":"ru"}
```

The analysis ID, risk IDs, evidence, and data fingerprint remain stable across language changes.
Uploaded values remain untouched; only system-generated analysis and recommendation text is localized.

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
limitations, affected entities, and a score breakdown.

## Grounded AI assistant

`POST /api/analyses/{analysis_id}/questions` supports top-risk, zone-risk, affected-entity,
evidence, recent-change, and shift-overview questions. Every observed fact contains evidence IDs
that resolve through the evidence endpoint.

The request accepts optional `risk_id`, `zone_id`, `entity_id`, and `language` context. Frontends should send
the selected risk ID for questions such as “What evidence supports this alert?” Context is
validated against the current analysis and identifiers from another analysis are rejected.

The optional OpenAI-compatible Chat Completions integration returns a JSON route used only to
classify the question and extract parameters from identifiers already present in the analysis. Final answers,
facts, values, timestamps, recommendations, and limitations are generated deterministically by
the backend. This prevents the model from adding unsupported mine data.

Configuration:

```env
OPENAI_API_KEY=your-key
AI_MODEL=your-available-model-id
AI_BASE_URL=https://api.openai.com/v1
```

Run `./configure-ai.ps1` from the repository root to securely configure OpenAI or a third-party
OpenAI-compatible relay, fetch its `/models` list, and select a model. The relay must support
`/chat/completions`. `AI_API_KEY` is accepted as an alternative key name. If the key or model is absent, the API
times out, the provider fails, or the structured route is invalid, the endpoint automatically
uses `deterministic_fallback`. No API key is required for the fallback.

Values can be placed in `backend/.env`; the application loads this file at startup. The read-only
`GET /api/config/ai` endpoint reports whether routing is configured and never returns the key.
`CORS_ALLOW_ORIGINS` can override the comma-separated frontend origins; both `localhost:5173`
and `127.0.0.1:5173` are enabled by default for the included frontend.

The model output is parsed into a strict Pydantic route and rejected if it references an identifier
that is absent from the uploaded analysis.

Question responses expose `answer_mode`, `model_used`, and a non-sensitive
`fallback_reason`, allowing the interface to distinguish model-assisted routing from the
grounded deterministic fallback. Provider errors and credentials are never returned.

## Frontend integration

Use `docs/frontend-contract.json` in the repository for a stable UI fixture. To test live data,
send one or more files using the `workers`, `equipment`, `environment`, and `events` multipart
fields. At least one file is required. The latest valid dataset timestamp is treated as now;
active entity counts use each entity's latest record within that final 30-minute window.

Every analysis response includes the engine version, analysis timestamp, SHA-256 data
fingerprint, `uploaded_csv` source-of-truth label, and the exact scoring-threshold snapshot.

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

## Known limitations

- In-memory analyses are lost when the server restarts; the store retains only the latest 25 analyses.
- The deterministic language router targets common English, Chinese, Russian, and Kazakh question patterns.
- The optional model improves intent routing only; it does not replace deterministic analysis.
- Zone records do not provide exact worker-equipment distance.
- Sensor and speed units are not defined by the challenge schema.
- Prototype policy thresholds must be aligned with the actual site's operating standards.
- Time-only timestamps are accepted when used consistently. If dated and time-only records are
  mixed, ungrounded time-only rows are excluded instead of inventing calendar dates or comparing
  incompatible time bases.

## Test

```powershell
pytest
```
