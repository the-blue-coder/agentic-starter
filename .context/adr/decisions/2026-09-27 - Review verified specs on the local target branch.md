---
type: decision
status: accepted
date: 2026-09-27
tags: [workflow, git, specs]
supersedes:
  - "[[2026-09-27 - Use timestamped feature spec identifiers]]"
  - "[[2026-09-27 - Persist design briefs and validate visual handoffs]]"
affects:
  - "[[.context/commands/dev.md]]"
  - "[[.context/commands/implement.md]]"
  - "[[.context/commands/review-security.md]]"
  - "[[.context/commands/commit-and-push.md]]"
  - "[[.context/commands/status.md]]"
---

# Review verified specs on the local target branch

## Context

The previous feature pipeline pushed each spec branch to GitHub and required one pull request per spec. That added a remote review and cleanup cycle even though the user wants to inspect the verified changes locally in VS Code or the terminal. The user also requires that commits and pushes happen only after a direct `$commit-and-push` invocation.

## Decision

Implement each spec in its own temporary worktree and local `feature/<spec-id>` branch, then, after implementation and all automated reviews pass, transfer its verified changes to the configured local target branch as uncommitted changes for the user to review; never create a pull request or push a feature branch.

Keep new spec IDs in `yyyy_mm_dd_hh_ii_ss-spec-title` format and support existing numeric IDs. After a safe transfer, remove the temporary worktree and local feature branch. The user reviews the changes on the target branch and directly invokes `$commit-and-push` when ready; only that command commits and pushes the target branch to `origin`.

Keep the self-contained per-spec UI design brief and reviewed references described by the superseded design-handoff decision. They remain synchronized with the spec worktree and are preserved in the local target checkout during handoff.

## Why not something else

- **Keep one pull request per spec**: rejected because the user wants the final review in the local target checkout and no pull requests at all.
- **Implement directly on the target branch**: rejected because a dedicated worktree and branch keep implementation isolated until automated reviews pass.
- **Commit or push during the handoff**: rejected because it would bypass the user's explicit `$commit-and-push` authorization gate and prevent local review before shipping.

## Consequences

- Positive: the user reviews the exact pending target-branch changes in their local editor and terminal, with no PR creation, remote feature branch, GitHub CLI, or post-merge cleanup cycle.
- Positive: implementation remains isolated in a per-spec worktree until its acceptance criteria, conventions, and security review pass.
- Negative / risk: GitHub PR discussion and PR-triggered checks are not part of this workflow; any required checks must be run locally or through another configured process.
- Negative / risk: only one spec can be integrated into the target checkout at a time; a clean and matching target base is required for safe handoff.
- Generates: update the shared workflow commands, all tool wrappers and references, settings, status output, and starter documentation to remove the PR pipeline.
