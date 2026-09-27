# Project Settings

This file holds project-specific settings that vary between projects using this starter. Every spec uses its complete ID (`yyyy_mm_dd_hh_ii_ss-spec-title`) for its temporary local `feature/<spec-id>` branch and worktree; existing legacy numeric spec IDs remain supported. Use `$implement` / `/implement` for one spec or `$parallel-implement` / `/parallel-implement` for a batch of independent specs. Both hand verified changes to the local target branch without creating pull requests. Parallel batches keep an ignored recovery manifest under `.worktrees/.parallel-batches/`; resolve any incomplete batch before starting more work. Review the complete target-branch diff locally and directly invoke `$commit-and-push` / `/commit-and-push` when ready; agents never commit or push otherwise. `Design workspace URL:` is an optional browser workspace for UI design passes (for example, Figma or OpenDesign); use `-` when none is configured. UI specs can still use local design references without a workspace URL. For backward compatibility, `/spec` also accepts the legacy `OpenDesign URL:` key. `Test command:` and `Typecheck command:` are read by the dev workflow (`$dev` in Codex, `/dev` elsewhere) and `/review-spec-implementation` - keep those keys named exactly as below.

Target branch: main
Design workspace URL: -
Test command: -
Typecheck command: -
