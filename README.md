# DockSmith

[![CI](https://github.com/jaivanthm24-cyber/prince28-dev13-docksmith/actions/workflows/ci.yml/badge.svg)](https://github.com/jaivanthm24-cyber/prince28-dev13-docksmith/actions/workflows/ci.yml)
[![CD](https://github.com/jaivanthm24-cyber/prince28-dev13-docksmith/actions/workflows/cd.yml/badge.svg)](https://github.com/jaivanthm24-cyber/prince28-dev13-docksmith/actions/workflows/cd.yml)
[![Deployment](https://img.shields.io/badge/Render-Deployed-success?logo=render&logoColor=white)](https://docksmith.onrender.com)
[![Uptime](https://img.shields.io/badge/Uptime-100%25-brightgreen?logo=uptimerobot&logoColor=white)](https://stats.uptimerobot.com)

A Docker and Compose expert that answers from the official Docker docs and checks every Dockerfile it suggests with a linter and a real build.

**Status:** Production-Ready (Multi-stage Dockerfile, Docker Compose Stack, Split Test Pyramid, PostgreSQL with pgvector, GIN Indexing, CI Workflow).

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
Client (Web / HTTP / CLI)
       │
       ▼
FastAPI Application (docksmith.api.main)
  ├── Lifespan Manager (Engine & Sessionmaker lifecycle)
  ├── Middleware (Request context ID, latency timing, RFC 9457 errors)
  ├── Routes:
  │     ├── GET  /health              (Liveness check)
  │     ├── GET  /ready               (Database readiness check)
  │     ├── GET  /v1/documents        (List, search, JSONB metadata filters)
  │     ├── GET  /v1/documents/{id}   (Lookup by external_id or topic_id)
  │     ├── GET  /v1/documents/{id}/pages (Document with page chunks)
  │     └── POST /v1/documents        (Create document with SHA-256)
       │
       ▼
DocumentRepository (docksmith.db.repository)
       │
       ▼
PostgreSQL Database (SQLAlchemy 2.0 Async + asyncpg on 127.0.0.1:5432)
  ├── documents (id, external_id, title, sha256, metadata [JSONB GIN])
  └── pages     (id, document_id [FK CASCADE], page_no [CHECK >= 1], text)
```

---

## Run Locally in One Command

You only need Docker running. From a fresh clone:

```bash
docker compose up --build -d
```

This starts:
- **Postgres (with pgvector)** on `127.0.0.1:5432` (`app` and `app_test` databases)
- **Redis 7** on `127.0.0.1:6379`
- **Migrate container** (runs `alembic upgrade head` and seeds 20 documents, then exits `0`)
- **FastAPI API** on `127.0.0.1:8000`

Inspect service status:
```bash
docker compose ps
```

- API docs: http://127.0.0.1:8000/docs
- Liveness: http://127.0.0.1:8000/health
- Readiness (checks database connectivity): http://127.0.0.1:8000/ready

To stop the stack:
```bash
docker compose down
# Add -v to clean persistent database volume
docker compose down -v
```

---

## Local Development Workflow

### 1. Requirements
- Linux / macOS / WSL2
- Python 3.12+
- `uv` package manager (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- Docker & Docker Compose

### 2. Environment Configuration
```bash
# Sync local virtual environment
uv sync

# Configure environment variables
cp .env.example .env
```

Standardized environment values in `.env`:
```env
APP_NAME=docksmith
APP_ENV=local
LOG_LEVEL=INFO
DATA_FILE=data/sample_records.json
DATABASE_URL=postgresql://app:app@localhost:5432/app  # pragma: allowlist secret
TEST_DATABASE_URL=postgresql://app:app@localhost:5432/app_test  # pragma: allowlist secret
REDIS_URL=redis://localhost:6379/0
```

### 3. Task Runner Commands

| Task | Make Shortcut | Windows / Poe Task | Description |
|---|---|---|---|
| Start local stack | `make up` | `docker compose up --build -d` | Launches Compose stack in background |
| Stop local stack | `make down` | `docker compose down` | Stops stack containers |
| Run API with reload | `make dev` | `uv run poe dev` | Runs FastAPI on `http://127.0.0.1:8000` |
| Unit tests | `make test` | `uv run poe test` | 16 unit tests (< 0.5s, in-memory) |
| Integration tests | `make test-integration`| `uv run poe test-integration` | 7 PostgreSQL integration tests |
| Coverage report | `make cov` | `uv run poe cov` | Branch coverage (enforces `fail_under = 80`) |
| Lint & format check | `make lint` | `uv run poe lint` | Runs Ruff check and format verification |
| DB migrations | `uv run poe migrate` | `uv run poe migrate` | Applies Alembic migrations |
| Seed database | `uv run poe seed` | `uv run poe seed` | Ingests sample data idempotently |

---

## API Endpoints

All endpoints follow RFC 7807 problem details for errors:

| Method | Path | Description |
| :--- | :--- | :--- |
| `GET` | `/health` | Instant process liveness indicator (`{"status": "ok"}`). |
| `GET` | `/ready` | Database readiness check verifying connectivity (`SELECT 1`). |
| `GET` | `/v1/documents` | List documents with query search (`?q=`), metadata filters (`?category=build`), limit, and offset. |
| `GET` | `/v1/documents/{id}` | Retrieve document by internal ID (`001`) or topic identifier (`multi-stage-builds`). |
| `GET` | `/v1/documents/{id}/pages` | Retrieve document along with its associated chunked pages. |
| `POST` | `/v1/documents` | Create a new document with SHA-256 fingerprinting. |

---

## Quality Checks & Testing

The repository maintains a strict split test pyramid:
- **16 Unit Tests** in `tests/unit/`: fast, in-memory, zero network dependencies, executing in ~0.25s.
- **7 PostgreSQL Integration Tests** in `tests/integration/`: creates an isolated session-scoped test database (`app_test`), executes real Alembic migrations, verifies GIN query planning, loader idempotency, and API integration.
- **Test Coverage**: Branch coverage is enforced with `fail_under = 80` in `pyproject.toml` (currently **85%** unit only, **87%** full stack).
- **Pre-commit Quality Gates**: 9 hooks enforcing formatting, linting, yaml/toml checks, secret detection, and whitespace consistency.

```bash
# Run unit tests
make test

# Run PostgreSQL integration tests
make test-integration

# Run coverage analysis
make cov

# Run all pre-commit hooks
uv run pre-commit run --all-files
```

---

## CI/CD Pipeline

GitHub Actions executes automatically on pull requests and pushes to `main` via [.github/workflows/ci.yml](.github/workflows/ci.yml):
- **Lint & Formatting**: Ruff check and formatting checks.
- **Unit Tests & Coverage**: Executes unit test suite with coverage report.
- **PostgreSQL Integration Tests**: Spins up `pgvector:pg17` and `redis:7-alpine` service containers, runs migrations, and tests real database operations.
- **Docker Build & Security**: Verifies multi-stage build, ensures image size < 400 MB, and verifies non-root user execution (`uid=999`).

---

## Completion Summary

- **Repository**: [jaivanthm24-cyber/prince28-dev13-docksmith](https://github.com/jaivanthm24-cyber/prince28-dev13-docksmith)
- **Port Standardization**: `127.0.0.1:5432` for PostgreSQL, `127.0.0.1:6379` for Redis, `127.0.0.1:8000` for FastAPI API.
- **Docker Image**: Multi-stage build with `uv:0.11.32`, non-root user `app:app` (`uid=999`), lean size: **70 MB** content / **300 MB** disk.
- **Database & Migrations**: PostgreSQL 17 + pgvector, Alembic schema migrations, JSONB metadata with `jsonb_path_ops` GIN index.
- **Test Pyramid**: 23 total automated tests (16 unit, 7 integration) passing with >80% coverage.
