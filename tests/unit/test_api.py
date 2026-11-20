import pytest


def test_health_endpoint(client):
    from fastapi.testclient import TestClient

    from docksmith.api.main import create_app
    from docksmith.config import Settings

    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "git_sha" in data
    assert data["git_sha"] == "development"

    # Test health with custom GIT_SHA injected
    custom_settings = Settings(
        app_env="ci",
        database_url="postgresql://localhost:5432/testdb",
        git_sha="sha-custom123",
        _env_file=None,
    )
    custom_app = create_app(custom_settings)
    with TestClient(custom_app) as custom_client:
        custom_resp = custom_client.get("/health")
        assert custom_resp.status_code == 200
        assert custom_resp.json()["git_sha"] == "sha-custom123"


def test_ready_endpoint(client):
    response = client.get("/ready")

    assert response.status_code == 200
    assert response.json()["status"] == "ready"


def test_ready_database_down(client, monkeypatch):
    import asyncio
    from unittest.mock import AsyncMock, MagicMock

    from docksmith.api.deps import check_db, get_app_settings, get_repo, get_session

    req = MagicMock()
    req.app.state.settings = "mock_settings"
    assert get_app_settings(req) == "mock_settings"

    mock_conn = AsyncMock()
    mock_conn.execute.return_value = "ok"
    mock_engine = MagicMock()
    mock_engine.connect.return_value.__aenter__.return_value = mock_conn
    req.app.state.engine = mock_engine
    assert asyncio.run(check_db(req)) is True

    mock_engine.connect.side_effect = RuntimeError("db down")
    assert asyncio.run(check_db(req)) is False

    mock_session = AsyncMock()
    mock_sm = MagicMock()
    mock_sm.return_value.__aenter__.return_value = mock_session
    req.app.state.sessionmaker = mock_sm

    async def run_session():
        async for s in get_session(req):
            repo = await get_repo(s)
            assert repo.session == s

    asyncio.run(run_session())

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
    from datetime import date

    from docksmith.db.models import Document
    from docksmith.db.repository import _value_candidates, to_dict

    assert True in _value_candidates("true")
    assert False in _value_candidates("false")
    assert 42 in _value_candidates("42")
    assert 3.14 in _value_candidates("3.14")
    assert "abc" in _value_candidates("abc")

    doc = Document(
        external_id="D1",
        title="Test",
        metadata_={"k": "v"},
        published_on=date(2025, 1, 1),
    )
    d = to_dict(doc)
    assert d["id"] == "D1"
    assert d["k"] == "v"

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

    pages_resp = client.get("/v1/documents/001/pages")
    assert pages_resp.status_code == 200
    assert "pages" in pages_resp.json()

    create_resp = client.post("/v1/documents", json={"title": "Test Create", "id": "003"})
    assert create_resp.status_code == 201
    assert create_resp.json()["id"] == "003"


def test_missing_document(client):
    response = client.get("/v1/documents/999")

    assert response.status_code == 404
    assert response.headers["content-type"].startswith("application/problem+json")

    pages_resp = client.get("/v1/documents/999/pages")
    assert pages_resp.status_code == 404


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

    @client.app.get("/test-500-endpoint")
    def crash():
        raise RuntimeError("simulated error")

    resp_500 = client.get("/test-500-endpoint", headers={"X-Request-ID": "err-999"})
    assert resp_500.status_code == 500
    assert resp_500.headers["X-Request-ID"] == "err-999"


def test_generated_request_id(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.headers["X-Request-ID"]


def test_settings_required(monkeypatch):
    from pydantic import ValidationError

    from docksmith.config import Settings

    monkeypatch.delenv("APP_ENV", raising=False)
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
