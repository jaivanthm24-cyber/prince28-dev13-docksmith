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

- API unit tests: 16 passed in 0.22s
- PostgreSQL integration tests: 7 passed in 2.41s
- Total: 23 passed (coverage 85% unit only, 87% full stack with fail_under = 80 enforced)

Commands:
```bash
make test
make test-integration
make cov
```

---

## D04 · Docker, Compose and tests

### The image

```text
$ docker images docksmith:dev
IMAGE           ID             DISK USAGE   CONTENT SIZE   EXTRA
docksmith:dev   2e70dc894d3d        300MB           70MB

$ docker run --rm docksmith:dev id
uid=999(app) gid=999(app) groups=999(app)
```

- Size: 300 MB (target: under 400 MB)
- First build: 31.4 s. After changing one line of code: 2.65 s.
- Which step said CACHED, and why?
The `RUN --mount=type=cache,target=/root/.cache/uv uv sync --locked --no-install-project --no-dev` step was CACHED because `pyproject.toml` and `uv.lock` did not change, allowing BuildKit to reuse pre-installed dependencies.

### The stack

```text
$ docker compose ps -a
NAME                  IMAGE                    COMMAND                  SERVICE   CREATED         STATUS                   PORTS
docksmith-api-1       docksmith-api            "sh -c 'exec uvicorn…"   api       2 minutes ago   Up 2 minutes (healthy)   127.0.0.1:8000->8000/tcp
docksmith-db-1        pgvector/pgvector:pg17   "docker-entrypoint.s…"   db        2 minutes ago   Up 2 minutes (healthy)   127.0.0.1:5432->5432/tcp
docksmith-migrate-1   docksmith-migrate        "sh -c 'alembic upgr…"   migrate   2 minutes ago   Exited (0) 2 minutes ago
docksmith-redis-1     redis:7-alpine           "docker-entrypoint.s…"   redis     2 minutes ago   Up 2 minutes (healthy)   127.0.0.1:6379->6379/tcp

$ docker compose logs migrate
first up: records=20 inserted=20 updated=0 unchanged=0
after down + up: records=20 inserted=0 updated=0 unchanged=20
```

### Breaking the database on purpose

```text
db stopped: /health → {"status":"ok","app":"docksmith","env":"local"}
db stopped: /ready → {"status":"not_ready","checks":{"database":false}} (HTTP 503)
db started: /ready → {"status":"ready","checks":{"database":true}} (HTTP 200)
```

### Tests and coverage

```text
uv run poe test → 16 passed in 0.22s
uv run poe test-integration → 7 passed in 2.41s
coverage TOTAL, unit only → TOTAL: 85% (passes fail_under = 80)
coverage TOTAL, with integration tests → TOTAL: 87%
```

Two files or lines my coverage report says are never run, and whether they matter:
Line 40-41 in `src/docksmith/api/deps.py` handles database ping exceptions, which only run during live database outages; lines 22-24 in `src/docksmith/api/middleware.py` handle unhandled server exception formatting, which are fallback safety nets for unexpected runtime crashes.

---

## D05 · CI/CD, Branch Protection, Deployment & Rollback Drill

### 1. Git SHA Injection & Health Endpoint

- Dockerfile updated with `ARG GIT_SHA="development"` and runtime environment variable `ENV GIT_SHA=$GIT_SHA`.
- `Settings.git_sha` dynamically exposed via `GET /health`:
```json
{
  "status": "ok",
  "app": "docksmith",
  "env": "local",
  "git_sha": "testsha123"
}
```
- Unit tests verify default `development` SHA as well as injected custom SHA values.

### 2. GitHub Actions CI & GHCR Automation

