from datetime import datetime

from pydantic import BaseModel, ConfigDict


ScalarValue = str | int | float | bool | None


class NormalizedRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    evidence_id: str
    record_type: str
    source_file: str
    source_row: int
    timestamp: datetime
    zone_id: str | None
    entity_id: str | None
    values: dict[str, ScalarValue]
    validation_issues: list[str]

