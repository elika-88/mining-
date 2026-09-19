from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class ApiModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Priority(StrEnum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class Language(StrEnum):
    EN = "en"
    KK = "kk"
    RU = "ru"
    ZH = "zh"


class EntityType(StrEnum):
    WORKER = "worker"
    EQUIPMENT = "equipment"
    EVENT = "event"


class AffectedEntity(ApiModel):
    type: EntityType
    id: str


class Evidence(ApiModel):
    evidence_id: str
    source_file: str
    source_row: int = Field(ge=1)
    timestamp: datetime | None
    zone_id: str | None = None
    facts: dict[str, str | int | float | bool | None]
    validation_issues: list[str] = Field(default_factory=list)


class ScoreBreakdown(ApiModel):
    severity: int = Field(ge=0, le=40)
    immediacy: int = Field(ge=0, le=20)
    exposure: int = Field(ge=0, le=15)
    corroboration: int = Field(ge=0, le=15)
    magnitude: int = Field(ge=0, le=10)


class Risk(ApiModel):
    risk_id: str
    title: str
    priority: Priority
    score: int = Field(ge=0, le=100)
    zone_id: str | None
    detected_at: datetime
    affected_entities: list[AffectedEntity]
    observed_data: list[Evidence]
    interpretation: str
    recommended_action: str
    limitations: list[str]
    score_breakdown: ScoreBreakdown


class ProcessingSummary(ApiModel):
    received_records: int = Field(ge=0)
    valid_records: int = Field(ge=0)
    rejected_records: int = Field(ge=0)
    warnings: list[str]


class FileProcessingSummary(ApiModel):
    file_type: str
    source_file: str | None
    received_records: int = Field(ge=0)
    valid_records: int = Field(ge=0)
    rejected_records: int = Field(ge=0)
    warnings: list[str]


class Overview(ApiModel):
    analysis_id: str
    status: str
    shift_started_at: datetime | None
    shift_ended_at: datetime | None
    active_workers: int = Field(ge=0)
    active_equipment: int = Field(ge=0)
    shift_events: int = Field(ge=0)
    high_priority_risks: int = Field(ge=0)
    processing_summary: ProcessingSummary
    files: list[FileProcessingSummary] = Field(default_factory=list)


class AnalysisMetadata(ApiModel):
    engine_version: str
    analyzed_at: datetime
    source_of_truth: str
    data_fingerprint: str
    thresholds: dict[str, float]


class GroundedFact(ApiModel):
    statement: str
    evidence_ids: list[str]


class QuestionAnswer(ApiModel):
    question: str
    language: Language = Language.EN
    answer: str
    answer_mode: str
    model_used: str | None = None
    fallback_reason: str | None = None
    observed_facts: list[GroundedFact]
    interpretation: str | None
    recommended_action: str | None
    limitations: list[str]


class AnalysisResponse(ApiModel):
    analysis_id: str
    language: Language = Language.EN
    overview: Overview
    risks: list[Risk]
    metadata: AnalysisMetadata


class QuestionRequest(ApiModel):
    question: str = Field(min_length=1, max_length=1000)
    language: Language | None = None
    risk_id: str | None = None
    zone_id: str | None = None
    entity_id: str | None = None


class LanguageRequest(ApiModel):
    language: Language
