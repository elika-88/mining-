import csv
import hashlib
import math
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import PurePath

from fastapi import UploadFile

from app.models.normalized import NormalizedRecord, ScalarValue
from app.models.responses import FileProcessingSummary

MAX_FILE_BYTES = 10 * 1024 * 1024

SCHEMAS: dict[str, dict[str, set[str]]] = {
    "workers": {
        "columns": {"worker_id", "timestamp", "zone_id", "status"},
        "identity": {"worker_id", "timestamp"},
        "numeric": set(),
    },
    "equipment": {
        "columns": {
            "equipment_id",
            "equipment_type",
            "timestamp",
            "zone_id",
            "status",
            "speed",
        },
        "identity": {"equipment_id", "timestamp"},
        "numeric": {"speed"},
    },
    "environment": {
        "columns": {"timestamp", "zone_id", "gas_level", "temperature", "visibility"},
        "identity": {"timestamp"},
        "numeric": {"gas_level", "temperature", "visibility"},
    },
    "events": {
        "columns": {"event_id", "timestamp", "zone_id", "event_type", "severity", "description"},
        "identity": {"event_id", "timestamp"},
        "numeric": set(),
    },
}

ENTITY_ID_FIELDS = {
    "workers": "worker_id",
    "equipment": "equipment_id",
    "events": "event_id",
}


@dataclass
class IngestionResult:
    records: list[NormalizedRecord] = field(default_factory=list)
    files: list[FileProcessingSummary] = field(default_factory=list)
    received_records: int = 0
    rejected_records: int = 0
    warnings: list[str] = field(default_factory=list)


def normalize_header(value: str) -> str:
    return value.strip().lower().replace(" ", "_").lstrip("\ufeff")


def clean_value(value: str | None) -> str | None:
    if value is None:
        return None
    cleaned = value.strip()
    return cleaned if cleaned else None


def parse_timestamp(value: str | None) -> datetime | None:
    cleaned = clean_value(value)
    if cleaned is None:
        return None
    candidate = cleaned[:-1] + "+00:00" if cleaned.endswith(("Z", "z")) else cleaned
    try:
        parsed = datetime.fromisoformat(candidate)
    except ValueError:
        for timestamp_format in (
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %H:%M",
            "%d/%m/%Y %H:%M:%S",
            "%d/%m/%Y %H:%M",
        ):
            try:
                parsed = datetime.strptime(cleaned, timestamp_format)
                break
            except ValueError:
                continue
        else:
            return None
    if parsed.tzinfo is not None:
        parsed = parsed.astimezone(timezone.utc).replace(tzinfo=None)
    return parsed


def parse_number(value: str | None) -> int | float | None:
    cleaned = clean_value(value)
    if cleaned is None:
        return None
    try:
        number = float(cleaned)
    except ValueError:
        return None
    if not math.isfinite(number):
        return None
    return int(number) if number.is_integer() else number


def safe_filename(filename: str | None, file_type: str) -> str:
    if not filename:
        return f"{file_type}.csv"
    return PurePath(filename.replace("\\", "/")).name


def evidence_id(file_type: str, source_file: str, source_row: int, row: dict[str, str | None]) -> str:
    material = f"{file_type}|{source_file}|{source_row}|{sorted(row.items())}"
    digest = hashlib.sha256(material.encode("utf-8")).hexdigest()[:16]
    return f"ev-{digest}"


