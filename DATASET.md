# Dataset: DockSmith

A Docker and Compose expert that answers from the official Docker docs and checks every Dockerfile it suggests with a linter and a real build.

- **Start target:** Build + Dockerfile reference + Compose docs (about 600 pages)
- **Full target:** All docs sections + CLI reference + release notes (3,000+ pages)
- **Collected by:** `scripts/fetch.py` as `examate-student-bot` (https://github.com/jaivanthm24-cyber/prince28-dev13-docksmith): robots.txt respected, at most 4 requests at once, 0.5 s between requests to one site.

## Where the documents come from

- https://docs.docker.com/
- https://github.com/docker/docs
- https://github.com/compose-spec/compose-spec

## Terms I follow

Docker docs repository Apache-2.0; Compose specification Apache-2.0.

- Every answer links to the original document.
- No personal data is collected.

<!-- generated:start -->
## Sources (generated 2026-11-23 11:08 UTC by scripts/dataset_report.py)

| Source | Licence / terms | Files | MB | Pages* | How | Fetched | Example URL |
|---|---|---|---|---|---|---|---|
| docker-docs | Docker docs repository Apache-2.0 | 226 | 1.2 | 408 | git @ 571ed524fa | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/_index.md |
| docker-website | Docker docs repository Apache-2.0 | 10 | 1.7 | 76 | http | 2026-11-23 | https://docs.docker.com/build/building/multi-stage/ |

**Total:** 236 files, 2.9 MB, 484 pages. Not downloaded: 0 blocked by robots.txt, 0 failed.

*Pages = PDF pages, plus one page per 3,000 characters of text or HTML.

## Files (first 200 of 236)

The complete list, with a sha256 fingerprint of every file, is `data/manifest.jsonl`.

| # | Title / file | Source | Pages | Fetched | URL |
|---|---|---|---|---|---|
| 1 | content/manuals/build/_index.md | docker-docs | 1 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/_index.md |
| 2 | content/manuals/build/bake/_index.md | docker-docs | 1 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/bake/_index.md |
| 3 | content/manuals/build/bake/compose-file.md | docker-docs | 3 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/bake/compose-file.md |
| 4 | content/manuals/build/bake/contexts.md | docker-docs | 1 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/bake/contexts.md |
| 5 | content/manuals/build/bake/expressions.md | docker-docs | 1 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/bake/expressions.md |
| 6 | content/manuals/build/bake/funcs.md | docker-docs | 1 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/bake/funcs.md |
| 7 | content/manuals/build/bake/inheritance.md | docker-docs | 2 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/bake/inheritance.md |
| 8 | content/manuals/build/bake/introduction.md | docker-docs | 1 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/bake/introduction.md |
| 9 | content/manuals/build/bake/matrices.md | docker-docs | 1 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/bake/matrices.md |
| 10 | content/manuals/build/bake/overrides.md | docker-docs | 4 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/bake/overrides.md |
| 11 | content/manuals/build/bake/remote-definition.md | docker-docs | 2 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/bake/remote-definition.md |
| 12 | content/manuals/build/bake/targets.md | docker-docs | 2 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/bake/targets.md |
| 13 | content/manuals/build/bake/variables.md | docker-docs | 3 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/bake/variables.md |
| 14 | content/manuals/build/builders/_index.md | docker-docs | 1 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/builders/_index.md |
| 15 | content/manuals/build/builders/drivers/_index.md | docker-docs | 2 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/builders/drivers/_index.md |
| 16 | content/manuals/build/builders/drivers/cloud.md | docker-docs |  | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/builders/drivers/cloud.md |
| 17 | content/manuals/build/builders/drivers/docker-container.md | docker-docs | 3 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/builders/drivers/docker-container.md |
| 18 | content/manuals/build/builders/drivers/docker.md | docker-docs |  | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/builders/drivers/docker.md |
| 19 | content/manuals/build/builders/drivers/kubernetes.md | docker-docs | 7 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/builders/drivers/kubernetes.md |
| 20 | content/manuals/build/builders/drivers/remote.md | docker-docs | 3 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/builders/drivers/remote.md |
| 21 | content/manuals/build/builders/manage.md | docker-docs | 2 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/builders/manage.md |
| 22 | content/manuals/build/building/_index.md | docker-docs |  | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/building/_index.md |
| 23 | content/manuals/build/building/base-images.md | docker-docs | 2 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/building/base-images.md |
| 24 | content/manuals/build/building/best-practices.md | docker-docs | 11 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/building/best-practices.md |
| 25 | content/manuals/build/building/cdi.md | docker-docs | 6 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/building/cdi.md |
| 26 | content/manuals/build/building/export.md | docker-docs | 1 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/building/export.md |
| 27 | content/manuals/build/building/multi-platform.md | docker-docs | 6 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/building/multi-platform.md |
| 28 | content/manuals/build/building/multi-stage.md | docker-docs | 2 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/building/multi-stage.md |
| 29 | content/manuals/build/building/registry-auth.md | docker-docs | 1 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/building/registry-auth.md |
| 30 | content/manuals/build/building/secrets.md | docker-docs | 3 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/building/secrets.md |
| 31 | content/manuals/build/building/variables.md | docker-docs | 10 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/building/variables.md |
| 32 | content/manuals/build/buildkit/_index.md | docker-docs | 3 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/buildkit/_index.md |
| 33 | content/manuals/build/buildkit/configure.md | docker-docs | 4 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/buildkit/configure.md |
| 34 | content/manuals/build/buildkit/dockerfile-release-notes.md | docker-docs |  | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/buildkit/dockerfile-release-notes.md |
| 35 | content/manuals/build/buildkit/frontend.md | docker-docs | 2 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/buildkit/frontend.md |
| 36 | content/manuals/build/cache/_index.md | docker-docs | 1 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/cache/_index.md |
| 37 | content/manuals/build/cache/backends/_index.md | docker-docs | 3 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/cache/backends/_index.md |
| 38 | content/manuals/build/cache/backends/azblob.md | docker-docs | 1 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/cache/backends/azblob.md |
| 39 | content/manuals/build/cache/backends/gha.md | docker-docs | 3 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/cache/backends/gha.md |
| 40 | content/manuals/build/cache/backends/inline.md | docker-docs | 1 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/cache/backends/inline.md |
| 41 | content/manuals/build/cache/backends/local.md | docker-docs | 2 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/cache/backends/local.md |
| 42 | content/manuals/build/cache/backends/registry.md | docker-docs | 2 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/cache/backends/registry.md |
| 43 | content/manuals/build/cache/backends/s3.md | docker-docs | 1 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/cache/backends/s3.md |
| 44 | content/manuals/build/cache/garbage-collection.md | docker-docs | 4 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/cache/garbage-collection.md |
| 45 | content/manuals/build/cache/invalidation.md | docker-docs | 1 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/cache/invalidation.md |
| 46 | content/manuals/build/cache/optimize.md | docker-docs | 5 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/cache/optimize.md |
| 47 | content/manuals/build/checks.md | docker-docs | 3 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/checks.md |
| 48 | content/manuals/build/ci/_index.md | docker-docs | 1 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/ci/_index.md |
| 49 | content/manuals/build/ci/github-actions/_index.md | docker-docs | 3 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/ci/github-actions/_index.md |
| 50 | content/manuals/build/ci/github-actions/annotations.md | docker-docs | 2 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/ci/github-actions/annotations.md |
| 51 | content/manuals/build/ci/github-actions/attestations.md | docker-docs | 2 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/ci/github-actions/attestations.md |
| 52 | content/manuals/build/ci/github-actions/bake-workflow.md | docker-docs | 2 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/ci/github-actions/bake-workflow.md |
| 53 | content/manuals/build/ci/github-actions/build-summary.md | docker-docs | 1 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/ci/github-actions/build-summary.md |
| 54 | content/manuals/build/ci/github-actions/build-workflow.md | docker-docs | 2 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/ci/github-actions/build-workflow.md |
| 55 | content/manuals/build/ci/github-actions/cache.md | docker-docs | 4 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/ci/github-actions/cache.md |
| 56 | content/manuals/build/ci/github-actions/checks.md | docker-docs | 1 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/ci/github-actions/checks.md |
| 57 | content/manuals/build/ci/github-actions/configure-builder.md | docker-docs | 4 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/ci/github-actions/configure-builder.md |
| 58 | content/manuals/build/ci/github-actions/copy-image-registries.md | docker-docs | 1 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/ci/github-actions/copy-image-registries.md |
| 59 | content/manuals/build/ci/github-actions/export-docker.md | docker-docs |  | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/ci/github-actions/export-docker.md |
| 60 | content/manuals/build/ci/github-actions/github-builder-architecture/index.md | docker-docs | 3 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/ci/github-actions/github-builder-architecture/index.md |
| 61 | content/manuals/build/ci/github-actions/local-registry.md | docker-docs |  | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/ci/github-actions/local-registry.md |
| 62 | content/manuals/build/ci/github-actions/manage-tags-labels.md | docker-docs | 1 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/ci/github-actions/manage-tags-labels.md |
| 63 | content/manuals/build/ci/github-actions/multi-platform.md | docker-docs | 2 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/ci/github-actions/multi-platform.md |
| 64 | content/manuals/build/ci/github-actions/named-contexts.md | docker-docs | 1 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/ci/github-actions/named-contexts.md |
| 65 | content/manuals/build/ci/github-actions/push-multi-registries.md | docker-docs | 1 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/ci/github-actions/push-multi-registries.md |
| 66 | content/manuals/build/ci/github-actions/reproducible-builds.md | docker-docs | 1 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/ci/github-actions/reproducible-builds.md |
| 67 | content/manuals/build/ci/github-actions/secrets.md | docker-docs | 4 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/ci/github-actions/secrets.md |
| 68 | content/manuals/build/ci/github-actions/share-image-jobs.md | docker-docs | 1 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/ci/github-actions/share-image-jobs.md |
| 69 | content/manuals/build/ci/github-actions/test-before-push.md | docker-docs | 1 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/ci/github-actions/test-before-push.md |
| 70 | content/manuals/build/ci/github-actions/update-dockerhub-desc.md | docker-docs |  | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/ci/github-actions/update-dockerhub-desc.md |
| 71 | content/manuals/build/concepts/_index.md | docker-docs |  | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/concepts/_index.md |
| 72 | content/manuals/build/concepts/context.md | docker-docs | 9 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/concepts/context.md |
| 73 | content/manuals/build/concepts/dockerfile.md | docker-docs | 4 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/concepts/dockerfile.md |
| 74 | content/manuals/build/concepts/overview.md | docker-docs | 1 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/concepts/overview.md |
| 75 | content/manuals/build/debug/_index.md | docker-docs |  | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/debug/_index.md |
| 76 | content/manuals/build/debug/opentelemetry.md | docker-docs |  | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/debug/opentelemetry.md |
| 77 | content/manuals/build/exporters/_index.md | docker-docs | 4 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/exporters/_index.md |
| 78 | content/manuals/build/exporters/image-registry.md | docker-docs | 2 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/exporters/image-registry.md |
| 79 | content/manuals/build/exporters/local-tar.md | docker-docs | 1 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/exporters/local-tar.md |
| 80 | content/manuals/build/exporters/oci-docker.md | docker-docs | 1 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/exporters/oci-docker.md |
| 81 | content/manuals/build/metadata/_index.md | docker-docs |  | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/metadata/_index.md |
| 82 | content/manuals/build/metadata/annotations.md | docker-docs | 3 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/metadata/annotations.md |
| 83 | content/manuals/build/metadata/attestations/_index.md | docker-docs | 3 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/metadata/attestations/_index.md |
| 84 | content/manuals/build/metadata/attestations/sbom.md | docker-docs | 4 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/metadata/attestations/sbom.md |
| 85 | content/manuals/build/metadata/attestations/slsa-provenance.md | docker-docs | 4 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/metadata/attestations/slsa-provenance.md |
| 86 | content/manuals/build/policies/_index.md | docker-docs | 2 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/policies/_index.md |
| 87 | content/manuals/build/policies/built-ins.md | docker-docs | 2 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/policies/built-ins.md |
| 88 | content/manuals/build/policies/debugging.md | docker-docs | 2 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/policies/debugging.md |
| 89 | content/manuals/build/policies/examples.md | docker-docs | 5 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/policies/examples.md |
| 90 | content/manuals/build/policies/inputs.md | docker-docs | 5 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/policies/inputs.md |
| 91 | content/manuals/build/policies/intro.md | docker-docs | 3 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/policies/intro.md |
| 92 | content/manuals/build/policies/testing.md | docker-docs | 1 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/policies/testing.md |
| 93 | content/manuals/build/policies/usage.md | docker-docs | 6 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/policies/usage.md |
| 94 | content/manuals/build/policies/validate-git.md | docker-docs | 3 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/policies/validate-git.md |
| 95 | content/manuals/build/policies/validate-images.md | docker-docs | 4 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/policies/validate-images.md |
| 96 | content/manuals/build/release-notes.md | docker-docs |  | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/build/release-notes.md |
| 97 | content/manuals/compose/_index.md | docker-docs | 1 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/compose/_index.md |
| 98 | content/manuals/compose/bridge/_index.md | docker-docs | 1 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/compose/bridge/_index.md |
| 99 | content/manuals/compose/bridge/customize.md | docker-docs | 4 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/compose/bridge/customize.md |
| 100 | content/manuals/compose/bridge/usage.md | docker-docs | 2 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/compose/bridge/usage.md |
| 101 | content/manuals/compose/bridge/use-model-runner.md | docker-docs | 1 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/compose/bridge/use-model-runner.md |
| 102 | content/manuals/compose/compose-sdk.md | docker-docs | 3 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/compose/compose-sdk.md |
| 103 | content/manuals/compose/gettingstarted.md | docker-docs | 6 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/compose/gettingstarted.md |
| 104 | content/manuals/compose/how-tos/_index.md | docker-docs |  | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/compose/how-tos/_index.md |
| 105 | content/manuals/compose/how-tos/dependent-images.md | docker-docs | 1 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/compose/how-tos/dependent-images.md |
| 106 | content/manuals/compose/how-tos/environment-variables/_index.md | docker-docs |  | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/compose/how-tos/environment-variables/_index.md |
| 107 | content/manuals/compose/how-tos/environment-variables/best-practices.md | docker-docs |  | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/compose/how-tos/environment-variables/best-practices.md |
| 108 | content/manuals/compose/how-tos/environment-variables/envvars-precedence.md | docker-docs | 3 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/compose/how-tos/environment-variables/envvars-precedence.md |
| 109 | content/manuals/compose/how-tos/environment-variables/envvars.md | docker-docs | 3 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/compose/how-tos/environment-variables/envvars.md |
| 110 | content/manuals/compose/how-tos/environment-variables/set-environment-variables.md | docker-docs | 2 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/compose/how-tos/environment-variables/set-environment-variables.md |
| 111 | content/manuals/compose/how-tos/environment-variables/variable-interpolation.md | docker-docs | 4 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/compose/how-tos/environment-variables/variable-interpolation.md |
| 112 | content/manuals/compose/how-tos/file-watch.md | docker-docs | 3 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/compose/how-tos/file-watch.md |
| 113 | content/manuals/compose/how-tos/gpu-support.md | docker-docs | 2 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/compose/how-tos/gpu-support.md |
| 114 | content/manuals/compose/how-tos/init-containers.md | docker-docs | 2 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/compose/how-tos/init-containers.md |
| 115 | content/manuals/compose/how-tos/jobs.md | docker-docs | 5 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/compose/how-tos/jobs.md |
| 116 | content/manuals/compose/how-tos/lifecycle.md | docker-docs | 1 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/compose/how-tos/lifecycle.md |
| 117 | content/manuals/compose/how-tos/models-and-compose.md | docker-docs | 3 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/compose/how-tos/models-and-compose.md |
| 118 | content/manuals/compose/how-tos/multiple-compose-files/_index.md | docker-docs | 1 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/compose/how-tos/multiple-compose-files/_index.md |
| 119 | content/manuals/compose/how-tos/multiple-compose-files/extends.md | docker-docs | 2 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/compose/how-tos/multiple-compose-files/extends.md |
| 120 | content/manuals/compose/how-tos/multiple-compose-files/include.md | docker-docs | 1 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/compose/how-tos/multiple-compose-files/include.md |
| 121 | content/manuals/compose/how-tos/multiple-compose-files/merge.md | docker-docs | 3 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/compose/how-tos/multiple-compose-files/merge.md |
| 122 | content/manuals/compose/how-tos/networking.md | docker-docs | 5 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/compose/how-tos/networking.md |
| 123 | content/manuals/compose/how-tos/oci-artifact.md | docker-docs | 2 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/compose/how-tos/oci-artifact.md |
| 124 | content/manuals/compose/how-tos/production.md | docker-docs | 1 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/compose/how-tos/production.md |
| 125 | content/manuals/compose/how-tos/profiles.md | docker-docs | 2 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/compose/how-tos/profiles.md |
| 126 | content/manuals/compose/how-tos/project-name.md | docker-docs | 1 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/compose/how-tos/project-name.md |
| 127 | content/manuals/compose/how-tos/provider-services.md | docker-docs | 2 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/compose/how-tos/provider-services.md |
| 128 | content/manuals/compose/how-tos/startup-order.md | docker-docs | 1 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/compose/how-tos/startup-order.md |
| 129 | content/manuals/compose/how-tos/use-secrets.md | docker-docs | 1 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/compose/how-tos/use-secrets.md |
| 130 | content/manuals/compose/install/_index.md | docker-docs | 1 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/compose/install/_index.md |
| 131 | content/manuals/compose/install/linux.md | docker-docs | 1 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/compose/install/linux.md |
| 132 | content/manuals/compose/install/standalone.md | docker-docs | 1 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/compose/install/standalone.md |
| 133 | content/manuals/compose/install/uninstall.md | docker-docs | 1 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/compose/install/uninstall.md |
| 134 | content/manuals/compose/intro/_index.md | docker-docs |  | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/compose/intro/_index.md |
| 135 | content/manuals/compose/intro/compose-application-model.md | docker-docs | 3 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/compose/intro/compose-application-model.md |
| 136 | content/manuals/compose/intro/features-uses.md | docker-docs | 1 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/compose/intro/features-uses.md |
| 137 | content/manuals/compose/intro/history.md | docker-docs | 1 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/compose/intro/history.md |
| 138 | content/manuals/compose/release-notes.md | docker-docs |  | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/compose/release-notes.md |
| 139 | content/manuals/compose/support-and-feedback/_index.md | docker-docs |  | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/compose/support-and-feedback/_index.md |
| 140 | content/manuals/compose/support-and-feedback/faq.md | docker-docs | 2 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/compose/support-and-feedback/faq.md |
| 141 | content/manuals/compose/support-and-feedback/feedback.md | docker-docs |  | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/compose/support-and-feedback/feedback.md |
| 142 | content/manuals/compose/trust-model.md | docker-docs | 2 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/manuals/compose/trust-model.md |
| 143 | content/reference/_index.md | docker-docs |  | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/reference/_index.md |
| 144 | content/reference/api/ai-governance-audit-logs/_index.md | docker-docs |  | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/reference/api/ai-governance-audit-logs/_index.md |
| 145 | content/reference/api/ai-governance/_index.md | docker-docs |  | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/reference/api/ai-governance/_index.md |
| 146 | content/reference/api/dvp/_index.md | docker-docs |  | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/reference/api/dvp/_index.md |
| 147 | content/reference/api/dvp/changelog.md | docker-docs |  | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/reference/api/dvp/changelog.md |
| 148 | content/reference/api/dvp/deprecated.md | docker-docs |  | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/reference/api/dvp/deprecated.md |
| 149 | content/reference/api/engine/_index.md | docker-docs | 6 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/reference/api/engine/_index.md |
| 150 | content/reference/api/engine/latest.md | docker-docs |  | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/reference/api/engine/latest.md |
| 151 | content/reference/api/engine/sdk/_index.md | docker-docs | 3 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/reference/api/engine/sdk/_index.md |
| 152 | content/reference/api/engine/sdk/examples.md | docker-docs | 6 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/reference/api/engine/sdk/examples.md |
| 153 | content/reference/api/engine/version/_index.md | docker-docs |  | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/reference/api/engine/version/_index.md |
| 154 | content/reference/api/engine/version/v1.40.md | docker-docs |  | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/reference/api/engine/version/v1.40.md |
| 155 | content/reference/api/engine/version/v1.41.md | docker-docs |  | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/reference/api/engine/version/v1.41.md |
| 156 | content/reference/api/engine/version/v1.42.md | docker-docs |  | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/reference/api/engine/version/v1.42.md |
| 157 | content/reference/api/engine/version/v1.43.md | docker-docs |  | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/reference/api/engine/version/v1.43.md |
| 158 | content/reference/api/engine/version/v1.44.md | docker-docs |  | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/reference/api/engine/version/v1.44.md |
| 159 | content/reference/api/engine/version/v1.45.md | docker-docs |  | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/reference/api/engine/version/v1.45.md |
| 160 | content/reference/api/engine/version/v1.46.md | docker-docs |  | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/reference/api/engine/version/v1.46.md |
| 161 | content/reference/api/engine/version/v1.47.md | docker-docs |  | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/reference/api/engine/version/v1.47.md |
| 162 | content/reference/api/engine/version/v1.48.md | docker-docs |  | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/reference/api/engine/version/v1.48.md |
| 163 | content/reference/api/engine/version/v1.49.md | docker-docs |  | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/reference/api/engine/version/v1.49.md |
| 164 | content/reference/api/engine/version/v1.50.md | docker-docs |  | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/reference/api/engine/version/v1.50.md |
| 165 | content/reference/api/engine/version/v1.51.md | docker-docs |  | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/reference/api/engine/version/v1.51.md |
| 166 | content/reference/api/engine/version/v1.52.md | docker-docs |  | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/reference/api/engine/version/v1.52.md |
| 167 | content/reference/api/engine/version/v1.53.md | docker-docs |  | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/reference/api/engine/version/v1.53.md |
| 168 | content/reference/api/engine/version/v1.54.md | docker-docs |  | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/reference/api/engine/version/v1.54.md |
| 169 | content/reference/api/engine/version/v1.55.md | docker-docs |  | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/reference/api/engine/version/v1.55.md |
| 170 | content/reference/api/engine/version/v1.56.md | docker-docs |  | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/reference/api/engine/version/v1.56.md |
| 171 | content/reference/api/engine/version/v1.57.md | docker-docs |  | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/reference/api/engine/version/v1.57.md |
| 172 | content/reference/api/extensions-sdk/BackendV0.md | docker-docs | 2 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/reference/api/extensions-sdk/BackendV0.md |
| 173 | content/reference/api/extensions-sdk/DesktopUI.md | docker-docs |  | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/reference/api/extensions-sdk/DesktopUI.md |
| 174 | content/reference/api/extensions-sdk/Dialog.md | docker-docs |  | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/reference/api/extensions-sdk/Dialog.md |
| 175 | content/reference/api/extensions-sdk/Docker.md | docker-docs | 1 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/reference/api/extensions-sdk/Docker.md |
| 176 | content/reference/api/extensions-sdk/DockerCommand.md | docker-docs |  | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/reference/api/extensions-sdk/DockerCommand.md |
| 177 | content/reference/api/extensions-sdk/DockerDesktopClient.md | docker-docs | 5 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/reference/api/extensions-sdk/DockerDesktopClient.md |
| 178 | content/reference/api/extensions-sdk/Exec.md | docker-docs |  | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/reference/api/extensions-sdk/Exec.md |
| 179 | content/reference/api/extensions-sdk/ExecOptions.md | docker-docs |  | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/reference/api/extensions-sdk/ExecOptions.md |
| 180 | content/reference/api/extensions-sdk/ExecProcess.md | docker-docs |  | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/reference/api/extensions-sdk/ExecProcess.md |
| 181 | content/reference/api/extensions-sdk/ExecResult.md | docker-docs | 1 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/reference/api/extensions-sdk/ExecResult.md |
| 182 | content/reference/api/extensions-sdk/ExecResultV0.md | docker-docs |  | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/reference/api/extensions-sdk/ExecResultV0.md |
| 183 | content/reference/api/extensions-sdk/ExecStreamOptions.md | docker-docs | 1 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/reference/api/extensions-sdk/ExecStreamOptions.md |
| 184 | content/reference/api/extensions-sdk/Extension.md | docker-docs |  | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/reference/api/extensions-sdk/Extension.md |
| 185 | content/reference/api/extensions-sdk/ExtensionCli.md | docker-docs |  | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/reference/api/extensions-sdk/ExtensionCli.md |
| 186 | content/reference/api/extensions-sdk/ExtensionHost.md | docker-docs | 1 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/reference/api/extensions-sdk/ExtensionHost.md |
| 187 | content/reference/api/extensions-sdk/ExtensionVM.md | docker-docs | 1 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/reference/api/extensions-sdk/ExtensionVM.md |
| 188 | content/reference/api/extensions-sdk/Host.md | docker-docs |  | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/reference/api/extensions-sdk/Host.md |
| 189 | content/reference/api/extensions-sdk/HttpService.md | docker-docs | 1 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/reference/api/extensions-sdk/HttpService.md |
| 190 | content/reference/api/extensions-sdk/NavigationIntents.md | docker-docs | 2 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/reference/api/extensions-sdk/NavigationIntents.md |
| 191 | content/reference/api/extensions-sdk/OpenDialogResult.md | docker-docs |  | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/reference/api/extensions-sdk/OpenDialogResult.md |
| 192 | content/reference/api/extensions-sdk/RawExecResult.md | docker-docs |  | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/reference/api/extensions-sdk/RawExecResult.md |
| 193 | content/reference/api/extensions-sdk/RequestConfig.md | docker-docs |  | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/reference/api/extensions-sdk/RequestConfig.md |
| 194 | content/reference/api/extensions-sdk/RequestConfigV0.md | docker-docs |  | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/reference/api/extensions-sdk/RequestConfigV0.md |
| 195 | content/reference/api/extensions-sdk/ServiceError.md | docker-docs |  | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/reference/api/extensions-sdk/ServiceError.md |
| 196 | content/reference/api/extensions-sdk/SpawnOptions.md | docker-docs |  | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/reference/api/extensions-sdk/SpawnOptions.md |
| 197 | content/reference/api/extensions-sdk/Toast.md | docker-docs |  | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/reference/api/extensions-sdk/Toast.md |
| 198 | content/reference/api/extensions-sdk/_index.md | docker-docs |  | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/reference/api/extensions-sdk/_index.md |
| 199 | content/reference/api/hub/_index.md | docker-docs |  | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/reference/api/hub/_index.md |
| 200 | content/reference/api/hub/changelog.md | docker-docs | 1 | 2026-11-23 | https://github.com/docker/docs/blob/HEAD/content/reference/api/hub/changelog.md |
<!-- generated:end -->

## Known gaps

- The start corpus contains 236 files and 484 measured pages covering BuildKit, Docker Compose, Dockerfile reference, and storage guides. The full 3,000-page target will additionally encompass the Docker Engine CLI reference, daemon architecture guides, and Docker release notes.
- Deduplication analysis: Verified `data/manifest.jsonl` across all 236 entries; found 0 duplicate SHA256 checksums across downloaded files.
