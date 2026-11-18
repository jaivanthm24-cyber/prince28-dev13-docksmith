# Real user questions: DockSmith

Written the way my user types them.

**User:** DevOps intern at a Chennai logistics startup whose Python image is 1.8 GB, rebuilds take 9 minutes and the container runs as root.

These 10 questions become my first evaluation set in Week 3. Question 6 is not answerable from my documents: the product must say "I don't know".

| # | Question | Type | Where the answer is (document, page) | More than one page? |
|---|---|---|---|---|
| 1 | What is a multi-stage build? | simple | Docker Docs — Building images: Multi-stage builds | No |
| 2 | What is the difference between CMD and ENTRYPOINT? | simple | Dockerfile reference — CMD and ENTRYPOINT instructions | Yes |
| 3 | Is the version key still needed in compose.yaml? | simple | Compose file reference — Version and name top-level attribute | No |
| 4 | Our FastAPI image is 1.8 GB on python:3.12, rebuilds take 9 minutes after every code change and it runs as root. Rewrite the Dockerfile and explain each change with the expected size and build time. | multi-step (several pages) | Docker Docs — Best practices for Dockerfiles, Optimize build cache, and General security guidelines | Yes |
| 5 | Compare bind mounts, named volumes and tmpfs mounts. | comparison | Docker Docs — Storage overview: Manage data in Docker | Yes |
| 6 | Why did our production container restart at 2 a.m.? | multi-step (several pages) | Docker Docs — Command-line reference: docker inspect (.State.ExitCode and .State.OOMKilled) | Yes |
| 7 | What is our company AWS cloud bill for our ECS clusters this month? | unanswerable: must reply "I don't know" | none: not in Docker documentation | - |
| 8 | Why is the MAINTAINER instruction deprecated in Dockerfiles and what should be used instead? | simple | Dockerfile reference — MAINTAINER (deprecated) and LABEL instructions | No |
| 9 | How does BuildKit cache mount (--mount=type=cache) speed up package installations compared to standard builds? | simple | Docker Docs — BuildKit cache mounts: Optimize cache | No |
| 10 | What is the difference between running Docker in rootless mode versus declaring USER inside a Dockerfile? | comparison | Docker Docs — Run the Docker daemon as a non-root user (Rootless mode) and Dockerfile USER instruction | Yes |

## Source references

1. Docker Documentation: https://docs.docker.com/
2. Docker Docs GitHub Repository: https://github.com/docker/docs
3. Compose Specification: https://github.com/compose-spec/compose-spec
4. Dockerfile Reference: https://docs.docker.com/reference/dockerfile/
5. Multi-stage Builds: https://docs.docker.com/build/building/multi-stage/
6. Docker Cache Optimization: https://docs.docker.com/build/cache/optimize/
7. Manage Data in Docker: https://docs.docker.com/storage/
8. Compose File Version and Name: https://docs.docker.com/compose/compose-file/04-version-and-name/
9. Docker Engine Security: https://docs.docker.com/engine/security/

**Note:** These references identify the relevant Docker documents and sections. The actual answers, linter checks, and optimizations must be verified with a real build, not inferred from generic web advice.
