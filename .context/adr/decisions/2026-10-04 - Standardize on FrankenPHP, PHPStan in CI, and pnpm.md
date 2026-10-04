---
type: decision
status: accepted
date: 2026-10-04
tags: [php, frankenphp, phpstan, pnpm, ci, stacks]
affects: [[Stack recipes]]
---

## Context

The Symfony stack recipes described the backend as PHP-FPM behind an inner nginx (and, for the Twig recipe, Apache), while the reference project already runs on FrankenPHP. Static analysis was only a hint in the review commands: the recipes did not say how to install PHPStan or run it in CI. And JavaScript tooling was only partly pinned to pnpm.

## Decision

- **FrankenPHP is the PHP runtime** in both Symfony recipes: a multi-stage `Dockerfile` on `dunglas/frankenphp`, server config in `frankenphp/` (`Caddyfile`, `conf.d/`, `docker-entrypoint.sh`), no PHP-FPM, no inner nginx or supervisord. A host nginx still proxies HTTP to the container's published port. Convention files record the long-lived-process rules (`symfony.md`, `performance/symfony.md`).
- **PHPStan runs at level 8 locally and in the GitHub workflow**, modeled on the reference backend: Symfony and Doctrine extensions, `phpstan.dist.neon` plus a committed baseline, a `phpstan` composer script, run inside the dev container (`docker compose exec backend composer phpstan`). The deploy workflow gets a `quality` job (build the dev image, start the backend, run PHPStan) that the deploy job depends on. Suppressing errors or lowering the level needs explicit user approval.
- **pnpm is the only JavaScript package manager**: stated in `global.md` for every JS dependency and script, with a committed `pnpm-lock.yaml` and `pnpm install --frozen-lockfile` in CI and Docker builds.

## Why not something else

- **Keep PHP-FPM and nginx in the container**: rejected because the reference project uses FrankenPHP and the extra processes add configuration without a benefit here.
- **Run PHPStan on the CI runner's own PHP**: rejected because it would diverge from the container's PHP version and extensions, and the Symfony extension needs the container's compiled dev cache.
- **Run PHPStan only locally**: rejected because a local check can be skipped; the deploy job must depend on it.
- **Allow npm or yarn per project**: rejected because mixed package managers produce competing lockfiles and inconsistent installs.

## Consequences

- Positive: one documented runtime, a deploy blocked by static-analysis failures, and one JS toolchain.
- Negative / risk: existing projects on PHP-FPM must migrate their Dockerfile and entrypoint themselves; FrankenPHP worker mode needs stateless services; the CI job adds a few minutes per deploy.
- Generates: edits to both stack recipes, `php.md`, `symfony.md`, `performance/symfony.md`, `global.md`, and the example `.github/workflows/deploy.yml`.
