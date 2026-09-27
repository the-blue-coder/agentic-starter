# Project Settings

This file holds project-specific settings that vary between projects using this starter. Every new spec uses its complete ID (`yyyy_mm_dd_hh_ii_ss-spec-title`) for its `feature/<spec-id>` branch and one pull request; existing legacy numeric spec IDs remain supported. The one-spec/one-branch/one-PR workflow is fixed. `Ship confirmation: human` means `/commit-and-push` asks before opening a PR. `Design workspace URL:` is an optional browser workspace for UI design passes (for example, Figma or OpenDesign); use `-` when none is configured. UI specs can still use local design references without a workspace URL. For backward compatibility, `/spec` also accepts the legacy `OpenDesign URL:` key. `Test command:` and `Typecheck command:` are read by the dev workflow (`$dev` in Codex, `/dev` elsewhere), `/commit-and-push`, and `/review-spec-implementation` - keep those keys named exactly as below.

Target branch: main
Ship confirmation: human
Design workspace URL: -
Test command: -
Typecheck command: -
