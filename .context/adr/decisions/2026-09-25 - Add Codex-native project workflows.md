---
type: decision
status: superseded
date: 2026-09-25
tags: [tooling, codex, agent-workflows]
---

## Context

The starter has Claude Code and opencode agents and command wrappers, but no Codex project setup. Codex uses TOML agent definitions under `.codex/agents/` and reusable skills under `.agents/skills/`, with `.context/commands/` remaining the canonical workflow source.

## Decision

Add Codex-native agents and thin command skills that delegate to `.context/commands/`, and document Codex in the starter workflow entrypoint.

## Why not something else

- **Copy the Claude directory structure unchanged**: rejected because Claude Markdown agents and command wrappers are not Codex's native formats and would not be discovered as Codex agents or skills.
- **Move command logic into Codex-specific files**: rejected because it would duplicate the canonical workflows in `.context/commands/` and allow the tools to drift.

## Consequences

- Positive: Codex can discover the project agents and named skills using its native formats while workflow logic stays shared.
- Negative / risk: command changes must keep their thin skills in `.agents/skills/` synchronized; this requirement is documented in the starter workflow entrypoint.
- Generates: future agent additions or changes must be mirrored in `.codex/agents/` alongside the other supported tools.
