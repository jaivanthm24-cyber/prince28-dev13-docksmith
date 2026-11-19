import pytest


def test_health_endpoint(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_ready_endpoint(client):
    response = client.get("/ready")

    assert response.status_code == 200
    assert response.json()["status"] == "ready"


def test_ready_database_down(client, monkeypatch):
    from docksmith.api.deps import check_db

    async def database_down():
        return False

    client.app.dependency_overrides[check_db] = database_down

    response = client.get("/ready")

    assert response.status_code == 503
    assert response.json()["status"] == "not_ready"


def test_list_documents(client):
    response = client.get("/v1/documents?limit=2")

    assert response.status_code == 200
    data = response.json()

    assert data["total"] == 2
    assert len(data["items"]) == 2


def test_list_documents_pagination(client):
    response = client.get("/v1/documents?limit=1&offset=1")

    assert response.status_code == 200
    data = response.json()

    assert data["total"] == 2
    assert len(data["items"]) == 1
    assert data["items"][0]["id"] == "002"


def test_search_documents(client):
    response = client.get("/v1/documents?q=multi-stage")

    assert response.status_code == 200
    data = response.json()

    assert data["total"] == 1
    assert data["items"][0]["topic_id"] == "multi-stage-builds"


def test_metadata_filter(client):
    response = client.get("/v1/documents?category=build")

    assert response.status_code == 200
    data = response.json()

    assert data["total"] == 1
    assert data["items"][0]["topic_id"] == "multi-stage-builds"


def test_invalid_filter_name(client):
    response = client.get("/v1/documents?Bad-Name=1")

    assert response.status_code == 400
    assert response.headers["content-type"].startswith("application/problem+json")


def test_get_document_found(client):
    response = client.get("/v1/documents/001")

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


def test_request_id_echoed(client):
    request_id = "test-request-123"

    response = client.get(
        "/health",
        headers={"X-Request-ID": request_id},
    )

    assert response.status_code == 200
    assert response.headers["X-Request-ID"] == request_id


def test_generated_request_id(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.headers["X-Request-ID"]


def test_settings_required():
    from pydantic import ValidationError

    from docksmith.config import Settings

    with pytest.raises(ValidationError):
        Settings(_env_file=None)


def test_database_url_conversion():
    from docksmith.config import Settings

    settings = Settings(
        app_env="ci",
        database_url="postgresql://localhost:5432/testdb",
        _env_file=None,
    )

    assert settings.database_url.startswith("postgresql+asyncpg://")


def test_database_url_removes_unsupported_parameters():
    from docksmith.config import Settings

    settings = Settings(
        app_env="ci",
        database_url=("postgresql://localhost:5432/testdb?sslmode=require&channel_binding=require"),
        _env_file=None,
    )

    assert settings.database_url.startswith("postgresql+asyncpg://")
    assert "sslmode" not in settings.database_url
    assert "channel_binding" not in settings.database_url
