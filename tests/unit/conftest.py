import pytest
from fastapi.testclient import TestClient

from docksmith.api.deps import (
    check_db,
    get_gateway,
    get_ingest_repo,
    get_manifest,
    get_queue,
    get_repo,
    get_usage_repo,
)
from docksmith.api.main import create_app
from docksmith.config import Settings
from docksmith.llm.gateway import FakeLLM, LLMGateway


class FakeRepository:
    """In-memory repository for API unit tests."""

    def __init__(self):
        self.documents = [
            {
                "id": "001",
                "topic_id": "multi-stage-builds",
                "category": "build",
                "title": "Multi-Stage Builds",
                "doc_type": "guide",
                "source_url": "https://docs.docker.com/build/building/multi-stage/",
                "licence": None,
                "published_on": None,
            },
            {
                "id": "002",
                "topic_id": "cmd-vs-entrypoint",
                "category": "reference",
                "title": "CMD vs ENTRYPOINT Instructions",
                "doc_type": "reference",
                "source_url": "https://docs.docker.com/reference/dockerfile/#entrypoint",
                "licence": None,
                "published_on": None,
            },
        ]

    async def list(self, *, q, filters, limit, offset):
        results = self.documents

        if q:
            results = [
                doc
                for doc in results
                if q.lower() in doc["title"].lower() or q.lower() in doc.get("topic_id", "").lower()
            ]

        for key, value in filters.items():
            results = [doc for doc in results if str(doc.get(key, "")).lower() == value.lower()]

        total = len(results)
        return total, results[offset : offset + limit]

    async def get(self, external_id):
        return next(
            (
                doc
                for doc in self.documents
                if doc["id"] == external_id or doc.get("topic_id") == external_id
            ),
            None,
        )

    async def get_pages(self, external_id):
        doc = await self.get(external_id)
        if not doc:
            return None
        return {
            **doc,
            "pages": [{"page_no": 1, "text": f"Page 1 content for {doc['title']}"}],
        }

    async def create(self, data):
        from fastapi import HTTPException

        ext_id = data.get("id") or "003"
        if any(d["id"] == ext_id for d in self.documents):
            raise HTTPException(
                status_code=409, detail=f"Document with id '{ext_id}' already exists."
            )
        new_doc = {
            "id": ext_id,
            "title": data["title"],
            "doc_type": data.get("doc_type", "record"),
            "source_url": data.get("source_url"),
            "licence": data.get("licence"),
            "published_on": data.get("published_on"),
            **data.get("metadata", {}),
        }
        self.documents.append(new_doc)
        return new_doc


@pytest.fixture
def fake_repo():
    return FakeRepository()


@pytest.fixture
def db_state():
    return {"up": True}


class FakeUsage:
    async def by_day(self, days=7):
        return [
            {
                "day": "2026-11-25",
                "calls": 3,
                "errors": 1,
                "fallbacks": 1,
                "tokens_in": 300,
                "tokens_out": 120,
                "cost_inr": 0.0642,
            }
        ]


@pytest.fixture
def fake_usage():
    return FakeUsage()


class FakeQueue:
    """Remembers which items were queued. No Redis anywhere near a unit test."""

    def __init__(self):
        self.items: list[int] = []

    async def put(self, item_ids):
        self.items += item_ids
        return len(item_ids)


class FakeIngestRepo:
    """Behaves like IngestRepository, with Python lists instead of tables."""

    def __init__(self):
        self.known = {"f-" + "a" * 20}  # one document is already in the database
        self.jobs: dict[str, list[dict]] = {}
        self.failed = [
            {
                "item": 7,
                "job_id": "old",
                "url": "https://x.test/bad.pdf",
                "path": "data/raw/x/bad.pdf",
                "attempts": 3,
                "error": "parse: corrupt",
            }
        ]

    async def known_ids(self):
        return self.known

    async def create(self, records):
        job_id = f"job{len(self.jobs) + 1}"
        self.jobs[job_id] = records
        return job_id, list(range(1, len(records) + 1))

    async def progress(self, job_id):
        if job_id not in self.jobs:
            return None
        counts = {"queued": len(self.jobs[job_id]), "running": 0, "done": 0, "skipped": 0}
        return {"job_id": job_id, "status": "working", "counts": counts | {"failed": 0}}

    async def dead_letter(self, *, job_id=None, limit=50):
        return self.failed[:limit]

    async def failed_records(self):
        return [{"url": item["url"], "path": item["path"]} for item in self.failed]


def manifest_line(n: int, **changes) -> dict:
    record = {
        "url": f"https://x.test/{n}.pdf",
        "source": "x",
        "licence": "CC BY 4.0",
        "path": f"data/raw/x/{n}.pdf",
        "sha256": str(n) * 64,
        "status": "downloaded",
    }
    return record | changes


MANIFEST = [
    manifest_line(1),
    manifest_line(2),
    manifest_line(3, sha256="a" * 64),  # already in the database
    manifest_line(4, status="failed"),  # never downloaded
]


@pytest.fixture
def queue():
    return FakeQueue()


@pytest.fixture
def ingest_repo():
    return FakeIngestRepo()


@pytest.fixture
def llm():
    """The fake model behind /v1/chat in unit tests. Put strings or errors in llm.script."""
    return FakeLLM()


@pytest.fixture
def settings():
    return Settings(
        app_env="ci",
        database_url="postgresql://localhost:5432/testdb",
        admin_token="test-token",  # pragma: allowlist secret
        _env_file=None,
    )


@pytest.fixture
def client(fake_repo, db_state, llm, fake_usage, settings, queue, ingest_repo):
    app = create_app(settings)

    async def override_repo():
        return fake_repo

    async def override_check_db():
        return db_state["up"]

    async def override_usage():
        return fake_usage

    app.dependency_overrides[get_repo] = override_repo
    app.dependency_overrides[check_db] = override_check_db
    app.dependency_overrides[get_gateway] = lambda: LLMGateway([llm])
    app.dependency_overrides[get_usage_repo] = override_usage
    app.dependency_overrides[get_queue] = lambda: queue
    app.dependency_overrides[get_ingest_repo] = lambda: ingest_repo
    app.dependency_overrides[get_manifest] = lambda: MANIFEST

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
