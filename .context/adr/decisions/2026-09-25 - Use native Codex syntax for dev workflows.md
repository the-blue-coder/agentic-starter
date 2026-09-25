---
type: decision
status: accepted
date: 2026-09-25
tags: [tooling, codex, agent-workflows]
affects: [[Codex skills]]
---

## Context

Shared `.context/commands/` docs used slash command syntax in workflow recommendations, but Codex invokes repository workflows through dollar-prefixed skills. This made `/dev` and `/implement` recommendations fail to match the Codex interface.

## Decision

Document `$dev` and `$implement` for Codex invocation while preserving `/dev` and `/implement` for other command environments.

## Why not something else

- **Use slash syntax in all environments**: rejected because Codex exposes these workflows as named skills invoked with `$`.
- **Replace slash syntax globally with dollar syntax**: rejected because other command environments continue to invoke `/dev` and `/implement`.

## Consequences

- Positive: cross-tool instructions identify the correct invocation for Codex and other environments.
- Negative / risk: shared workflow references must retain both forms where users are told what to run.
