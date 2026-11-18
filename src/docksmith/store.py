"""Loads the hand-entered records from data/sample_records.json."""

import json
from pathlib import Path
from typing import Any

Record = dict[str, Any]


class RecordStore:
    def __init__(self, path: Path) -> None:
        self.path = path
        self._records: dict[str, Record] = {}

    def load(self) -> int:
        data = json.loads(self.path.read_text(encoding="utf-8"))

        if not isinstance(data, list):
            raise ValueError(f"{self.path} must contain a JSON list of records")

        records: dict[str, Record] = {}

        for row in data:
            if "id" not in row:
                raise ValueError(f"every record needs an 'id' field: {row}")

            records[str(row["id"])] = row

        self._records = records
        return len(records)

    @property
    def ready(self) -> bool:
        return bool(self._records)

    def search(self, q: str | None = None) -> list[Record]:
        rows = list(self._records.values())

        if not q:
            return rows

        needle = q.lower()

        return [
            record
            for record in rows
            if any(needle in str(value).lower() for value in record.values())
        ]

    def get(self, record_id: str) -> Record | None:
        # First, search using the internal ID.
        record = self._records.get(record_id)

        if record is not None:
            return record

        # Otherwise, search using the topic identifier.
        for row in self._records.values():
            if row.get("topic_id") == record_id:
                return row

        return None
