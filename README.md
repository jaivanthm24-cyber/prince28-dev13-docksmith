# DockSmith

A Docker and Compose expert that answers from the official Docker docs and checks every Dockerfile it suggests with a linter and a real build.

**Status:** Day 4 Docker, Compose Stack & Test Pyramid (FastAPI, AsyncPG, Alembic, Multi-stage Docker, Compose Stack, Split Test Pyramid, >80% Coverage).

---

## Who It's For

DevOps intern at a Chennai logistics startup whose Python image is 1.8 GB, rebuilds take 9 minutes and the container runs as root.

## The Problem

Docker documentation spans Engine, Build (BuildKit), Compose and extensive reference manuals. Outdated tutorials and forum answers promote deprecated syntax (e.g. `docker-compose v1`, the obsolete `version:` key, `MAINTAINER`), ignore security best practices (running as root), and produce bloated images with broken layer caching that takes 9 minutes to rebuild. DockSmith helps the DevOps intern diagnose these pitfalls, enforce Hadolint compliance, and generate hardened, minimal multi-stage Dockerfiles.

## Data Sources

Docker documentation (`docker/docs` repository: build, engine, compose, reference), the Dockerfile reference, the Compose specification and Docker release notes.

- https://docs.docker.com/
- https://github.com/docker/docs
- https://github.com/compose-spec/compose-spec
- Terms: Docker docs repository Apache-2.0; Compose specification Apache-2.0.

## Hardest Problem (My Interview Story)

Advice that must survive a real build: suggested Dockerfiles must pass hadolint, build with BuildKit and be measured (image size, layers, build time, root vs non-root), and deprecated syntax must be labelled with the current replacement and its doc page.

## Signature Feature

Dockerfile doctor: paste a Dockerfile and get the fixed version with hadolint results and before/after image size and build time.

## Target Metric

90%+ of 30 suggested Dockerfiles build and pass hadolint; average image size cut by 50%+ on 10 bloated samples.

---

## Architecture Overview

```
Client (Web / HTTP)
       │
       ▼
FastAPI Application (docksmith.api.main)
  ├── Lifespan Manager (Engine & Sessionmaker lifecycle)
  ├── Middleware (Request context ID, latency timing, RFC 9457 errors)
  ├── Routes:
  │     ├── GET  /health           (Liveness check)
  │     ├── GET  /ready            (Database readiness check)
  │     ├── GET  /v1/documents     (List, search, JSONB metadata filters)
  │     ├── GET  /v1/documents/{id}(Lookup by external_id or topic_id)
  │     ├── GET  /v1/documents/{id}/pages (Document with page chunks)
  │     └── POST /v1/documents     (Idempotent creation with SHA-256)
       │
       ▼
DocumentRepository (docksmith.db.repository)
       │
       ▼
PostgreSQL Database (SQLAlchemy 2.0 Async + asyncpg)
  ├── documents (id, external_id, title, sha256, metadata [JSONB GIN])
  └── pages     (id, document_id [FK CASCADE], page_no [CHECK >= 1], text)
```

---

## Prerequisites & Installation

### 1. Requirements
- Ubuntu 22.04+ / Linux
- Python 3.12+
- `uv` package manager (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- Docker (for isolated PostgreSQL database)

### 2. Environment Setup
```bash
# Clone and enter directory
cd "day 2/newww"

# Sync dependencies and create virtual environment
uv sync

# Configure environment variables
cp .env.example .env
```

### 3. PostgreSQL Database Setup
DockSmith utilizes a dedicated local PostgreSQL container bound strictly to `127.0.0.1:5432`:

```bash
# Launch PostgreSQL 16 container
docker run -d \
  --name docksmith-postgres \
  --restart unless-stopped \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=docksmith \
  -p 127.0.0.1:5432:5432 \
  -v docksmith-pgdata:/var/lib/postgresql/data \
  postgres:16-alpine

# Verify connectivity
uv run python scripts/db_check.py
```

### 4. Database Migrations
Apply Alembic migrations to construct the database schema and GIN indexes:
```bash
# Upgrade schema to head revision
uv run alembic upgrade head

# (Optional) Verify downgrade and upgrade
uv run alembic downgrade -1
uv run alembic upgrade head
```

### 5. Ingest Records
Load curated Docker & Compose reference records idempotently:
```bash
uv run python scripts/load_db.py
# Output: records=20 inserted=20 updated=0 unchanged=0 pages_synced=40
```

---

## Running the Application

```bash
uv run uvicorn docksmith.api.main:create_app --factory --reload --host 127.0.0.1 --port 8000
```

- Interactive OpenAPI Swagger Docs: `http://localhost:8000/docs`
- Healthcheck: `http://localhost:8000/health`
- Readiness: `http://localhost:8000/ready`
- Documents API: `http://localhost:8000/v1/documents`

---

## API Endpoints

| Method | Path | Description |
| :--- | :--- | :--- |
| `GET` | `/health` | Instant process liveness indicator (`{"status": "ok"}`). |
| `GET` | `/ready` | Database readiness check verifying connectivity (`SELECT 1`). |
| `GET` | `/v1/documents` | List documents with query search (`?q=`), metadata filters (`?category=build`), limit, and offset. |
| `GET` | `/v1/documents/{id}` | Retrieve document by internal ID (`001`) or topic identifier (`multi-stage-builds`). |
| `GET` | `/v1/documents/{id}/pages` | Retrieve document along with its associated chunked pages. |
| `POST` | `/v1/documents` | Create a new document with SHA-256 fingerprinting. |

---

## Running Quality Checks & Tests

```bash
# Run unit test suite (16 tests, fast in-memory, no network)
make test
# Or: uv run poe test

# Run PostgreSQL integration tests (7 tests with real database)
make test-integration
# Or: uv run poe test-integration

# Run branch test coverage (>80% required)
make cov
# Or: uv run poe cov

# Run Ruff linting and formatting check
make lint
# Or: uv run poe lint

# Run pre-commit hooks across all files
uv run pre-commit run --all-files

# Run GIN index EXPLAIN query analysis
uv run python scripts/explain.py
```

---

## Troubleshooting

- **Database connection refused (`ECONNREFUSED` / `Cannot connect to host`)**:
  Verify the Docker container is active: `docker ps | grep docksmith-postgres`. If stopped, restart with `docker start docksmith-postgres`.
- **`psql` client wrapper**:
  A user-space wrapper is available at `~/.local/bin/psql`. Test via `psql -U postgres -d docksmith -c "SELECT 1;"`.
- **Secret scanning warnings**:
  Ensure `.env` is never committed (`.gitignore` protects secrets). Use `.env.example` as a template.

---

## Run locally in one command

You need Docker Desktop running. From a fresh clone:

```bash
docker compose up --build
```

This starts Postgres (with pgvector), Redis, runs the migrations and loads the sample data once, then starts the API.

- API docs: http://localhost:8000/docs
- Liveness: http://localhost:8000/health
- Readiness (checks the database): http://localhost:8000/ready

Stop with `Ctrl+C`, then `docker compose down`. Add `-v` to also delete the database volume.

## Develop and test

| Task | Mac / Linux | Windows |
|---|---|---|
| Run the API with reload | `make dev` | `uv run poe dev` |
| Unit tests (no network) | `make test` | `uv run poe test` |
| Integration tests (needs `docker compose up`) | `make test-integration` | `uv run poe test-integration` |
| Coverage report | `make cov` | `uv run poe cov` |
| Lint and format check | `make lint` | `uv run poe lint` |
