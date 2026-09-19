from collections import OrderedDict
from dataclasses import dataclass

from app.models.normalized import NormalizedRecord
from app.models.responses import AnalysisResponse, Evidence


@dataclass(frozen=True)
class StoredAnalysis:
    response: AnalysisResponse
    records: tuple[NormalizedRecord, ...]
    evidence: dict[str, Evidence]


class AnalysisStore:
    def __init__(self, max_analyses: int = 25) -> None:
        self._analyses: OrderedDict[str, StoredAnalysis] = OrderedDict()
        self._max_analyses = max_analyses

    def save(self, response: AnalysisResponse, records: list[NormalizedRecord]) -> None:
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
        self._analyses[response.analysis_id] = StoredAnalysis(
            response=response,
            records=tuple(records),
            evidence=evidence,
        )
        self._analyses.move_to_end(response.analysis_id)
        while len(self._analyses) > self._max_analyses:
            self._analyses.popitem(last=False)

    def get(self, analysis_id: str) -> StoredAnalysis | None:
        return self._analyses.get(analysis_id)


analysis_store = AnalysisStore()
