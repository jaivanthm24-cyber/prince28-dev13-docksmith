# Engineering notes: DockSmith

## D03 · PostgreSQL

### Migrations (upgrade, downgrade, upgrade)

```text
$ uv run alembic downgrade -1
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running downgrade 069afa2de3a0 -> cc17e2451ac1, add gin index on metadata

$ uv run alembic current
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
cc17e2451ac1

$ uv run alembic upgrade head
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade cc17e2451ac1 -> 069afa2de3a0, add gin index on metadata

$ uv run alembic history
cc17e2451ac1 -> 069afa2de3a0 (head), add gin index on metadata
<base> -> cc17e2451ac1, create documents and pages
```

### The loader is idempotent

```text
run 1:
records=20 inserted=20 updated=0 unchanged=0

run 2:
records=20 inserted=0 updated=0 unchanged=20

run 3 (after editing one record):
records=20 inserted=0 updated=1 unchanged=19
```

### EXPLAIN for ?topic_id=multi-stage-builds

```text
$ uv run python scripts/explain.py topic_id multi-stage-builds

--- Normal query plan ---
Seq Scan on documents  (cost=0.00..3.25 rows=1 width=178) (actual time=0.019..0.019 rows=1 loops=1)
  Filter: (metadata @> '{"topic_id": "multi-stage-builds"}'::jsonb)
  Rows Removed by Filter: 19
  Buffers: shared hit=3
Planning:
  Buffers: shared hit=126
Planning Time: 0.870 ms
Execution Time: 0.034 ms

--- Query plan with sequential scans disabled ---
Bitmap Heap Scan on documents  (cost=8.54..12.56 rows=1 width=178) (actual time=0.011..0.012 rows=1 loops=1)
  Recheck Cond: (metadata @> '{"topic_id": "multi-stage-builds"}'::jsonb)
  Heap Blocks: exact=1
  Buffers: shared hit=3
  ->  Bitmap Index Scan on ix_documents_metadata_gin  (cost=0.00..8.54 rows=1 width=0) (actual time=0.006..0.006 rows=1 loops=1)
        Index Cond: (metadata @> '{"topic_id": "multi-stage-builds"}'::jsonb)
        Buffers: shared hit=2
Planning:
  Buffers: shared hit=1
Planning Time: 0.046 ms
Execution Time: 0.045 ms
```

Why did the planner choose a Seq Scan on my table? (2 lines, your own words)
With only 20 records residing in 3 shared buffer blocks, scanning all rows directly is significantly cheaper than loading and traversing the GIN index structure. The planner determines that sequential disk/buffer reading incurs less I/O overhead for tiny datasets.

When would it switch to the GIN index? (1 line)
PostgreSQL switches to the GIN index as the table scales to hundreds or thousands of rows where the cost of a full table scan outweighs index traversal and bitmap heap lookups.

---

## 1. Database Connection

- Database: PostgreSQL (Neon compatible)
- Database version: PostgreSQL 16.16
- Driver: asyncpg (`postgresql+asyncpg://`)
- ORM: SQLAlchemy 2.0 (asyncio)
- Migrations: Alembic 1.14+

## 2. Database Migrations

Two migrations were created and successfully applied:
- `cc17e2451ac1`: Create `documents` and `pages` tables with foreign keys and unique constraints.
- `069afa2de3a0`: Add GIN index `ix_documents_metadata_gin` on JSONB metadata using `jsonb_path_ops`.

Verified migration operations:
- Downgrade one revision (`uv run alembic downgrade -1`)
- Verify current revision (`uv run alembic current`)
- Re-upgrade to head (`uv run alembic upgrade head`)
- Inspect revision history (`uv run alembic history`)

Current migration: `069afa2de3a0 (head)`

## 3. Idempotent Loader Evidence

The loader (`scripts/load_db.py`) hashes each record using SHA-256 and compares it against existing rows in a single atomic transaction:
- **First execution** (cold start): `records=20 inserted=20 updated=0 unchanged=0`
- **Second execution** (idempotency check): `records=20 inserted=0 updated=0 unchanged=20`
- **Third execution** (single record edit): `records=20 inserted=0 updated=1 unchanged=19`

## 4. API Verification

Verified endpoints against the PostgreSQL backend:
- `GET /health` -> 200 OK (liveness probe, instant, zero DB overhead)
- `GET /ready` -> 200 OK (`{"status": "ready", "checks": {"database": true}}`)
- `GET /ready` (with simulated DB downtime) -> 503 Service Unavailable (`{"status": "not_ready", "checks": {"database": false}}`)
- `GET /v1/documents?limit=2` -> 200 OK (paginated items with total count)
- `GET /v1/documents?category=build` -> 200 OK (JSONB metadata filter)
- `GET /v1/documents/001` -> 200 OK (document lookup)
- `GET /v1/documents?Bad-Name=1` -> 400 Bad Request (`application/problem+json`)

## 5. Automated Tests

- API unit tests: 16 passed
- PostgreSQL integration tests: 3 passed (or skipped when `TEST_DATABASE_URL` is omitted)
- Total: 19 passed

Commands:
```bash
uv run pytest
TEST_DATABASE_URL="postgresql://localhost:5432/docksmith_test" uv run pytest
```
