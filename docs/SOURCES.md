# Sources & Ingestion Catalog

This document catalogues the primary data sources, documentation repositories, specifications, and license terms used by **DockSmith** for ingestion, retrieval, and verification.

---

## Record Fields Schema

Each ingested record conforms to the following schema:
- `id`: Unique document record identifier (e.g., `DOC-BUILD-001`, `DOC-COMPOSE-002`).
- `page`: Source file path or web page route (e.g., `manuals/engine/reference/builder.md`).
- `section`: Header or anchor section within the document (e.g., `Multi-stage builds`, `COPY --link`).
- `topic`: Domain classification (`buildkit`, `compose`, `security`, `engine`, `cli`, `caching`).
- `instruction_or_key`: Specific Dockerfile directive or Compose top-level key (e.g., `RUN --mount=type=cache`, `services.build.target`).
- `product`: Target ecosystem component (`Docker Engine`, `Docker Buildx`, `Docker Compose`, `Compose Spec`).
- `deprecated`: Boolean flag indicating whether the directive/syntax is deprecated (`true`/`false`).

---

## Data Sources Catalog

| Source ID | Source Name | URL / Repository | Format | License & Terms | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `SRC-DOCS-01` | Docker Official Documentation | https://docs.docker.com/ | Web pages (HTML/Markdown) | Apache-2.0 License | Complete official documentation for Docker Engine, Buildx, Desktop, and CLI reference. |
| `SRC-DOCS-02` | Docker Docs Source Repository | https://github.com/docker/docs | Markdown (`.md`), YAML (`.yaml`) | Apache-2.0 License | Upstream Hugo Markdown source repository containing all current documentation content and guides. |
| `SRC-SPEC-01` | Compose Specification | https://github.com/compose-spec/compose-spec | Markdown specification (`.md`), JSON Schema | Apache-2.0 License | Official open standard defining the Compose file format and key definitions. |
| `SRC-DOCKERFILE-01` | Dockerfile Reference | https://docs.docker.com/reference/dockerfile/ | Web pages (HTML/Markdown) | Apache-2.0 License | Complete reference guide for all Dockerfile instructions, parser directives, and build args. |
| `SRC-RELEASE-01` | Docker Engine Release Notes | https://docs.docker.com/engine/release-notes/ | Web pages (HTML/Markdown) | Apache-2.0 License | Historical and recent changelogs detailing deprecations, removals, and new flags. |
| `SRC-BESTPRACTICES-01` | Docker Development Best Practices | https://docs.docker.com/develop/develop-images/instructions/ | Web pages (HTML/Markdown) | Apache-2.0 License | Official guidance on image layer optimization, caching, security, and non-root execution. |

---

## Terms of Use & Attribution Summary

- **Docker Documentation Repository (`docker/docs`)**: Open source under the **Apache License 2.0**. Permissions allow commercial use, modification, distribution, and private use, with preserved copyright and license notices.
- **Compose Specification (`compose-spec/compose-spec`)**: Open source under the **Apache License 2.0**.
- **Usage Policy**: Ingested documentation data is cached locally for semantic retrieval, linting assistance, and developer guidance without violating rate limits or intellectual property rights.
