---
type: decision
status: proposed
date: 2026-10-04
tags: [tooling, agent-workflows]
supersedes: [[2026-09-25 - Use native Codex syntax for dev workflows]]
affects: [[Codex skills]]
---

## Context

The starter mirrored every command and subagent into `.codex/` (skills, agents, config) and documented dollar-prefixed Codex invocations next to slash commands. The project owner now works only with Claude Code and OpenCode, so the Codex mirror is maintenance cost with no user.

## Decision

Remove `.codex/` and all Codex-specific documentation; commands are invoked as `/<command>` and mirrored only to `.claude/` and `.opencode/`.

## Why not something else

- **Keep `.codex/` frozen**: rejected because it would drift from the canonical `.context/commands/` and mislead users.
- **Keep dual `$`/`/` syntax in docs**: rejected because it adds noise for a tool nobody uses.

## Consequences

- Positive: fewer files to mirror, simpler command documentation.
- Negative / risk: Codex users must restore `.codex/` from git history; earlier Codex ADRs stay as historical records.
