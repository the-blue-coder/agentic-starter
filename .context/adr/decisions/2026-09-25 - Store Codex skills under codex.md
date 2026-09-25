---
type: decision
status: proposed
date: 2026-09-25
tags: [tooling, codex, agent-workflows]
supersedes: [[2026-09-25 - Use agents directory for Codex skills]]
affects: [[Codex skills]]
---

## Context

The accepted setup placed project skills in `.agents/skills/` after an earlier `.codex/skills/` test failed. That failure was caused by skill metadata encoding, not directory discovery. With valid metadata, `codex debug prompt-input` lists skills from both roots, confirming `.codex/skills/` is discoverable.

## Decision

Store repository Codex skills in `.codex/skills/` alongside Codex configuration and agents.

## Why not something else

- **Keep skills in `.agents/skills/`**: rejected because `.codex/skills/` is discoverable in the current Codex CLI and keeping Codex files together better matches the project layout.
- **Duplicate skills in both directories**: rejected because it creates duplicate entries and two copies to maintain.

## Consequences

- Positive: Codex-specific files stay consolidated under `.codex/` and skills remain discoverable.
- Negative / risk: projects or tools that only scan `.agents/skills/` will not discover these skills.
- Generates: command maintenance instructions and security-review references must use `.codex/skills/`.
