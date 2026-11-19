"""All SQL for documents lives here. Endpoints never write SQL themselves."""

from __future__ import annotations

import hashlib
import json
import re
from datetime import date
from typing import Any

from sqlalchemy import Text, cast, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from docksmith.db.models import Document, Page

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
        "published_on": (doc.published_on.isoformat() if doc.published_on else None),
    }


def to_page_dict(page: Page) -> dict[str, Any]:
    return {
        "id": page.id,
        "page_no": page.page_no,
        "text": page.text,
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
                    Document.external_id.ilike(like),
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

    async def get(self, identifier: str) -> dict[str, Any] | None:
        stmt = select(Document).where(
            or_(
                Document.external_id == identifier,
                Document.metadata_.contains({"topic_id": identifier}),
            )
        )
        doc = await self.session.scalar(stmt)
        return to_dict(doc) if doc else None

    async def get_with_pages(self, identifier: str) -> dict[str, Any] | None:
        stmt = (
            select(Document)
            .options(selectinload(Document.pages))
            .where(
                or_(
                    Document.external_id == identifier,
                    Document.metadata_.contains({"topic_id": identifier}),
                )
            )
        )
        doc = await self.session.scalar(stmt)
        if not doc:
            return None
        res = to_dict(doc)
        res["pages"] = [to_page_dict(p) for p in sorted(doc.pages, key=lambda x: x.page_no)]
        return res

    async def create(
        self, data: dict[str, Any], pages: list[dict[str, Any]] | None = None
    ) -> dict[str, Any]:
        canonical = json.dumps(data, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
        sha256 = hashlib.sha256(canonical.encode("utf-8")).hexdigest()

        known = {
            "id",
            "external_id",
            "title",
            "source_url",
            "official_doc_url",
            "licence",
            "doc_type",
            "published_on",
        }
        metadata = {k: v for k, v in data.items() if k not in known}

        pub = data.get("published_on")
        pub_date = date.fromisoformat(pub) if isinstance(pub, str) else pub

        doc = Document(
            external_id=str(data.get("external_id") or data["id"]),
            title=str(data["title"]),
            source_url=data.get("official_doc_url") or data.get("source_url"),
            licence=data.get("licence"),
            doc_type=data.get("doc_type") or "record",
            published_on=pub_date,
            sha256=sha256,
            metadata_=metadata,
        )

        if pages:
            doc.pages = [Page(page_no=p["page_no"], text=p["text"]) for p in pages]

        self.session.add(doc)
        await self.session.commit()
        return to_dict(doc)