- CI workflow `.github/workflows/ci.yml` enforces strict pipeline dependencies:
  - `docker-build` job depends on all three prior validation jobs: `needs: [lint, unit-tests, integration-tests]`.
  - Docker image is built with `--build-arg GIT_SHA=${{ github.sha }}`.
  - Verification: enforces non-root execution (`uid=999`) and runtime health check asserting the injected `GIT_SHA`.
  - Automated publication to GitHub Container Registry (`ghcr.io`) upon passing all checks:
    - `ghcr.io/jaivanthm24-cyber/prince28-dev13-docksmith:main`
    - `ghcr.io/jaivanthm24-cyber/prince28-dev13-docksmith:<commit_sha>`
    - `ghcr.io/jaivanthm24-cyber/prince28-dev13-docksmith:sha-<commit_sha>`

### 3. Branch Protection Ruleset (`protect-main`)

- Ruleset `protect-main` (ID: `27710737`) active on `main`:
  - Enforce Pull Requests before merging.
  - Require status checks:
    - `Code Quality & Linting`
    - `Unit Tests & Coverage`
    - `PostgreSQL Integration Tests`
    - `Docker Image Build & Verification`
  - Block force pushes (`non_fast_forward`).
  - Prevent branch deletion (`deletion`).

### 4. Continuous Deployment (`.github/workflows/cd.yml`)

- Triggered automatically upon successful CI completion on `main` (`workflow_run`) or on-demand (`workflow_dispatch`).
- Validates required secrets (`DATABASE_URL`, `RENDER_DEPLOY_HOOK`) and variables (`LIVE_URL`).
- Runs production migrations via `alembic upgrade head` on Neon PostgreSQL.
- URL-encodes exact GHCR image URL `ghcr.io/jaivanthm24-cyber/prince28-dev13-docksmith:<commit_sha>` and triggers Render Deploy Hook via `&imgURL=${ENCODED_IMAGE_URL}`.
- Executes strict smoke testing (`scripts/smoke.py`) requiring exact SHA match and database readiness.

### 5. Dedicated Rollback Workflow (`.github/workflows/rollback.yml`)

- Dispatched manually via `workflow_dispatch` with required input `target_sha`.
- Validates target SHA (rejects empty or `development` SHA).
- Skips database migrations by default during rollback (`run_migrations: false`) to avoid schema corruption.
- Deploys exact GHCR image to Render using URL-encoded `imgURL` parameter.
- Runs automated smoke suite asserting `git_sha == target_sha` and database readiness before reporting success.

### 6. Nightly Health Check (`.github/workflows/nightly.yml`)

- Scheduled daily at `02:00 UTC` (`07:30 IST`) via cron `0 2 * * *`.
- Probes `/health` (HTTP 200, status ok), `/ready` (HTTP 200, database connected), and `/docs` (HTTP 200).
- Exits with error if production service is degraded.

### 7. Rollback & Roll-Forward Drill Evidence

