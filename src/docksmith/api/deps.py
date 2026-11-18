from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from docksmith.config import Settings
from docksmith.store import RecordStore


def get_settings(request: Request) -> Settings:
    return request.app.state.settings


async def get_session(request: Request) -> AsyncIterator[AsyncSession]:
    session_factory = request.app.state.sessionmaker
    async with session_factory() as session:
        yield session


def get_store(request: Request) -> RecordStore:
    return request.app.state.store


SettingsDep = Annotated[Settings, Depends(get_settings)]
SessionDep = Annotated[AsyncSession, Depends(get_session)]
StoreDep = Annotated[RecordStore, Depends(get_store)]
