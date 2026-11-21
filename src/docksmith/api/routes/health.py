from fastapi import APIRouter, Response

from docksmith.api.deps import DbCheckDep, SettingsDep

router = APIRouter(tags=["health"])


@router.get("/health")
def health(settings: SettingsDep) -> dict[str, str]:
    """Liveness: is the process alive? Instant. Never touches DB."""
    return {
        "status": "ok",
        "app": settings.app_name,
        "env": settings.app_env,
        "version": settings.git_sha,
        "git_sha": settings.git_sha,
    }


@router.get("/ready")
async def ready(
    db_ok: DbCheckDep,
    response: Response,
) -> dict:
    """Readiness: can this instance serve traffic right now?"""
    checks = {"database": db_ok}
    ok = all(checks.values())

    if not ok:
        response.status_code = 503

    return {
        "status": "ready" if ok else "not_ready",
        "checks": checks,
    }
