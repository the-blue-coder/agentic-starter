# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
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
- Add conditional reference-product framing to the PRD for replacement, competitor, and benchmark projects.
- Clarify Symfony domain entity, repository, and application-service responsibilities.
- Keep the starter stack-agnostic; retain the previous Symfony + Next.js + Contabo setup only as a reference recipe under `.context/stacks/`.
