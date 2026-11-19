# Day 3 — PostgreSQL Migration Notes: DockSmith

## 1. Database Connection

- Database: Dedicated PostgreSQL 16 (PostgreSQL 16.16 on x86_64 Alpine Linux, localhost:5432)
- Driver: asyncpg (`postgresql+asyncpg://`)
- ORM: SQLAlchemy 2.0 async sessions
- Connection Pool: `AsyncAdaptedQueuePool` with `pool_pre_ping=True`
- Migrations: Alembic 1.14.0 with async engine runner

## 2. Database Migrations

Two migrations were created and successfully applied to `docksmith` database:

- `cc17e2451ac1`: Create `documents` and `pages` tables with primary keys, unique constraints, foreign keys (`ON DELETE CASCADE`), positive page check constraint, and indexes.
- `069afa2de3a0`: Add GIN index `ix_documents_metadata_gin` on `documents.metadata` using `jsonb_path_ops`.

Verified migration operations:
- `uv run alembic upgrade head` -> applied both migrations.
- `uv run alembic downgrade -1` -> rolled back GIN index cleanly.
- `uv run alembic upgrade head` -> re-applied to head revision.
- Current migration: `069afa2de3a0 (head)`

## 3. Idempotent Loader Evidence

The data loader (`scripts/load_db.py`) was executed multiple times against `data/sample_records.json`:

### First Execution (Initial Seed)
```text
records=20 inserted=20 updated=0 unchanged=0 pages_synced=40
```
Inserted 20 documents and 40 structured pages (overview + best practices/hadolint rules).

### Second Execution (Idempotency Check)
```text
records=20 inserted=0 updated=0 unchanged=20 pages_synced=0
```
Verified that identical content produces matching SHA-256 fingerprints, preventing duplicates.

### Third Execution (Mutation & Update Check)
Verified that modifying a record's content recalculates the SHA-256 fingerprint, updates the document row in place, and synchronizes associated pages without orphan records.

## 4. API Verification

Verified endpoints with live database connectivity:

- `GET /health` -> `200 OK` (`{"status": "ok", "app": "docksmith", "env": "local"}`)
- `GET /ready` -> `200 OK` (`{"status": "ready", "checks": {"database": true}}`)
- `GET /v1/documents` -> `200 OK` (20 documents returned with pagination and filters)
- `GET /v1/documents/001` -> `200 OK` (retrieval by external ID)
- `GET /v1/documents/multi-stage-builds` -> `200 OK` (retrieval by topic identifier)
- `GET /v1/documents/001/pages` -> `200 OK` (retrieval with 2 pages)
- `POST /v1/documents` -> `201 Created` (dynamic document creation with SHA-256)
- `POST /v1/documents` (duplicate) -> `409 Conflict` (duplicate prevention)
- `GET /v1/documents?category=build` -> `200 OK` (JSONB metadata filter)
- `GET /v1/documents?Bad-Name=1` -> `400 Bad Request` (RFC 9457 Problem Details)
- `GET /v1/documents/999` -> `404 Not Found` (RFC 9457 Problem Details)

## 5. Automated Tests

- API unit tests (isolated with FakeRepository & dependency overrides): 20 passed
- PostgreSQL integration tests (`tests/test_db_integration.py` against live database): 5 passed
- Total: 25 passed in 0.88s

Command:
```bash
uv run pytest
```

Quality Gates:
- `uv run ruff check .` -> All checks passed!
- `uv run ruff format --check .` -> 27 files already formatted!
- `uv run pre-commit run --all-files` -> All hooks passed!

## 6. EXPLAIN ANALYZE Evidence

Query:
```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT external_id, title
FROM documents
WHERE metadata @> '{"topic_id": "multi-stage-builds"}'::jsonb;
```

### Normal Query Plan
```text
Seq Scan on documents  (cost=0.00..11.00 rows=1 width=178) (actual time=0.012..0.029 rows=1 loops=1)
  Filter: (metadata @> '{"topic_id": "multi-stage-builds"}'::jsonb)
  Rows Removed by Filter: 19
  Buffers: shared hit=3
Planning Time: 1.657 ms
Execution Time: 0.049 ms
```

### Query Plan with Sequential Scans Disabled (`SET enable_seqscan = off`)
```text
Bitmap Heap Scan on documents  (cost=12.81..16.82 rows=1 width=178) (actual time=0.023..0.024 rows=1 loops=1)
  Recheck Cond: (metadata @> '{"topic_id": "multi-stage-builds"}'::jsonb)
  Heap Blocks: exact=1
  Buffers: shared hit=4
  ->  Bitmap Index Scan on ix_documents_metadata_gin  (cost=0.00..12.81 rows=1 width=0) (actual time=0.014..0.014 rows=1 loops=1)
        Index Cond: (metadata @> '{"topic_id": "multi-stage-builds"}'::jsonb)
        Buffers: shared hit=3
Planning Time: 0.070 ms
Execution Time: 0.085 ms
```

## 7. Engineering Understanding

PostgreSQL's cost-based query optimizer chose a Sequential Scan under normal settings because the `documents` table currently holds 20 records (stored within 1 disk page). Reading a single page sequentially is significantly faster than reading the GIN index tree and subsequently reading the table page.

When `enable_seqscan = off` is set, the optimizer utilizes the `ix_documents_metadata_gin` index via a Bitmap Index Scan and Bitmap Heap Scan. This confirms that the GIN index with `jsonb_path_ops` is correctly structured, registered in catalog metadata, and fully active for containment (`@>`) queries as dataset size scales.
