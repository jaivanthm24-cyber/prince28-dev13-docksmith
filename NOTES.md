## Day 3 — Postgres Storage, Migrations, and Idempotent Ingestion

### Architecture & Schema Decisions
- **Async Driver & Pooling:** Normalized `DATABASE_URL` to `postgresql+asyncpg://` via `docksmith.db.url.to_asyncpg_url` and enabled `pool_pre_ping=True` for Neon Postgres connection resilience.
- **ORM & Naming Conventions:** Configured a shared SQLAlchemy `Base` with deterministic index, unique, check, foreign key, and primary key naming conventions (`ix_`, `uq_`, `ck_`, `fk_`, `pk_`).
- **Tables & Migrations:**
  - `cc17e2451ac1`: Initial schema defining `documents` (with `external_id`, `metadata_` JSONB, `content_hash`, and timestamps) and `pages` (with `ON DELETE CASCADE` foreign key to `documents.id` and unique `(document_id, page_no)`).
  - `069afa2de3a0`: Added GIN index `ix_documents_metadata_gin` on `documents.metadata_` to accelerate JSONB lookups.
  - Verified full `alembic upgrade head`, `alembic downgrade -1`, `alembic downgrade base`, and re-upgrade cycles.
- **Idempotent Loader (`scripts/load_db.py`):** Computes a canonical SHA-256 `content_hash` per record to insert new rows, update changed rows, and skip unchanged rows across repeated runs.
- **FastAPI Integration:** Wired an async `lifespan` context manager in `create_app` to initialize `app.state.engine` and `app.state.sessionmaker`, injected `AsyncSession` via `get_session`, and preserved all Day 1/Day 2 API contracts and RFC 9457 error shapes.

### Verification Summary
- **Idempotent Ingestion:** Ran `uv run python scripts/load_db.py` multiple times (`20 inserted` on first run; `20 unchanged` on subsequent runs).
- **Live Endpoints:** Verified `200 OK` on `/health`, `/ready` (`{"status":"ready","records":20,"checks":{"records_loaded":true}}`), `/v1/documents`, and `404 Not Found` with RFC 9457 Problem Details on missing IDs.
- **Automated Tests:** Updated `tests/test_api.py` (9 passed).
