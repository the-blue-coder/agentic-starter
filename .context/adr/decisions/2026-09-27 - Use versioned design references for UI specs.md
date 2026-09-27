---
type: decision
status: superseded
date: 2026-09-27
tags: [workflow, design, tooling]
supersedes: [[2026-09-27 - Use exported OpenDesign references for UI specs]]
---

# Use versioned design references for UI specs

## Context

Projects may use different design tools, existing design sources, or no hosted workspace. The local implementation agent may be Codex, Claude Code, OpenCode, or another tool, and should not need live access or provider-specific integrations to inspect the approved design.

## Decision

For each UI spec, store the reviewed, relevant design references and assets under `.context/feature-specs/design/<NNN-slug>/` so they travel with the spec branch. The design workspace URL is optional. OpenDesign is one possible design tool, not a workflow requirement.

## Why not something else

- **Require one design provider or agent-specific MCP setup**: rejected because projects and local clients use different tools and configurations.
- **Keep the design only in a hosted workspace**: rejected because the spec branch would not contain a stable reference for implementation or review.

## Consequences

- Positive: the same versioned reference works with any local coding agent and travels with its spec PR.
- Positive: projects can use their preferred design tool or references they already have.
- Negative / risk: the user must add relevant local references before implementation, unless they explicitly approve a prose-only design description.
- Negative / risk: exported files and assets can add size to a PR; keep only relevant references and assets.
