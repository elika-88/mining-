# Mock shift dataset

Synthetic data for local demonstration. It is not organizer-provided or real mine data.

The dataset deliberately contains:

- workers and moving equipment in Zone B;
- worsening Zone B environmental readings;
- high and critical events;
- an equipment maintenance state;
- a missing worker zone;
- invalid timestamps and identifiers;
- invalid numeric telemetry;
- a duplicate equipment record.

Expected ingestion result:

- received records: 23;
- valid records: 19;
- rejected records: 4;
- active workers: 3;
- active equipment: 3;
- shift events: 2;
- dataset time range: `2026-09-19T14:45:00` to `2026-09-19T15:30:00`.

Risk detection is not part of ingestion phase 2, so the current API returns an empty risk list
even though this dataset contains signals intended for the next rule-engine phase.
