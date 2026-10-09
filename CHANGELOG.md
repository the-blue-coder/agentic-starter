# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Add `/review-performance` and a `performance-reviewer` subagent, with per-stack rules in `.context/coding-conventions/performance/`; it runs before `/review-security` in `/implement`, `/implement-queue`, `/implement-swarm`, the individual feature path, and the quick path (where it reports "Not applicable" unless the diff has a query, loop, UI rendering, dependency change, or file handling).
- Add `/update-workflow`, which brings an existing project's workflow files (`.context/`, `.claude/`, `.opencode/`, git hooks) up to the latest starter version without touching project-owned files, and migrates legacy numeric specs to UTC IDs based on each spec's first-commit date; add `Starter source:` and `Starter version:` to `.context/project-settings.md`.

- Add `html.md` (HTML best practice for all markup) and `seo.md` (rendering, URLs, metadata, crawl control, structured data, per-stack implementation), and `/review-seo` with an `seo-reviewer` subagent; it runs between `/review-performance` and `/review-security` only when flagged (`SEO:` is `yes` or `hybrid` and, for a spec, `seo: true`) and is otherwise neither launched nor mentioned.
- Add the `seo:` frontmatter flag to specs (set by `/spec`, like `ui:`) and the `SEO:` (`yes`, `no`, `hybrid`) and `SEO public scope:` settings, decided by `/init-project` for new projects and by `/update-workflow` for older ones; `/spec` and `/status` require them.
- Document FrankenPHP as the PHP runtime of both Symfony recipes, PHPStan (level 8, local and in a new `quality` job of `.github/workflows/deploy.yml` that gates the deploy), and pnpm as the only JavaScript package manager.
- Add a complete Summary section at the top of the README, and reorder its workflow section: framing first, then features, then quick fixes.

### Changed
- Drop the per-spec verification record (`.context/docs/verif/`): `/dev` now runs the test and typecheck commands and writes the `## Test map` at the end of the spec, `/review-spec-implementation` always runs them itself, and `/status` and `/update-workflow` no longer know the record; `/update-workflow` deletes the obsolete folder in existing projects.
- Lighten the TDD workflow without dropping it: the loop now works one acceptance criterion at a time (a batch of tests, one red run, one green run) instead of one test at a time; the strict scope is limited to business logic and bug fixes; the per-cycle TDD journal becomes a per-criterion `## Test map` in the verification record; pure UI, markup, styling, copy, and configuration criteria may be marked "verified manually" instead of needing a test. Superseded decision: `2026-10-04 - Apply the TDD loop across the workflow`.
- Fix the `enforce-spec-pipeline.sh` hook so a write inside `.worktrees/<spec-id>/` is not gated by that spec's own unchecked criteria; before, `/implement` could never write its first file because it marks the spec `in-progress` first.
- Fix the `enforce-spec-pipeline.sh` hook message to point to `/review-spec-implementation` instead of a non-existent `/verify`.
- Replace the `CurrentUserExtension::OWNED_RESOURCES` list with interface-based ownership scoping (`OwnedByUserInterface` + `CurrentUserOwnershipExtension` in `src/Doctrine/`): unauthenticated callers get an empty result and other users' rows return 404.
- Document the `src/` layout for Symfony API (API Platform) and Twig fullstack projects, add Gatsby coding conventions, and align the Next.js domain-module rules (import direction, barrel, shared module) with the reference projects.
- Document the Next.js domain-module pattern (`src/lib/<domain>/` with types, constants, parsers, api, server, index) in place of `services/`, `src/types/`, and per-domain constants files.
- Apply a strict red-green-refactor TDD loop to backend code, frontend logic, and bug fixes, with component and Playwright e2e tests for UI behavior and journeys; add `.context/coding-conventions/tdd.md`, a TDD journal in the verification record, and test-traceability checks in the reviews.
- Require a `## Testing` section in `.context/architecture.md`, chosen at `/architecture` time with stack-recipe defaults and enforced by the `/spec` framing gate.
- Remove Codex support (`.codex/` and `$`-prefixed skill syntax); commands are mirrored to Claude Code and OpenCode only.
- Replace per-spec pull requests with verified local target-branch handoffs for user review before the explicitly authorized commit and push.
- Add parallel spec implementation with an integrated local handoff and resumable worktree cleanup.
- Rename `/parallel-implement` to `/implement-swarm` and make it autonomous: no questions mid-run, decisions made and recorded by the agent, failed specs set aside, final decision report, never commits.
- Add `/implement-queue`, the autonomous serial counterpart: specs run one after another in worktrees, each on top of the previous verified result, then land uncommitted on the target branch.
- Allow `/dev`, `/implement`, and `/implement-swarm` to resolve dropped local spec files consistently across coding agents.

- Block feature specification until shared initialization, product framing, architecture, and the UI design system when applicable are complete.
- Separate generic shared project initialization from architecture decisions; rename the architect command to architecture and remove the standalone INIT.md guide.
- Make the per-spec UI design handoff provider-agnostic, with any design tool or local references supported.
- Use UTC timestamped IDs for new specs while keeping legacy numeric specs readable across worktrees, branches, verification records, and status reports.
- Persist UI design briefs with each spec, require reviewed visual references or explicit prose-only approval, and keep supplied active content unexecuted.
- Require evidence or user-provided direction before documenting a design system, use exact WCAG contrast values, and resolve failures at the system level or through explicit user-approved exceptions.
- Add conditional reference-product framing to `project-overview.md` for replacement, competitor, and benchmark projects.
- Fold the PRD into `project-overview.md`: `/prd` now writes Scope, Success Criteria, Constraints, and Reference Product there, `/spec` and `/status` gate on those sections, and `/update-workflow` migrates a legacy `.context/framing/prd.md`.
- Clarify Symfony domain entity, repository, and application-service responsibilities.
- Keep the starter stack-agnostic; retain the previous Symfony + Next.js + Contabo setup only as a reference recipe under `.context/stacks/`.
