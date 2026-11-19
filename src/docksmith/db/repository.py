"""All SQL for documents lives here. Endpoints never write SQL themselves."""

import hashlib
import json
import re
import uuid
from datetime import date
from typing import Any

from fastapi import HTTPException
from sqlalchemy import Text, cast, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from docksmith.db.models import Document

FILTER_KEY = re.compile(r"^[a-z_][a-z0-9_]{0,40}$")


def to_dict(doc: Document) -> dict[str, Any]:
    """Keep the same flat response shape as the previous API."""
    return {
        "id": doc.external_id,
        **doc.metadata_,
        "title": doc.title,
        "doc_type": doc.doc_type,
        "source_url": doc.source_url,
        "licence": doc.licence,
        "published_on": doc.published_on.isoformat() if doc.published_on else None,
    }


def _value_candidates(value: str) -> list[Any]:
    """Interpret URL values as text, numbers, booleans or list items."""
    out: list[Any] = [value, [value]]
    lowered = value.lower()

    if lowered in ("true", "false"):
        out.append(lowered == "true")
    elif re.fullmatch(r"-?\d+", value):
        out.append(int(value))
    elif re.fullmatch(r"-?\d+\.\d+", value):
        out.append(float(value))

    return out


class DocumentRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list(
        self,
        *,
        q: str | None,
        filters: dict[str, str],
        limit: int,
        offset: int,
    ) -> tuple[int, list[dict[str, Any]]]:
        stmt = select(Document)

        if q:
            like = f"%{q}%"
            stmt = stmt.where(
                or_(
                    Document.title.ilike(like),
                    cast(Document.metadata_, Text).ilike(like),
                )
            )

        for key, value in filters.items():
            stmt = stmt.where(
                or_(
                    *(
                        Document.metadata_.contains({key: candidate})
                        for candidate in _value_candidates(value)
                    )
                )
            )

        total = await self.session.scalar(select(func.count()).select_from(stmt.subquery()))

        rows = await self.session.scalars(
            stmt.order_by(Document.external_id).limit(limit).offset(offset)
        )

        return total or 0, [to_dict(doc) for doc in rows]

    async def get(self, external_id: str) -> dict[str, Any] | None:
        doc = await self.session.scalar(select(Document).where(Document.external_id == external_id))
        if doc is None:
            # Fallback to topic_id match in metadata
            doc = await self.session.scalar(
                select(Document).where(Document.metadata_["topic_id"].as_string() == external_id)
            )
        return to_dict(doc) if doc else None

    async def get_pages(self, external_id: str) -> dict[str, Any] | None:
        stmt = (
            select(Document)
            .options(selectinload(Document.pages))
            .where(Document.external_id == external_id)
        )
        doc = await self.session.scalar(stmt)
        if doc is None:
            stmt = (
                select(Document)
                .options(selectinload(Document.pages))
                .where(Document.metadata_["topic_id"].as_string() == external_id)
            )
            doc = await self.session.scalar(stmt)
        if doc is None:
            return None
        return {
            **to_dict(doc),
            "pages": [
                {"page_no": p.page_no, "text": p.text}
                for p in sorted(doc.pages, key=lambda p: p.page_no)
            ],
        }

    async def create(self, data: dict[str, Any]) -> dict[str, Any]:
        ext_id = str(data.get("id") or uuid.uuid4().hex[:8])
        existing = await self.session.scalar(select(Document).where(Document.external_id == ext_id))
        if existing:
            raise HTTPException(
                status_code=409,
                detail=f"Document with id '{ext_id}' already exists.",
            )

        metadata = data.get("metadata", {})
        title = data.get("title") or ext_id
        canonical = json.dumps(
            {"id": ext_id, "title": title, **metadata},
            sort_keys=True,
            ensure_ascii=False,
            separators=(",", ":"),
        )
        sha = hashlib.sha256(canonical.encode("utf-8")).hexdigest()

        published = data.get("published_on")
        pub_date = None
        if published:
            pub_date = date.fromisoformat(published) if isinstance(published, str) else published

        doc = Document(
            external_id=ext_id,
            title=title,
            doc_type=data.get("doc_type", "record"),
            source_url=data.get("source_url"),
            licence=data.get("licence"),
            published_on=pub_date,
            sha256=sha,
            metadata_=metadata,
        )
        self.session.add(doc)
        await self.session.commit()
        await self.session.refresh(doc)
        return to_dict(doc)
