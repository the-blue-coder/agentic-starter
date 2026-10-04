---
type: decision
status: proposed
date: 2026-10-04
tags: [workflow, tooling, specs, migration]
affects: [[Implementation workflows]]
---

## Context

Projects copy the starter's workflow files and then drift from it: commands, subagents, hooks, and conventions evolve, and nothing brings an existing project up to date. Two earlier decisions also left projects half-migrated: spec IDs moved from `<number>-<slug>` to `yyyy_mm_dd_hh_ii_ss-spec-title`, and [[2026-09-27 - Use timestamped feature spec identifiers]] explicitly declined to rename historical specs, so older projects mix both formats indefinitely.

## Decision

Add `/update-workflow`, run by hand inside an existing project. It clones the starter named by `Starter source:` in `.context/project-settings.md`, then updates only workflow-owned paths: `.context/` commands, scripts, stacks, conventions (not `security.md`) and workflow docs, the `.claude/` and `.opencode/` commands, agents and hooks, `.githooks/`, and the root agent files. Project-owned files are never touched. Each file is classified by comparing it with the starter's history: an unmodified older copy is overwritten, a customized file is three-way merged against `Starter version:` (the last applied starter commit, stamped by the command), and files the starter deleted are removed only when unmodified. Without that stamp a base is never guessed, so a project's first update treats its differing files as conflicts, decided by group with the user's confirmation: starter version for workflow machinery (commands, agents, hooks, `global.md`, `tdd.md`), the project's own version for stack conventions and recipes. Project-only files, such as custom commands, are left alone. Settings, hook entries, `.gitignore`, `.gitattributes`, `AGENTS.md`, and `CLAUDE.md` are merged additively.

The same run migrates legacy numeric specs to UTC IDs, using the date of each spec file's first commit made strictly increasing in numeric order, and rewrites references to them in project-owned Markdown. Specs with an active worktree or feature branch are skipped until their handoff. This relaxes the "do not rename historical specs" clause of the superseded timestamp decision, but only as an explicit step the user confirms; unmigrated legacy IDs stay supported. The command shows the whole plan and waits for confirmation, leaves everything uncommitted and unstaged, and never commits or pushes.

## Why not something else

- **Re-copy the starter files over the project**: rejected because it overwrites local customizations without warning.
- **Always take the starter's version, or always keep the local one**: rejected because the first loses customizations and the second leaves the project stale.
- **Guess a merge base from the most similar historical version**: rejected after a dry run on a real older project, where copies predated the starter's history and similarity was too low to trust a merge.
- **One question per conflicting file**: rejected because a first update of an older project conflicts on most workflow files.
- **A separate command only for spec renumbering**: rejected because workflow files and spec IDs change together, and the workflow also evolves for reasons other than numbering.
- **Rename specs with a fresh timestamp from the migration day**: rejected because it destroys the chronological order that first-commit dates preserve.
- **Rename specs with active worktrees too**: rejected because it would break their `feature/<spec-id>` branch and worktree.

## Consequences

- Positive: existing projects follow starter improvements deliberately, with a reviewable diff and no silent overwrites; legacy and new spec IDs stop coexisting.
- Negative / risk: bare-number mentions of a spec ("spec 006") are not rewritten; old IDs remain in Git history and past references outside the repository; conflict resolution on customized files still needs the user.
- Generates: new `update-workflow` command with wrappers for `.claude/` and `.opencode/`, and `Starter source:` and `Starter version:` keys in `.context/project-settings.md`.
