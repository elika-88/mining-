from collections import OrderedDict
from dataclasses import dataclass

from app.models.normalized import NormalizedRecord
from app.models.responses import AnalysisResponse, Evidence, FileProcessingSummary
from app.services.ingestion import IngestionResult


@dataclass(frozen=True)
class StoredAnalysis:
    response: AnalysisResponse
    records: tuple[NormalizedRecord, ...]
    evidence: dict[str, Evidence]
    ingestion_files: tuple[FileProcessingSummary, ...] = ()
    received_records: int = 0
    rejected_records: int = 0
    ingestion_warnings: tuple[str, ...] = ()


class AnalysisStore:
    def __init__(self, max_analyses: int = 25) -> None:
        self._analyses: OrderedDict[str, StoredAnalysis] = OrderedDict()
        self._max_analyses = max_analyses

    def save(
        self,
        response: AnalysisResponse,
        records: list[NormalizedRecord],
        ingestion: IngestionResult | None = None,
    ) -> None:
        evidence = {
            record.evidence_id: Evidence(
                evidence_id=record.evidence_id,
                source_file=record.source_file,
                source_row=record.source_row,
                timestamp=record.timestamp,
                zone_id=record.zone_id,
                facts=record.values,
                validation_issues=record.validation_issues,
            )
            for record in records
        }
        for risk in response.risks:
            for localized_evidence in risk.observed_data:
                evidence[localized_evidence.evidence_id] = localized_evidence
        self._analyses[response.analysis_id] = StoredAnalysis(
            response=response,
            records=tuple(records),
            evidence=evidence,
            ingestion_files=tuple(ingestion.files if ingestion else response.overview.files),
            received_records=(
                ingestion.received_records
                if ingestion
                else response.overview.processing_summary.received_records
            ),
            rejected_records=(
                ingestion.rejected_records
                if ingestion
                else response.overview.processing_summary.rejected_records
            ),
            ingestion_warnings=tuple(
                ingestion.warnings
                if ingestion
                else response.overview.processing_summary.warnings
            ),
        )
        self._analyses.move_to_end(response.analysis_id)
        while len(self._analyses) > self._max_analyses:
            self._analyses.popitem(last=False)

    def get(self, analysis_id: str) -> StoredAnalysis | None:
        return self._analyses.get(analysis_id)


analysis_store = AnalysisStore()
