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
                "title": "Multi-Stage Builds",
                "category": "build",
                "doc_type": "guide",
                "source_url": "https://docs.docker.com/build/building/multi-stage/",
                "licence": None,
                "published_on": None,
                "pages": [
                    {"id": 1, "page_no": 1, "text": "Page 1 overview"},
                    {"id": 2, "page_no": 2, "text": "Page 2 rules"},
                ],
            },
            {
                "id": "002",
                "topic_id": "cmd-vs-entrypoint",
                "title": "CMD vs ENTRYPOINT Instructions",
                "category": "reference",
                "doc_type": "reference",
                "source_url": "https://docs.docker.com/reference/dockerfile/#entrypoint",
                "licence": None,
                "published_on": None,
                "pages": [
                    {"id": 3, "page_no": 1, "text": "Page 1 commands"},
                ],
            },
        ]

    async def list(self, *, q, filters, limit, offset):
        results = self.documents

        if q:
            needle = q.lower()
            results = [
                doc
                for doc in results
                if needle in doc["title"].lower()
                or needle in doc["topic_id"].lower()
                or needle in doc["id"].lower()
            ]

        for key, value in filters.items():
            results = [doc for doc in results if str(doc.get(key, "")).lower() == value.lower()]

        total = len(results)
        return total, [
            {k: v for k, v in doc.items() if k != "pages"}
            for doc in results[offset : offset + limit]
        ]

    async def get(self, identifier):
        for doc in self.documents:
            if doc["id"] == identifier or doc.get("topic_id") == identifier:
                return {k: v for k, v in doc.items() if k != "pages"}
        return None

    async def get_with_pages(self, identifier):
        for doc in self.documents:
            if doc["id"] == identifier or doc.get("topic_id") == identifier:
                return doc
        return None

    async def create(self, data, pages=None):
        doc = dict(data)
        doc["pages"] = pages or []
        self.documents.append(doc)
        return {k: v for k, v in doc.items() if k != "pages"}


@pytest.fixture
def fake_repo():
    return FakeRepository()


@pytest.fixture
def client(fake_repo):
    settings = Settings(
        app_env="ci",
        database_url="postgresql://localhost:5432/testdb",
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
