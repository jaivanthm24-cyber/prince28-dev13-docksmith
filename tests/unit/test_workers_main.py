from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from arq.connections import RedisSettings

from docksmith.config import Settings
from docksmith.workers.main import WorkerSettings, run_embedded, shutdown, startup, worker_options
from docksmith.workers.queue import Queue, redis_settings


def test_redis_settings():
    s = redis_settings("redis://localhost:6379/1")
    assert isinstance(s, RedisSettings)
    assert s.conn_retries == 1
    assert s.conn_retry_delay == 0


def test_worker_options():
    settings = Settings(app_env="local", redis_url="redis://localhost:6379", _env_file=None)
    opts = worker_options(settings, embedded=True)
    assert opts["max_jobs"] == settings.ingest_concurrency
    assert opts["job_timeout"] == settings.ingest_job_timeout
    assert opts["max_tries"] == settings.ingest_max_tries
    assert opts["ctx"]["embedded"] is True
    assert callable(opts["on_startup"])
    assert callable(opts["on_shutdown"])


def test_worker_settings_class():
    assert isinstance(WorkerSettings, dict)
    assert "functions" in WorkerSettings


@pytest.mark.asyncio
async def test_queue_put_and_close():
    pool = MagicMock()
    pool.enqueue_job = AsyncMock(side_effect=[MagicMock(), None])
    pool.aclose = AsyncMock()

    q = Queue(pool)
    added = await q.put([1, 2])
    assert added == 1
    assert pool.enqueue_job.await_count == 2

    await q.close()
    pool.aclose.assert_awaited_once()


@pytest.mark.asyncio
async def test_startup_and_shutdown():
    settings = Settings(
        app_env="local",
        redis_url="redis://localhost:6379",
        prompts_dir="prompts",
        _env_file=None,
    )
    ctx = {
        "settings": settings,
        "embedded": True,
        "redis": MagicMock(),
    }

    mock_engine = MagicMock()
    mock_engine.dispose = AsyncMock()
    mock_session = MagicMock()
    mock_session.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session.__aexit__ = AsyncMock()
    mock_sessionmaker = MagicMock(return_value=mock_session)

    mock_http = MagicMock()
    mock_http.aclose = AsyncMock()

    with (
        patch("docksmith.workers.main.make_engine", return_value=mock_engine),
        patch("docksmith.workers.main.make_sessionmaker", return_value=mock_sessionmaker),
        patch("docksmith.workers.main.build_gateway") as mock_gw,
        patch("docksmith.workers.main.make_client", return_value=mock_http),
        patch("docksmith.workers.main.IngestRepository") as mock_repo_cls,
        patch("docksmith.workers.main.Queue") as mock_q_cls,
    ):
        mock_gateway = MagicMock()
        mock_gateway.providers = []
        mock_gw.return_value = mock_gateway

        mock_repo = MagicMock()
        mock_repo.open_item_ids = AsyncMock(return_value=[1, 2])
        mock_repo_cls.return_value = mock_repo

        mock_q = MagicMock()
        mock_q.put = AsyncMock(return_value=2)
        mock_q_cls.return_value = mock_q

        await startup(ctx)
        assert ctx["engine"] is mock_engine
        assert ctx["http"] is mock_http

        await shutdown(ctx)
        mock_http.aclose.assert_awaited_once()
        mock_engine.dispose.assert_awaited_once()


@pytest.mark.asyncio
async def test_run_embedded():
    settings = Settings(app_env="local", redis_url="redis://localhost:6379", _env_file=None)
    mock_worker = MagicMock()
    mock_worker.async_run = AsyncMock()
    mock_worker.close = AsyncMock()

    with patch("docksmith.workers.main.Worker", return_value=mock_worker):
        await run_embedded(settings)
        mock_worker.async_run.assert_awaited_once()
