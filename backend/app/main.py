from typing import Annotated

from fastapi import FastAPI, File, HTTPException, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware

from app.mock_data import (
    ANALYSIS_ID,
    DEMO_ANALYSIS,
    DEMO_OVERVIEW,
    DEMO_RISK,
    TRUCK_EVIDENCE,
    WORKER_EVIDENCE,
    build_demo_answer,
)
from app.models.responses import (
    AnalysisResponse,
    Evidence,
    Overview,
    QuestionAnswer,
    QuestionRequest,
    Risk,
)

app = FastAPI(
    title="Mine Safety Incident Prevention API",
    version="0.1.0",
    description=(
        "Contract-first prototype API. Current responses are explicitly marked demo data; "
        "CSV ingestion and deterministic analysis are implemented in the next phase."
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def require_demo_analysis(analysis_id: str) -> None:
    if analysis_id != ANALYSIS_ID:
        raise HTTPException(status_code=404, detail="Analysis not found")


@app.get("/api/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok", "version": app.version}


@app.post(
    "/api/analyses",
    response_model=AnalysisResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["analysis"],
    summary="Upload shift CSV files and start analysis",
)
async def create_analysis(
    workers: Annotated[UploadFile | None, File()] = None,
    equipment: Annotated[UploadFile | None, File()] = None,
    environment: Annotated[UploadFile | None, File()] = None,
    events: Annotated[UploadFile | None, File()] = None,
) -> AnalysisResponse:
    # Phase-one contract endpoint. Files are accepted so frontend integration can begin.
    _ = workers, equipment, environment, events
    return DEMO_ANALYSIS


@app.get(
    "/api/analyses/{analysis_id}/overview",
    response_model=Overview,
    tags=["analysis"],
)
def get_overview(analysis_id: str) -> Overview:
    require_demo_analysis(analysis_id)
    return DEMO_OVERVIEW


@app.get(
    "/api/analyses/{analysis_id}/risks",
    response_model=list[Risk],
    tags=["risks"],
)
def list_risks(analysis_id: str) -> list[Risk]:
    require_demo_analysis(analysis_id)
    return [DEMO_RISK]


@app.get(
    "/api/analyses/{analysis_id}/risks/{risk_id}",
    response_model=Risk,
    tags=["risks"],
)
def get_risk(analysis_id: str, risk_id: str) -> Risk:
    require_demo_analysis(analysis_id)
    if risk_id != DEMO_RISK.risk_id:
        raise HTTPException(status_code=404, detail="Risk not found")
    return DEMO_RISK


@app.get(
    "/api/analyses/{analysis_id}/evidence/{evidence_id}",
    response_model=Evidence,
    tags=["evidence"],
)
def get_evidence(analysis_id: str, evidence_id: str) -> Evidence:
    require_demo_analysis(analysis_id)
    evidence_by_id = {
        WORKER_EVIDENCE.evidence_id: WORKER_EVIDENCE,
        TRUCK_EVIDENCE.evidence_id: TRUCK_EVIDENCE,
    }
    evidence = evidence_by_id.get(evidence_id)
    if evidence is None:
        raise HTTPException(status_code=404, detail="Evidence not found")
    return evidence


@app.post(
    "/api/analyses/{analysis_id}/questions",
    response_model=QuestionAnswer,
    tags=["assistant"],
)
def ask_question(analysis_id: str, request: QuestionRequest) -> QuestionAnswer:
    require_demo_analysis(analysis_id)
    return build_demo_answer(request.question)

