---
type: decision
status: superseded
date: 2026-09-25
tags: [tooling, codex, agent-workflows]
supersedes: [[2026-09-25 - Keep Codex workflows under codex config]]
---

## Context

The Codex command skills were moved into `.codex/skills/` to keep Codex files under one directory. After restart, this environment did not expose those command skills for automatic use. The documented repository discovery path for local Codex skills is `.agents/skills/`.

## Decision

Store repository Codex skills in `.agents/skills/`, while keeping Codex configuration and custom agents in `.codex/`.

## Why not something else

- **Store all Codex files under `.codex/`**: rejected because the current assistant environment did not make the project command skills available from `.codex/skills/` after restart.
- **Use the older Team Config skill path**: rejected for this project because it did not provide the expected skill availability in the user's current workflow.

## Consequences

- Positive: repository skills use the documented standalone discovery path and appear as project skills.
- Negative / risk: Codex files are split between `.codex/` and `.agents/` at the repository root.
