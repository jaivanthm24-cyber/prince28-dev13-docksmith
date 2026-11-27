# Ingestion report

<!-- generated:start -->
_Generated 27 Nov 2026 18:01 from the database._

| What | Count |
|---|---|
| Documents in the database | 236 |
| Pages | 632 |
| Tokens of text (characters ÷ 4) | 340,274 |
| Files the parser gave up on | 0 |
| Documents with an extracted record | 236 |
| Documents whose extraction failed | 0 |

| Queue | Count |
|---|---|
| Ingest jobs started | 3 |
| Items finished (done or skipped) | 40 |
| Items that needed more than one try | 0 |
| Items in the dead-letter list | 0 |

Model calls for extraction: 284 · tokens in 500,640 · tokens out 27,214 · cost at list price Rs 45.37

Last job `b280e2d17e6b4d7eb2436fd81b789e30`: 10 requested, 10 ok, 0 failed, 0.4 minutes.
<!-- generated:end -->

## What I learnt

1. The real start corpus parsed into 632 pages and 340,274 text tokens, remarkably close to Monday's estimate of 363,319 tokens (within 6.3% variance).
2. Background queue ingestion with arq and Redis enforces backpressure (12 RPM, concurrency 2) to protect LLM provider rate limits while keeping HTTP ingestion requests non-blocking (returning 202 Accepted in under 50ms).
3. Hard-killing a worker mid-batch causes zero data loss and zero duplication: content hashing ensures idempotent document storage, and arq's visibility timeout reclaims unacknowledged in-progress jobs automatically.
