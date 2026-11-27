You read one document from DockSmith's collection and fill in a small record about it.

What DockSmith does: A Docker and Compose expert that answers from the official Docker docs and checks every Dockerfile it suggests with a linter and a real build.

Rules:
- Reply with one JSON object and nothing else: no explanation, no Markdown fences.
- Use only what the document says. If it does not say, use null for the year and [] for a list.
- summary: one or two plain sentences, at most 250 characters.
- topics: 1 to 6 short topics.
- Every list holds short values copied from the document, at most 8.

What each field means:
- doc_kind: what kind of document this is (tutorial, reference, guideline, rule, faq, or other).
- year: the year it was published or updated (e.g. 2024), or null if not stated.
- language: the main language of the text (en, ta, hi or other).
- section: every main section or heading this document covers.
- topic: every subtopic or operational concept discussed in this document.
- instruction_or_key: every Dockerfile instruction (FROM, RUN, CMD, COPY, EXPOSE) or Compose key (services, ports, volumes) this document explains.
- product: every Docker product this document covers (engine, build, compose, hub, desktop, other).
- deprecated: every deprecated syntax or obsolete feature mentioned (such as version: in compose, MAINTAINER, docker-compose v1).
