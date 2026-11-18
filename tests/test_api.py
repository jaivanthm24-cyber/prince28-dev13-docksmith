import pytest
from fastapi.testclient import TestClient

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


def test_list_documents(client):
    response = client.get("/v1/documents?limit=2")

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 5
    assert len(data["items"]) == 2


def test_missing_document(client):
    response = client.get("/v1/documents/999")

    assert response.status_code == 404
    assert response.headers["content-type"].startswith("application/problem+json")


def test_invalid_limit(client):
    response = client.get("/v1/documents?limit=0")

    assert response.status_code == 422
    assert response.headers["content-type"].startswith("application/problem+json")
