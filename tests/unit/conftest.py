import pytest
from fastapi.testclient import TestClient

from docksmith.api.deps import check_db, get_gateway, get_repo, get_usage_repo
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


@pytest.fixture
def llm():
    """The fake model behind /v1/chat in unit tests. Put strings or errors in llm.script."""
    return FakeLLM()


@pytest.fixture
def settings():
    return Settings(
        app_env="ci",
        database_url="postgresql://localhost:5432/testdb",
        _env_file=None,
    )


@pytest.fixture
def client(fake_repo, db_state, llm, fake_usage, settings):
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

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
