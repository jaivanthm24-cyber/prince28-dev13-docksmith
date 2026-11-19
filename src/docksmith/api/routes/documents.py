from typing import Annotated, Any

from fastapi import APIRouter, HTTPException, Query, Request
from pydantic import BaseModel, Field

from docksmith.api.deps import RepoDep
from docksmith.db.repository import FILTER_KEY

router = APIRouter(prefix="/documents", tags=["documents"])

RESERVED = {"q", "limit", "offset"}


class PageCreate(BaseModel):
    page_no: int = Field(ge=1)
    text: str = Field(min_length=1)


class DocumentCreate(BaseModel):
    id: str = Field(min_length=1, max_length=64)
    title: str = Field(min_length=1)
    source_url: str | None = None
    licence: str | None = None
    doc_type: str = "record"
    published_on: str | None = None
    pages: list[PageCreate] | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


@router.get("")
async def list_documents(
    request: Request,
    repo: RepoDep,
    q: Annotated[str | None, Query(max_length=200)] = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> dict:
    """List documents with full-text search and metadata filters."""
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
    """Retrieve document by internal ID or topic identifier."""
    record = await repo.get(doc_id)
    if record is None:
        raise HTTPException(
            status_code=404,
            detail=f"No document with id '{doc_id}'.",
        )
    return record


@router.get("/{doc_id}/pages")
async def get_document_pages(doc_id: str, repo: RepoDep) -> dict:
    """Retrieve document along with its associated pages."""
    record = await repo.get_with_pages(doc_id)
    if record is None:
        raise HTTPException(
            status_code=404,
            detail=f"No document with id '{doc_id}'.",
        )
    return record


@router.post("", status_code=201)
async def create_document(doc_in: DocumentCreate, repo: RepoDep) -> dict:
    """Create a new document with SHA-256 fingerprint."""
    existing = await repo.get(doc_in.id)
    if existing:
        raise HTTPException(
            status_code=409,
            detail=f"Document with id '{doc_in.id}' already exists.",
        )

    doc_data = {
        "id": doc_in.id,
        "title": doc_in.title,
        "source_url": doc_in.source_url,
        "licence": doc_in.licence,
        "doc_type": doc_in.doc_type,
        "published_on": doc_in.published_on,
        **doc_in.metadata,
    }

    pages_data = [p.model_dump() for p in doc_in.pages] if doc_in.pages else None
    return await repo.create(doc_data, pages=pages_data)
