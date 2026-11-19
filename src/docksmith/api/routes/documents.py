from datetime import date
from typing import Annotated, Any

from fastapi import APIRouter, HTTPException, Query, Request
from pydantic import BaseModel, Field

from docksmith.api.deps import RepoDep
from docksmith.db.repository import FILTER_KEY

router = APIRouter(prefix="/documents", tags=["documents"])

RESERVED = {"q", "limit", "offset"}


class DocumentCreate(BaseModel):
    id: str | None = None
    title: str = Field(min_length=1, max_length=500)
    doc_type: str = "record"
    source_url: str | None = None
    licence: str | None = None
    published_on: date | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


@router.get("")
async def list_documents(
    request: Request,
    repo: RepoDep,
    q: Annotated[str | None, Query(max_length=200)] = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> dict:
    """Other query parameters filter on metadata fields."""
    filters = {key: value for key, value in request.query_params.items() if key not in RESERVED}

    bad = [key for key in filters if not FILTER_KEY.match(key)]

    if bad:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid filter name: {bad[0]}",
        )

    total, items = await repo.list(
        q=q,
        filters=filters,
        limit=limit,
        offset=offset,
    )

    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "filters": filters,
        "items": items,
    }


@router.get("/{doc_id}")
async def get_document(doc_id: str, repo: RepoDep) -> dict:
    record = await repo.get(doc_id)

    if record is None:
        raise HTTPException(
            status_code=404,
            detail=f"No document with id '{doc_id}'.",
        )

    return record


@router.get("/{doc_id}/pages")
async def get_document_pages(doc_id: str, repo: RepoDep) -> dict:
    record = await repo.get_pages(doc_id)

    if record is None:
        raise HTTPException(
            status_code=404,
            detail=f"No document with id '{doc_id}'.",
        )

    return record


@router.post("", status_code=201)
async def create_document(payload: DocumentCreate, repo: RepoDep) -> dict:
    created = await repo.create(payload.model_dump())
    return created
