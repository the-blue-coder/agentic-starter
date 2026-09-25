---
type: decision
status: superseded
date: 2026-09-25
tags: [tooling, codex, agent-workflows]
supersedes: [[2026-09-25 - Add Codex-native project workflows]]
---

## Context

The initial Codex setup put reusable command skills in `.agents/skills/`, following the standalone local skill discovery guide. The user prefers to keep Codex files together under `.codex/`. OpenAI's Team Config documentation lists repository `.codex/skills/` for shared reusable workflows, and Codex CLI 0.156.1 in this environment discovers the skills from that directory.

## Decision

Keep the Codex agents, configuration, and reusable workflow skills together under `.codex/`.

## Why not something else

- **Keep repository skills in `.agents/skills/`**: rejected because `.codex/skills/` is supported by this project's active Codex Team Config layer and avoids an extra top-level tool directory.
- **Duplicate skills in both locations**: rejected because it creates duplicate skill entries and two copies to maintain.

## Consequences

- Positive: all Codex-specific project files live under `.codex/`.
- Positive: skills remain discoverable through the Team Config layer; this was confirmed with the installed CLI's prompt-input inspection.
- Negative / risk: standalone skill discovery documentation also lists `.agents/skills/`; the repository relies on Team Config's `.codex/skills/` discovery behavior.
