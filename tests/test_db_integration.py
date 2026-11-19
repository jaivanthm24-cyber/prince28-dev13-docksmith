import os

import pytest
from dotenv import dotenv_values
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from docksmith.db.models import Document, Page
from docksmith.db.repository import DocumentRepository
from docksmith.db.url import to_asyncpg_url

env = dotenv_values(".env")
TEST_DATABASE_URL = (
    os.getenv("TEST_DATABASE_URL") or env.get("TEST_DATABASE_URL") or env.get("DATABASE_URL")
)

pytestmark = [
    pytest.mark.anyio,
    pytest.mark.skipif(
        not TEST_DATABASE_URL,
        reason="TEST_DATABASE_URL is not configured",
    ),
]


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def db_session():
    if not TEST_DATABASE_URL:
        pytest.skip("TEST_DATABASE_URL is not configured")

    database_url = to_asyncpg_url(TEST_DATABASE_URL)
    engine = create_async_engine(database_url)

    try:
        session_factory = async_sessionmaker(
            engine,
            expire_on_commit=False,
        )

        async with session_factory() as session:
            yield session
    finally:
        await engine.dispose()


async def test_database_tables_accessible(db_session):
    result = await db_session.execute(select(Document))
    docs = result.scalars().all()
    assert len(docs) >= 20


async def test_pages_populated(db_session):
    result = await db_session.execute(select(Page))
    pages = result.scalars().all()
    assert len(pages) >= 40


async def test_repository_get_by_id_and_topic(db_session):
    repo = DocumentRepository(db_session)
    doc_by_id = await repo.get("001")
    assert doc_by_id is not None
    assert doc_by_id["title"] == "Multi-Stage Builds"

    doc_by_topic = await repo.get("multi-stage-builds")
    assert doc_by_topic is not None
    assert doc_by_topic["id"] == "001"


async def test_repository_get_with_pages(db_session):
    repo = DocumentRepository(db_session)
    doc = await repo.get_with_pages("001")
    assert doc is not None
    assert "pages" in doc
    assert len(doc["pages"]) >= 2
    assert doc["pages"][0]["page_no"] == 1


async def test_repository_metadata_filter(db_session):
    repo = DocumentRepository(db_session)
    total, items = await repo.list(
        q=None,
        filters={"category": "build"},
        limit=10,
        offset=0,
    )
    assert total >= 1
    assert any(d.get("category") == "build" for d in items)