async def ingest_upload(file_type: str, upload: UploadFile) -> tuple[list[NormalizedRecord], FileProcessingSummary]:
    source_file = safe_filename(upload.filename, file_type)
    warnings: list[str] = []
    received_records = 0
    rejected_records = 0
    records: list[NormalizedRecord] = []

    content = await upload.read(MAX_FILE_BYTES + 1)
    await upload.close()
    if len(content) > MAX_FILE_BYTES:
        return [], FileProcessingSummary(
            file_type=file_type,
            source_file=source_file,
            received_records=0,
            valid_records=0,
            rejected_records=0,
            warnings=[f"File exceeds the {MAX_FILE_BYTES // (1024 * 1024)} MB limit and was skipped."],
        )
    if not content.strip():
        return [], FileProcessingSummary(
            file_type=file_type,
            source_file=source_file,
            received_records=0,
            valid_records=0,
            rejected_records=0,
            warnings=["File is empty."],
        )

    try:
        text = content.decode("utf-8-sig")
    except UnicodeDecodeError:
        return [], FileProcessingSummary(
            file_type=file_type,
            source_file=source_file,
            received_records=0,
            valid_records=0,
            rejected_records=0,
            warnings=["File is not valid UTF-8 and was skipped."],
        )

    lines = text.splitlines()
    try:
        header_values = next(csv.reader([lines[0]], strict=True))
        normalized_headers = [normalize_header(header) for header in header_values]
        if any(not header for header in normalized_headers) or len(set(normalized_headers)) != len(normalized_headers):
            raise csv.Error("CSV contains blank or duplicate column names")
        schema = SCHEMAS[file_type]
        missing_columns = sorted(schema["columns"] - set(normalized_headers))
        if missing_columns:
            warnings.append(f"Missing expected columns: {', '.join(missing_columns)}.")

        seen_rows: set[tuple[tuple[str, str | None], ...]] = set()
        for row_number, raw_line in enumerate(lines[1:], start=2):
            if not raw_line.strip():
                continue
            received_records += 1
            try:
                row_values = next(csv.reader([raw_line], strict=True))
            except csv.Error as error:
                rejected_records += 1
                warnings.append(f"Row {row_number}: malformed CSV ({error}); row was rejected.")
                continue
            if len(row_values) > len(normalized_headers):
                rejected_records += 1
                warnings.append(f"Row {row_number}: too many fields; row was rejected.")
                continue
            row_values.extend([None] * (len(normalized_headers) - len(row_values)))
            raw_row = dict(zip(normalized_headers, row_values, strict=True))
            row = {header: clean_value(value) for header, value in raw_row.items()}
            row_key = tuple(sorted(row.items()))
            if row_key in seen_rows:
                rejected_records += 1
                warnings.append(f"Row {row_number}: duplicate row was excluded.")
                continue
            seen_rows.add(row_key)

            missing_identity = sorted(field for field in schema["identity"] if not row.get(field))
            timestamp = parse_timestamp(row.get("timestamp"))
            if missing_identity or timestamp is None:
                rejected_records += 1
                reasons = []
                if missing_identity:
                    reasons.append(f"missing {', '.join(missing_identity)}")
                if row.get("timestamp") and timestamp is None:
                    reasons.append("invalid timestamp")
                warnings.append(f"Row {row_number}: {'; '.join(reasons)}; row was rejected.")
                continue

            validation_issues: list[str] = []
            values: dict[str, ScalarValue] = {}
            for header in normalized_headers:
                if header == "timestamp":
                    continue
                if header in schema["numeric"]:
                    numeric_value = parse_number(row.get(header))
                    if row.get(header) is not None and numeric_value is None:
                        validation_issues.append(f"Invalid numeric value for {header}; stored as null.")
                    values[header] = numeric_value
                else:
                    values[header] = row.get(header)

            zone_id = row.get("zone_id")
            if zone_id is None:
                validation_issues.append("Missing zone_id; excluded from zone-based analysis.")
            for expected_column in sorted(schema["columns"] - {"timestamp", "zone_id"}):
                if expected_column not in values:
                    values[expected_column] = None
                if values[expected_column] is None and expected_column not in schema["identity"]:
                    validation_issues.append(f"Missing {expected_column}.")

            entity_field = ENTITY_ID_FIELDS.get(file_type)
            entity_id = row.get(entity_field) if entity_field else None
            records.append(
                NormalizedRecord(
                    evidence_id=evidence_id(file_type, source_file, row_number, row),
                    record_type=file_type,
                    source_file=source_file,
                    source_row=row_number,
                    timestamp=timestamp,
                    zone_id=zone_id,
                    entity_id=entity_id,
                    values=values,
                    validation_issues=validation_issues,
                )
            )
    except csv.Error as error:
        warnings.append(f"Malformed CSV: {error}.")

    if received_records == 0 and not warnings:
        warnings.append("File contains a header but no data rows.")
    warnings.extend(
        f"Row {record.source_row}: {issue}" for record in records for issue in record.validation_issues
    )
    summary = FileProcessingSummary(
        file_type=file_type,
        source_file=source_file,
        received_records=received_records,
        valid_records=len(records),
        rejected_records=rejected_records,
        warnings=list(dict.fromkeys(warnings)),
    )
    return records, summary


async def ingest_files(uploads: dict[str, UploadFile | None]) -> IngestionResult:
    result = IngestionResult()
    for file_type, upload in uploads.items():
        if upload is None:
            result.files.append(
                FileProcessingSummary(
                    file_type=file_type,
                    source_file=None,
                    received_records=0,
                    valid_records=0,
                    rejected_records=0,
                    warnings=["File was not provided."],
                )
            )
            continue
        records, summary = await ingest_upload(file_type, upload)
        result.records.extend(records)
        result.files.append(summary)
        result.received_records += summary.received_records
        result.rejected_records += summary.rejected_records
        result.warnings.extend(f"{file_type}: {warning}" for warning in summary.warnings)
    result.warnings = list(dict.fromkeys(result.warnings))
    return result
