# Project Settings

This file holds project-specific settings that vary between projects using this starter. Every new spec uses its complete ID (`yyyy_mm_dd_hh_ii_ss-spec-title`) for its temporary local `feature/<spec-id>` branch and worktree; existing legacy numeric spec IDs remain supported. The workflow uses one isolated worktree and branch per spec, then transfers verified changes to the local target branch for review. It does not create pull requests. Complete the local review and user-authorized commit/push before starting another spec. `Design workspace URL:` is an optional browser workspace for UI design passes (for example, Figma or OpenDesign); use `-` when none is configured. UI specs can still use local design references without a workspace URL. For backward compatibility, `/spec` also accepts the legacy `OpenDesign URL:` key. `Test command:` and `Typecheck command:` are read by the dev workflow (`$dev` in Codex, `/dev` elsewhere) and `/review-spec-implementation` - keep those keys named exactly as below.

Target branch: main
Design workspace URL: -
Test command: -
Typecheck command: -
