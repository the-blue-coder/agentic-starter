---
type: decision
status: accepted
date: 2026-10-04
tags: [tooling, agent-workflows, parallelism]
supersedes: [[2026-09-27 - Parallel implementation batches and resumable handoff]]
affects: [[Implementation workflows]]
---

## Context

`/parallel-implement` batched independent specs but still paused for confirmations and open questions, and there was no way to run dependent specs in series unattended. The owner wants to start a multi-spec run and read one report at the end, while keeping Git history under their control.

## Decision

Replace `/parallel-implement` with `/implement-swarm` (parallel) and add `/implement-queue` (series), both autonomous under `.context/commands/autonomous-mode.md`: the agent decides open questions and records them, sets failed specs aside instead of blocking the batch, never commits or pushes, and ends with a decision report. The manifest, worktrees, patch integration, transfer, and resume machinery of the parallel ADR are kept unchanged.

## Why not something else

- **Autonomous mode flag on `/implement`**: rejected because multi-spec orchestration, worktree seeding, and the manifest differ too much from the single-spec flow.
- **Keep `/parallel-implement` and add a separate autonomous command**: rejected because two near-identical parallel commands would drift.
- **Stop the whole batch when one spec fails**: rejected by the owner; one failing spec should not discard the others.
- **Let the agent commit in autonomous mode**: rejected because Git history stays user-owned.

## Consequences

- Positive: unattended multi-spec runs with an auditable decision trail; dependent specs can run in series.
- Negative / risk: decisions made without the user may need rework, hence the mandatory report; a queue seeds each worktree from the previous patch, which adds a `review_base` concept to reviews.
