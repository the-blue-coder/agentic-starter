---
type: decision
status: proposed
date: 2026-09-27
tags: [workflow, spec, process]
affects:
  - '[[spec-workflow]]'
---

# Require complete framing before feature specs

## Context

Feature specs depend on a reliable project identity, product perimeter, technical architecture, and (for UI projects) design tokens. Previously, `/spec` could be run at any time, so it could create feature plans before those shared constraints were documented. Tool-specific guidance also needs to produce the same readiness behavior across Codex, Claude Code, and OpenCode.

## Decision

Make `/spec` stop before feature planning unless shared initialization, the project PRD, and architecture are complete, with the design system also complete for projects whose architecture declares a user-facing UI.

## Why not something else

- **Keep framing as a recommendation:** rejected because an agent could still create a spec before the project constraints were established.
- **Let `/spec` fill missing framing while planning a feature:** rejected because a feature request should not silently make project-wide product or architecture decisions.
- **Require `/design-system` for every project:** rejected because a backend-only project has no UI tokens or contrast audit to establish.

## Consequences

- Positive: every feature spec starts from the same documented project and product constraints.
- Positive: an explicit `Frontend` value distinguishes UI projects from backend-only projects across tools.
- Negative / risk: existing projects must complete shared initialization and product framing before using `/spec`, even if their codebase already has an architecture document.
- Generates: `/spec`, `/status`, the session entrypoint, and README describe and enforce the same readiness gate.
