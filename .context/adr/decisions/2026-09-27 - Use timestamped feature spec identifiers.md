---
type: decision
status: proposed
date: 2026-09-27
tags: [workflow, git, specs]
supersedes:
  - "[[2026-09-27 - Use one PR per feature spec]]"
  - "[[2026-09-27 - Use versioned design references for UI specs]]"
---

# Use timestamped feature spec identifiers

## Context

The sequential three-digit spec prefix is allocated from the files visible in one checkout. Parallel work, multiple agents, or separate machines can choose the same next number. The identifier is also reused as the feature branch, worktree, design folder, verification record, and pull request head, so collisions can mix otherwise separate work.

## Decision

Every new feature spec uses `yyyy_mm_dd_hh_ii_ss-spec-title`, where the timestamp is UTC and uses a 24-hour clock (`hh` is 00–23, `ii` is minutes, and `ss` is seconds), and the title is a lowercase, hyphenated slug. For example: `2026_09_27_15_42_31-add-search`.

Use the complete spec ID for the spec filename, `feature/<spec-id>` branch, `.worktrees/<spec-id>/` worktree, `.context/feature-specs/design/<spec-id>/` handoff folder, and `.context/docs/verif/<spec-id>.md` verification record. Preserve one spec per branch and exactly one pull request against the configured target branch.

If the exact full ID already exists, allocate the next UTC second and check again. Keep existing numeric specs, branches, and records in place; commands continue to support them by using the full legacy filename stem. Do not rename historical specs as part of this change.

## Why not something else

- **Keep incrementing a local sequence**: rejected because separate checkouts and agents can allocate the same next number.
- **Use a date without time**: rejected because multiple specs can be created on the same day.
- **Rename all existing specs**: rejected because it would disrupt existing branches, worktrees, and PR references without helping new allocations.

## Consequences

- Positive: independent agents and checkouts have a much lower risk of choosing a colliding ID.
- Positive: every per-spec path can be derived from one stable identifier.
- Negative / risk: IDs and branches are longer; tools and reports must keep the complete filename stem.
- Negative / risk: legacy numeric identifiers remain a supported path until their work is complete.
