---
type: decision
status: superseded
date: 2026-09-27
tags: [workflow, design, tooling]
---

# Use exported OpenDesign references for UI specs

## Context

OpenDesign runs as a separate browser workspace, while implementation may happen through Codex, Claude Code, OpenCode, or another local coding agent. Direct MCP access would require each local agent to have a compatible installation and a live connection to the hosted OpenDesign instance.

## Decision

For each UI spec, export the reviewed OpenDesign project and store its files under `.context/feature-specs/design/<NNN-slug>/` so the local coding agent can read the same versioned reference from the spec branch.

## Why not something else

- **Agent-specific MCP setup as the required path**: rejected because local clients differ in configuration and a hosted OpenDesign instance may not be reachable through their local MCP setup.
- **Keeping the design only in the hosted workspace**: rejected because the spec branch would not contain a stable design reference for implementation or review.

## Consequences

- Positive: the same design reference works with any local coding agent and travels with its spec PR.
- Negative / risk: the user must export and extract the design files before `/spec` can finish its UI handoff.
- Negative / risk: generated prototype files can add size to a PR; keep only the relevant entry file and assets.
