# DockSmith

A Docker and Compose expert that answers from the official Docker docs and checks every Dockerfile it suggests with a linter and a real build.

**Status:** Day 1 foundation (FastAPI skeleton, quality gates). Live URL from Day 5.

## Who it's for

DevOps intern at a Chennai logistics startup whose Python image is 1.8 GB, rebuilds take 9 minutes and the container runs as root.

## The problem

Docker documentation spans Engine, Build (BuildKit), Compose and extensive reference manuals. Outdated tutorials and forum answers promote deprecated syntax (e.g. `docker-compose v1`, the obsolete `version:` key, `MAINTAINER`), ignore security best practices (running as root), and produce bloated images with broken layer caching that takes 9 minutes to rebuild. DockSmith helps the DevOps intern diagnose these pitfalls, enforce Hadolint compliance, and generate hardened, minimal multi-stage Dockerfiles.

## Data sources

Docker documentation (`docker/docs` repository: build, engine, compose, reference), the Dockerfile reference, the Compose specification and Docker release notes.

- https://docs.docker.com/
- https://github.com/docker/docs
- https://github.com/compose-spec/compose-spec
- Terms: Docker docs repository Apache-2.0; Compose specification Apache-2.0.

## Hardest problem (my interview story)

Advice that must survive a real build: suggested Dockerfiles must pass hadolint, build with BuildKit and be measured (image size, layers, build time, root vs non-root), and deprecated syntax must be labelled with the current replacement and its doc page.

## Signature feature

Dockerfile doctor: paste a Dockerfile and get the fixed version with hadolint results and before/after image size and build time.

## Target metric

90%+ of 30 suggested Dockerfiles build and pass hadolint; average image size cut by 50%+ on 10 bloated samples.

## Run it locally

```bash
uv sync
copy .env.example .env
uv run uvicorn docksmith.api.main:create_app --factory --reload
```

Then open http://localhost:8000/docs

## Checks

```bash
uv run pytest
uv run ruff check .
```

## Target adjustments

The initial record lookup target is 500 ms to provide a practical performance goal for the first version. The answer cost target is Rs 1.00 per question to allow flexibility while evaluating the AI model and retrieval pipeline. Both targets can be tightened after performance and cost measurements.
