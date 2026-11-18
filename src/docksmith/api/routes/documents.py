from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import String, cast, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from docksmith.api.deps import get_session
from docksmith.db.models import Document

router = APIRouter(prefix="/documents", tags=["documents"])


def _serialize(doc: Document) -> dict[str, Any]:
    return {
        "id": doc.external_id,
        "title": doc.title,
        "source_url": doc.source_url,
        "licence": doc.licence,
        "doc_type": doc.doc_type,
        "published_on": doc.published_on.isoformat() if doc.published_on else None,
        **(doc.metadata_ or {}),
    }


@router.get("")
async def list_documents(
    q: Annotated[str | None, Query(max_length=200)] = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
    session: AsyncSession = Depends(get_session),
) -> dict:
    stmt = select(Document).order_by(Document.id)
    if q:
        pattern = f"%{q}%"
        stmt = stmt.where(
            or_(
                Document.title.ilike(pattern),
                Document.external_id.ilike(pattern),
                cast(Document.metadata_, String).ilike(pattern),
            )
        )

    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = (await session.execute(count_stmt)).scalar_one()

    stmt = stmt.offset(offset).limit(limit)
    docs = (await session.execute(stmt)).scalars().all()
    items = [_serialize(doc) for doc in docs]
    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "items": items,
    }


@router.get("/{doc_id}")
async def get_document(
    doc_id: str,
    session: AsyncSession = Depends(get_session),
) -> dict:
    doc = (
        (
            await session.execute(
                select(Document).where(
                    or_(
                        Document.external_id == doc_id,
                        cast(Document.metadata_["topic_id"], String) == f'"{doc_id}"',
                        cast(Document.metadata_["topic_id"], String) == doc_id,
                    )
                )
            )
        )
        .scalars()
        .first()
    )

    if doc is None:
        raise HTTPException(status_code=404, detail=f"No document with id '{doc_id}'.")
    return _serialize(doc)
