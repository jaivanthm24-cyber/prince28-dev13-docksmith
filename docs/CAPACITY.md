# Capacity plan: DockSmith

Full corpus target: All docs sections + CLI reference + release notes (3,000+ pages)

<!-- generated:start -->
## Measured on my start corpus (2026-11-23 11:08 UTC)

| What | Value |
|---|---|
| Files | 236 |
| Size on disk | 2.9 MB |
| Pages (PDF pages + 1 per 3,000 characters of text/HTML) | 484 |
| Characters of text | 1,453,276 |
| Estimated tokens (characters / 4) | 363,319 |
| Tokens per page | 750 |
| PDFs with almost no text (scanned? OCR is Day 7) | 0 |
| Files not measured (zip, xlsx, unreadable) | 0 |

## Estimate for the full corpus (target: 3,000 pages)

| What | How | Value |
|---|---|---|
| Scale factor | target / measured | x 6.2 |
| Tokens | measured tokens x scale | 2.25 M |
| Raw files | measured MB x scale | 18 MB |
| Chunks | tokens / 400 x 1.15 overlap | 6,469 |
| Embedding cost, one time | tokens x 1.15 x $0.15 per 1M | $0.39 = Rs 37 |
| Vector storage | chunks x 768 numbers x 4 bytes | 20 MB |
| Text in Postgres | characters x scale x 1.2 | 11 MB |

Assumptions: 4 characters per token, 400-token chunks, 768-dimension embeddings at $0.15 per 1M tokens, Rs 95 per US dollar.
<!-- generated:end -->

## What I conclude

1. No, embedding the entire 3,000-page corpus costs only $0.39 (about Rs 37), which is negligible.
2. Yes, vectors (20 MB) plus raw text (11 MB) total ~31 MB, easily fitting into Neon free tier's 500 MB limit (~6.2% utilization).
3. Chunk count (6,469) and tokens per page (750), since Docker code blocks and tables differ from standard prose; I will measure real chunk counts after Day 8 parsing.
4. At 10x growth (30,000 pages), embedding costs ~$3.90 (Rs 370) and Postgres storage reaches ~310 MB, still fitting within Neon's 500 MB limit.
   However, indexing with pgvector will require memory budgeting and HNSW/IVFFlat index tuning for fast vector search.
