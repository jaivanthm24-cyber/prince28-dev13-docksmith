"""Load data/sample_records.json into Postgres.

Safe to run again and again: new records are inserted, changed ones updated,
unchanged ones skipped (we compare a sha256 fingerprint of each record).

Run: uv run python scripts/load_db.py
"""

import asyncio
import hashlib
import json
from datetime import date

from sqlalchemy import delete, select, update

from docksmith.config import get_settings
from docksmith.db.models import Document, Page
from docksmith.db.session import make_engine, make_sessionmaker

KNOWN = {"id", "title", "official_doc_url", "source_url", "licence", "doc_type", "published_on"}


def fingerprint(record: dict) -> str:
    canonical = json.dumps(record, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def to_row(record: dict) -> dict:
    published = record.get("published_on")
    return {
        "external_id": str(record["id"]),
        "title": str(record.get("title") or record["id"]),
        "source_url": record.get("official_doc_url") or record.get("source_url"),
        "licence": record.get("licence"),
        "doc_type": record.get("doc_type") or "record",
        "published_on": date.fromisoformat(published) if published else None,
        "sha256": fingerprint(record),
        "metadata_": {k: v for k, v in record.items() if k not in KNOWN},
    }


def make_pages(record: dict) -> list[dict]:
    p1_lines = [
        f"# {record['title']}",
        "",
        "## Summary",
        record.get("summary", ""),
        "",
        f"Official Documentation: {record.get('official_doc_url', '')}",
        f"Category: {record.get('category', 'general')} | Type: {record.get('doc_type', 'guide')}",
    ]

    best_practices = record.get("best_practices", [])
    common_mistakes = record.get("common_mistakes", [])
    hadolint_rules = record.get("hadolint_rules", [])

    p2_lines = [
        f"# Best Practices & Hadolint Rules for {record['title']}",
        "",
        "## Best Practices",
    ]
    if best_practices:
        p2_lines.extend(f"- {bp}" for bp in best_practices)
    else:
        p2_lines.append("- Follow official Docker documentation guidelines.")

    p2_lines.append("")
    p2_lines.append("## Common Mistakes")
    if common_mistakes:
        p2_lines.extend(f"- {cm}" for cm in common_mistakes)
    else:
        p2_lines.append("- None reported.")

    if hadolint_rules:
        p2_lines.append("")
        p2_lines.append("## Hadolint Rules")
        p2_lines.extend(f"- {r}" for r in hadolint_rules)

    return [
        {"page_no": 1, "text": "\n".join(p1_lines)},
        {"page_no": 2, "text": "\n".join(p2_lines)},
    ]


async def main() -> None:
    settings = get_settings()
    records = json.loads(settings.data_file.read_text(encoding="utf-8"))
    engine = make_engine(settings)
    session_factory = make_sessionmaker(engine)

    inserted = updated = unchanged = pages_loaded = 0
    async with session_factory() as session, session.begin():
        rows = await session.execute(select(Document.external_id, Document.sha256, Document.id))
        existing = {r[0]: (r[1], r[2]) for r in rows.all()}

        for record in records:
            row = to_row(record)
            pages_data = make_pages(record)
            old_info = existing.get(row["external_id"])

            if old_info is None:
                doc = Document(**row)
                session.add(doc)
                await session.flush()
                for p in pages_data:
                    session.add(Page(document_id=doc.id, page_no=p["page_no"], text=p["text"]))
                inserted += 1
                pages_loaded += len(pages_data)
            elif old_info[0] != row["sha256"]:
                doc_id = old_info[1]
                await session.execute(update(Document).where(Document.id == doc_id).values(**row))
                await session.execute(delete(Page).where(Page.document_id == doc_id))
                for p in pages_data:
                    session.add(Page(document_id=doc_id, page_no=p["page_no"], text=p["text"]))
                updated += 1
                pages_loaded += len(pages_data)
            else:
                doc_id = old_info[1]
                # Ensure pages exist if previously omitted
                existing_pages_count = await session.scalar(
                    select(Page.id).where(Page.document_id == doc_id).limit(1)
                )
                if existing_pages_count is None:
                    for p in pages_data:
                        session.add(Page(document_id=doc_id, page_no=p["page_no"], text=p["text"]))
                    pages_loaded += len(pages_data)
                unchanged += 1

    await engine.dispose()
    print(
        f"records={len(records)} inserted={inserted} updated={updated} "
        f"unchanged={unchanged} pages_synced={pages_loaded}"
    )


if __name__ == "__main__":
    asyncio.run(main())
