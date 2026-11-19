import os

import pytest
from dotenv import dotenv_values
from sqlalchemy import select
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from docksmith.db.models import Base, Document
from docksmith.db.repository import DocumentRepository
from docksmith.db.url import to_asyncpg_url

env = dotenv_values(".env")
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL") or env.get("TEST_DATABASE_URL")

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
    database_name = make_url(database_url).database

    if database_name != "docksmith_test":
        pytest.fail(f"Refusing destructive tests against database: {database_name}")

    engine = create_async_engine(database_url)

    try:
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.drop_all)
            await connection.run_sync(Base.metadata.create_all)

        session_factory = async_sessionmaker(
            engine,
            expire_on_commit=False,
        )

        async with session_factory() as session:
            yield session
    finally:
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.drop_all)

        await engine.dispose()


async def seed_document(session):
    document = Document(
        external_id="TEST-001",
        title="Multi-Stage Builds",
        source_url="https://docs.docker.com/build/building/multi-stage/",
        licence="Apache-2.0",
        doc_type="record",
        sha256="a" * 64,
        metadata_={
            "topic_id": "multi-stage-builds",
            "category": "build",
        },
    )

    session.add(document)
    await session.commit()


async def test_database_tables_created(db_session):
    result = await db_session.execute(select(Document))
    assert result.scalars().all() == []


async def test_insert_and_retrieve_document(db_session):
    await seed_document(db_session)

    repository = DocumentRepository(db_session)
    document = await repository.get("TEST-001")

    assert document is not None
    assert document["topic_id"] == "multi-stage-builds"
    assert document["category"] == "build"


async def test_metadata_filter(db_session):
    await seed_document(db_session)

    repository = DocumentRepository(db_session)

    total, documents = await repository.list(
        q=None,
        filters={"category": "build"},
        limit=10,
        offset=0,
    )

    assert total == 1
    assert documents[0]["category"] == "build"
