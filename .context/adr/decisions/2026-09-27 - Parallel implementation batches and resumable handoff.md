---
type: decision
status: accepted
date: 2026-09-27
tags: [workflow, git, specs, agents]
supersedes:
  - "[[2026-09-27 - Review verified specs on the local target branch]]"
affects:
  - "[[.context/commands/parallel-implement.md]]"
  - "[[.context/commands/implement.md]]"
  - "[[.context/commands/dev.md]]"
  - "[[.context/commands/status.md]]"
  - "[[.context/commands/commit-and-push.md]]"
---

# Parallel implementation batches and resumable handoff

## Context

The per-spec workflow isolates implementation in one temporary feature worktree, reviews it, and transfers its uncommitted changes to the local target branch. The user wants several independent specs implemented concurrently by subagents, with a primary agent coordinating integration, while preserving local review and the direct `$commit-and-push` authorization gate. A process interruption or failed deletion can leave temporary worktrees behind.

## Decision

Run selected `todo` specs concurrently in one worktree and local feature branch per spec, have the primary agent integrate their uncommitted diffs in a temporary integration worktree and transfer the reviewed batch to the local target branch without creating commits, and track every lifecycle phase in an ignored manifest so interrupted integration or cleanup is detectable and resumable.

Use patch-based three-way integration because the feature worktrees have no commits; do not use `git merge --no-commit`, which needs source commits. Keep target changes uncommitted and unstaged for the user's local review. Permit `$commit-and-push` only after direct user invocation. Do not delete a worktree until its complete diff is verified in the target checkout; remove feature branches only after their worktree is gone and their commit still matches the recorded base.

## Why not something else

- **Run each spec sequentially through the existing handoff:** rejected because it cannot keep several isolated implementations in flight and would dirty the target checkout after the first spec.
- **Use `git merge --no-commit`:** rejected because workers produce no feature-branch commits under the existing commit authorization rule.
- **Delete worktrees unconditionally in a final cleanup block:** rejected because interruptions can prevent cleanup and forced deletion before transfer could lose uncommitted work.
- **Stop the entire batch when one cleanup operation fails and forget its state:** rejected because orphaned worktrees or branches would go undetected and block reliable future work.

## Consequences

- Positive: independent specs can be implemented concurrently and presented as one uncommitted local target-branch diff for review.
- Positive: the batch manifest records worker, integration, transfer, and cleanup state; `/status` can report incomplete work and `parallel-implement resume <batch-id>` can continue safely.
- Negative / risk: overlapping edits need three-way patch resolution and aggregate review; unresolved conflicts leave the primary target checkout unchanged and the batch worktrees intact.
- Negative / risk: a crash can still leave worktrees behind, but the manifest and read-only status reporting make them visible and cleanup resumable rather than silent.
- Negative / risk: only one incomplete batch may exist at a time, and new work remains blocked until recovery and local target review are complete.
- Generates: shared parallel command, per-spec batch-worker mode, status and workflow gates, tool wrappers, and README/setting documentation.