- **Rollback Execution**:
  - Run ID: `44864576295`
  - Workflow Run: [Rollback #44864576295](https://github.com/jaivanthm24-cyber/prince28-dev13-docksmith/actions/runs/44864576295)
  - Target SHA: `2c3a2f2` # pragma: allowlist secret
  - Migrations: Skipped (`run_migrations: false` safeguard)
  - Conclusion: **Success**
- **Rollback Verification Log**:
  ```
  === DockSmith Smoke Tests: https://prince28-dev13-docksmith.onrender.com ===
  Expected Git SHA: 2c3a2f2
  [1/24] Probing /health ...
    -> OK (200): running SHA '2c3a2f2' matches expected '2c3a2f2'
  Probing /ready (attempt 1/5) ...
    -> OK (200): database readiness verified ({'status': 'ready', 'checks': {'database': True}})
  Probing /docs ...
    -> OK (200)
  Probing /v1/documents?limit=2 ...
    -> OK (200): total=1, items_returned=1
  === ALL SMOKE TESTS PASSED CLEANLY ===
  ```
- **Recovery Timings (MTTR)**:
  - Incident Detection: ~15 seconds
  - Rollback Dispatch: ~10 seconds
  - Render Image Pull & Redeploy: ~25 seconds
  - Smoke Verification: ~6 seconds
  - Total Recovery Time: ~56 seconds
- **Roll-Forward Execution**:
  - Run ID: `44864654729`
  - Workflow Run: [CD #44864654729](https://github.com/jaivanthm24-cyber/prince28-dev13-docksmith/actions/runs/44864654729)
  - Reapplied forward state and verified live production health.
  - Conclusion: **Success**

### 8. External Production Infrastructure

- **Live URL**: `https://prince28-dev13-docksmith.onrender.com`
- **Render Web Service**: `srv-dc0gbme1egvs73frp42g` (Oregon region, Docker runtime, free tier).
- **Neon PostgreSQL**: `ep-lingering-butterfly-ao1vs7d1-pooler.c-2.ap-southeast-1.aws.neon.tech/neondb` (PostgreSQL 17).
- **GitHub Secrets**: `DATABASE_URL` (Neon URI), `RENDER_DEPLOY_HOOK` (Render webhook).
- **GitHub Variable**: `LIVE_URL` (`https://prince28-dev13-docksmith.onrender.com`).
- **Uptime Monitoring**: UptimeRobot 5-minute HTTP check on `/health`.
- **Release Tag**: Annotated tag `week-1` pushed to remote.


## D06 · Collecting the corpus

- Start target: Build + Dockerfile reference + Compose docs (about 600 pages)
- Collected today: 236 files, 484 pages, 2.9 MB (from DATASET.md)
- Doors used: URL list / Git repository

### Licence check

| Source | Licence or terms, in my words | May I show full text in answers? |
|---|---|---|
| docker-docs | Apache-2.0 (open source documentation) | Yes, with attribution and Apache-2.0 notice |
| docker-website | Docker docs repository Apache-2.0 | Yes, with attribution and link to docs.docker.com |

### robots.txt

- Site: docs.docker.com . Its robots.txt says (2 lines): User-agent: * / Content-Signal: ai-train=yes, search=yes, ai-input=yes
- Was anything blocked for my bot? What did I do about it? Nothing was blocked; robots.txt explicitly allows ai-input and crawl.

### Kill and resume

- Run 1: I pressed Ctrl+C after 3 files
- Run 2: downloaded=7 skipped=3
- Run 3: downloaded=0 skipped=10

### Capacity (from docs/CAPACITY.md)

- Tokens per page, measured: 750
- Full corpus: 2.25 M tokens, 6,469 chunks, embedding about Rs 37, vectors 20 MB
- The number that surprised me most, and why (2 lines):
  Embedding the entire 3,000-page Docker documentation corpus only costs Rs 37 ($0.39), which is far cheaper than expected.
  At the same time, the vectors and chunk text (~31 MB total) comfortably fit in a free-tier Postgres database.

### One thing that went wrong today, and how I fixed it

Running `scripts/fetch.py repo` initially failed because the directory `data/raw/docker-docs` already existed from the HTTP URL download. I updated the source name in `data/sources.csv` to `docker-website` so web pages and git repository files stay isolated in distinct subdirectories without name collision.

## D07 · Parser comparison

<!-- parsers:start -->
| File | Parsers (A / B) | Pages | A found | B found | Time (A / B) | Better, why |
|---|---|---|---|---|---|---|
| dockerfile-6ca35cbd.html | trafilatura / strip tags | 40 | 109,355 chars, 90 headings, 13 tables | 121,232 chars, 104 headings, 0 tables | 0.27 s / 0.02 s | trafilatura: extracts 13 clean Markdown tables and removes ~12KB nav boilerplate |
| volumes-ea5bbea4.html | trafilatura / strip tags | 10 | 25,280 chars, 33 headings, 2 tables | 39,071 chars, 0 headings, 0 tables | 0.06 s / 0.01 s | trafilatura: keeps 33 structural headings and 2 tables; strip tags collapsed to 0 headings |
| best-practices-3cbb6d8f.html | trafilatura / strip tags | 11 | 29,506 chars, 29 headings, 0 tables | 40,951 chars, 12 headings, 0 tables | 0.04 s / 0.01 s | trafilatura: strips 11KB header/nav junk and preserves 29 section headings |
| bind-mounts-3db617b7.html | trafilatura / strip tags | 6 | 16,241 chars, 14 headings, 4 tables | 29,529 chars, 0 headings, 0 tables | 0.03 s / 0.00 s | trafilatura: produces 4 Markdown tables and 14 clean headings; strip tags loses table layout |
| optimize-c53a9295.html | trafilatura / strip tags | 5 | 12,555 chars, 7 headings, 0 tables | 23,766 chars, 4 headings, 0 tables | 0.03 s / 0.00 s | trafilatura: drops 11KB irrelevant nav links; keeps 7 core build cache headings |
| tmpfs-1e363cba.html | trafilatura / strip tags | 3 | 7,696 chars, 7 headings, 2 tables | 20,812 chars, 0 headings, 0 tables | 0.02 s / 0.00 s | trafilatura: extracts 2 structured tables with exact parameters; strip tags flattens them |
| multi-stage-341ad40b.html | trafilatura / strip tags | 3 | 6,064 chars, 6 headings, 0 tables | 18,596 chars, 4 headings, 0 tables | 0.04 s / 0.00 s | trafilatura: extracts 6 clear headings and eliminates 12KB navigation noise |
| cache-98bb87ae.html | trafilatura / strip tags | 1 | 1,525 chars, 2 headings, 0 tables | 12,774 chars, 1 headings, 0 tables | 0.01 s / 0.00 s | trafilatura: accurately captures concise guide content; strip tags had 11KB template fluff |
| compose-file-54b15924.html | trafilatura / strip tags | 1 | 997 chars, 0 headings, 0 tables | 11,123 chars, 0 headings, 0 tables | 0.01 s / 0.00 s | trafilatura: cleans overview prose; strip tags diluted content with 10KB nav links |
| 04-version-and-name-eb4e3746.html | trafilatura / strip tags | 1 | 1,263 chars, 2 headings, 0 tables | 11,079 chars, 0 headings, 0 tables | 0.01 s / 0.00 s | trafilatura: retains 2 key version deprecation headings without header/footer noise |
<!-- parsers:end -->

### D07 · Parsing my corpus

- Files in the manifest: 236 · parsed: 236 · failed: 0 · pages in Postgres: 632
- Parsing coverage: 100 % of files

### Failures by reason

| Reason | Files | What I did |
|---|---|---|
| (none) | 0 | All 236 files parsed cleanly into documents and pages with zero failures |

- The one I fixed: file (none: 0 failures across 236 files) , reason (clean corpus) , fix: verified parser robustness across all Markdown and HTML files

### What I saw when I read my parsed pages

- A page where the heading path is right (document, page, path): File overrides, Page 4, ["File overrides", "Command line", "Override resource limits"]
- Something that came out wrong (document, page, what): File overrides, Page 1, YAML frontmatter (`--- title: ... ---`) was preserved in page 1 raw text
- A table: Markdown grid or loose text? (document, page): Dockerfile reference, Page 15, clean Markdown grid (`| Instruction | Description |`)

### My parser choice

- For PDFs I use PyMuPDF because it detects font sizes to infer hierarchical heading levels and extracts ruled tables into Markdown, whereas pypdf yields plain text without table or heading structure.
- A kind of document in my corpus that neither parser handles well: Multi-column reference tables embedded within raw HTML blocks that lack clear semantic table tags.

### One thing that went wrong today, and how I fixed it

Local `.env` initially had the local compose URL (`postgresql://app:app@localhost:5432/app` # pragma: allowlist secret) which caused connection errors during `alembic upgrade head`. I updated `.env` with the project's Neon PostgreSQL connection string so migrations and corpus parsing store pages directly into the remote database.
