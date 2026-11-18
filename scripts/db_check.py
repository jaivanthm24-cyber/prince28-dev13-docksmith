import asyncio

from sqlalchemy import text

from docksmith.config import get_settings
from docksmith.db.session import make_engine


async def main() -> None:
    engine = make_engine(get_settings())
    async with engine.connect() as conn:
        db_name = await conn.scalar(text("SELECT current_database()"))
        version = await conn.scalar(text("SELECT version()"))
        print(f"Connected to database '{db_name}'")
        print(version)
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
