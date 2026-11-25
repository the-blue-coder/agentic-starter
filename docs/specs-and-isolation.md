# Specs and isolation

- **Spec ID:** `yyyy_mm_dd_hh_ii_ss-spec-title` (UTC). Older `NNN-slug` IDs stay supported until migrated by `/update-workflow`.
- **One spec, one worktree, one branch:** `.worktrees/<spec-id>/` on `feature/<spec-id>`, removed after a verified handoff.
- **Per-spec files:** the spec (with its `ui:` and `seo:` frontmatter flags), a design brief and visual references for UI specs under `.context/feature-specs/design/<spec-id>/`, and a `## Test map` section at the end of the spec.
- **Batches:** `/implement-queue` and `/implement-swarm` keep a resumable manifest under `.worktrees/.parallel-batches/`; an incomplete batch blocks new work until it is resumed.
