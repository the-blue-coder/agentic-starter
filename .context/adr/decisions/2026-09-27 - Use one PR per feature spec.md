---
type: decision
status: superseded
date: 2026-09-27
tags: [workflow, git]
---

# Use one PR per feature spec

## Context

The feature workflow already creates a worktree and `feature/<NNN-slug>` branch for each spec, but project settings also allowed local squash-merges. That made the documented one-spec/one-branch/one-PR pipeline optional and let initialization leave its required settings unresolved.

## Decision

Every feature spec uses one `feature/<NNN-slug>` branch and exactly one pull request against the configured target branch.

## Why not something else

- **Local squash-merge mode**: rejected because it bypasses the required pull request and makes the per-spec pipeline inconsistent.
- **A second PR after a closed PR**: rejected because one spec must keep one review record; reopen the existing PR instead.

## Consequences

- Positive: CI, review, and merge state are visible for every feature spec.
- Positive: `$commit-and-push` can resolve one branch and one PR deterministically.
- Negative / risk: a feature project needs a GitHub remote and authenticated `gh` CLI to open or inspect its PR.
