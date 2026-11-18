from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from docksmith.api.deps import SettingsDep, get_session
from docksmith.db.models import Document

router = APIRouter(tags=["health"])


@router.get("/health")
def health(settings: SettingsDep) -> dict:
    return {"status": "ok", "app": settings.app_name, "env": settings.app_env}


@router.get("/ready")
async def ready(session: AsyncSession = Depends(get_session)):
    try:
        count = (await session.execute(select(func.count()).select_from(Document))).scalar_one()
    except Exception as exc:
        return JSONResponse(
            status_code=503,
            content={"status": "not_ready", "reason": f"database unavailable: {exc}"},
        )

    if count < 5:
        return JSONResponse(
            status_code=503,
            content={
                "status": "not_ready",
                "reason": f"need at least 5 records, found {count}",
            },
        )
    return {"status": "ready", "records": count, "checks": {"records_loaded": True}}
