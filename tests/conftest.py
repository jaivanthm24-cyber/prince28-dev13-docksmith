import pytest
from fastapi.testclient import TestClient

from docksmith.api.deps import check_db, get_repo
from docksmith.api.main import create_app
from docksmith.config import Settings


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


@pytest.fixture
def fake_repo():
    return FakeRepository()


@pytest.fixture
def client(fake_repo):
    settings = Settings(
        app_env="ci",
        database_url="postgresql://localhost:5432/testdb",
        _env_file=None,
    )

    app = create_app(settings)

    async def override_repo():
        return fake_repo

    async def override_check_db():
        return True

    app.dependency_overrides[get_repo] = override_repo
    app.dependency_overrides[check_db] = override_check_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
