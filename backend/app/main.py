from typing import Annotated

from fastapi import FastAPI, File, HTTPException, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware

from app.models.responses import (
    AnalysisResponse,
    Evidence,
    Overview,
    QuestionAnswer,
    QuestionRequest,
    Risk,
)
from app.services.analysis import build_analysis
from app.services.ingestion import ingest_files
from app.store.memory import StoredAnalysis, analysis_store

app = FastAPI(
    title="Mine Safety Incident Prevention API",
    version="0.2.0",
    description=(
        "Mine-shift CSV ingestion API with row-level validation and evidence provenance. "
        "Deterministic risk detection is implemented in the next phase."
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def require_analysis(analysis_id: str) -> StoredAnalysis:
    analysis = analysis_store.get(analysis_id)
    if analysis is None:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return analysis


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
    uploads = {
        "workers": workers,
        "equipment": equipment,
        "environment": environment,
        "events": events,
    }
    if not any(uploads.values()):
        raise HTTPException(status_code=422, detail="At least one CSV file must be provided.")
    ingestion = await ingest_files(uploads)
    response, records = build_analysis(ingestion)
    analysis_store.save(response, records)
    return response


@app.get(
    "/api/analyses/{analysis_id}/overview",
    response_model=Overview,
    tags=["analysis"],
)
def get_overview(analysis_id: str) -> Overview:
    return require_analysis(analysis_id).response.overview


@app.get(
    "/api/analyses/{analysis_id}/risks",
    response_model=list[Risk],
    tags=["risks"],
)
def list_risks(analysis_id: str) -> list[Risk]:
    return require_analysis(analysis_id).response.risks


@app.get(
    "/api/analyses/{analysis_id}/risks/{risk_id}",
    response_model=Risk,
    tags=["risks"],
)
def get_risk(analysis_id: str, risk_id: str) -> Risk:
    analysis = require_analysis(analysis_id)
    risk = next((risk for risk in analysis.response.risks if risk.risk_id == risk_id), None)
    if risk is None:
        raise HTTPException(status_code=404, detail="Risk not found")
    return risk


@app.get(
    "/api/analyses/{analysis_id}/evidence/{evidence_id}",
    response_model=Evidence,
    tags=["evidence"],
)
def get_evidence(analysis_id: str, evidence_id: str) -> Evidence:
    analysis = require_analysis(analysis_id)
    evidence = analysis.evidence.get(evidence_id)
    if evidence is None:
        raise HTTPException(status_code=404, detail="Evidence not found")
    return evidence


@app.post(
    "/api/analyses/{analysis_id}/questions",
    response_model=QuestionAnswer,
    tags=["assistant"],
)
def ask_question(analysis_id: str, request: QuestionRequest) -> QuestionAnswer:
    require_analysis(analysis_id)
    return QuestionAnswer(
        question=request.question,
        answer=(
            "The uploaded CSV files were processed successfully, but risk detection and "
            "grounded natural-language analysis are not enabled in this ingestion phase."
        ),
        answer_mode="ingestion_only",
        observed_facts=[],
        interpretation=None,
        recommended_action=None,
        limitations=[
            "No safety conclusion was generated from the uploaded records.",
            "Use the overview and file warnings to inspect data quality.",
        ],
    )
