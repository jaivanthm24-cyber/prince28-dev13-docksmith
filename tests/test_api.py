import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError
from sqlalchemy.exc import ArgumentError

from docksmith.api.deps import get_session
from docksmith.api.main import create_app
from docksmith.config import Settings


@pytest.fixture
def client():
    settings = Settings(
        app_env="ci",
        data_file="data/sample_records.json",
    )
    app = create_app(settings)

    with TestClient(app) as test_client:
        yield test_client


def test_health_endpoint(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_ready_endpoint(client):
    response = client.get("/ready")

    assert response.status_code == 200
    assert response.json()["status"] == "ready"


def test_ready_returns_503_when_records_missing() -> None:
    class _EmptyResult:
        def scalar_one(self) -> int:
            return 0

    class _EmptySession:
        async def execute(self, _stmt) -> _EmptyResult:
            return _EmptyResult()

    async def _override_session():
        yield _EmptySession()

    app = create_app(
        Settings(
            app_name="docksmith",
            app_env="ci",
            log_level="WARNING",
        )
    )
    app.dependency_overrides[get_session] = _override_session
    res = TestClient(app).get("/ready")
    assert res.status_code == 503
    assert res.json()["status"] == "not_ready"


def test_list_documents(client):
    response = client.get("/v1/documents?limit=2")

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 20
    assert len(data["items"]) == 2


def test_get_multistage_document(client):
    response = client.get("/v1/documents/multi-stage-builds")

    assert response.status_code == 200
    assert response.json()["topic_id"] == "multi-stage-builds"


def test_missing_document(client):
    response = client.get("/v1/documents/999")

    assert response.status_code == 404
    assert response.headers["content-type"].startswith("application/problem+json")


def test_invalid_limit(client):
    response = client.get("/v1/documents?limit=0")

    assert response.status_code == 422
    assert response.headers["content-type"].startswith("application/problem+json")


def test_get_document_by_internal_id(client):
    response = client.get("/v1/documents/001")

    assert response.status_code == 200
    assert response.json()["id"] == "001"
    assert response.json()["topic_id"] == "multi-stage-builds"


def test_settings_rejects_empty_database_url() -> None:
    with pytest.raises((ValidationError, ValueError, ArgumentError)):
        Settings(_env_file=None, database_url="")
