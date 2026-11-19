import asyncio
import json
import sys

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from docksmith.config import get_settings

QUERY = text("""
    EXPLAIN (ANALYZE, BUFFERS)
    SELECT external_id, title
    FROM documents
    WHERE metadata @> CAST(:filter AS jsonb)
""")


async def main(field: str = "topic_id", value: str = "multi-stage-builds") -> None:
    settings = get_settings()
    engine = create_async_engine(settings.database_url)

    metadata_filter = json.dumps({field: value})

    try:
        async with engine.connect() as connection:
            print("\n--- Normal query plan ---")

            result = await connection.execute(
                QUERY,
                {"filter": metadata_filter},
            )

            for row in result:
                print(row[0])

            print("\n--- Query plan with sequential scans disabled ---")

            await connection.execute(text("SET enable_seqscan = off"))

            result = await connection.execute(
                QUERY,
                {"filter": metadata_filter},
            )

            for row in result:
                print(row[0])

            await connection.rollback()

    finally:
        await engine.dispose()


if __name__ == "__main__":
    if len(sys.argv) == 3:
        asyncio.run(main(sys.argv[1], sys.argv[2]))
    else:
        asyncio.run(main())
