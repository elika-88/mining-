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

Expected risk result:

- 6 prioritized risks;
- 5 HIGH or CRITICAL risks;
- top risk: compound Zone B escalation, score 95;
- worker-equipment conflict involving `W-001` and `T-01`;
- adverse Zone B environmental conditions;
- abnormal maintenance status for `L-02`.
