---
name: feedback_quick-path-reviews
description: Always run all reviews after direct code edits, including small follow-ups after a spec.
metadata:
  type: feedback
---

Run `/review-changes`, `/review-performance`, and `/review-security` immediately after every direct code edit, including quick fixes and follow-up edits after a spec workflow. Do not treat manual inspection, a clean diff check, or tests as a substitute. `/review-performance` runs mandatory-or-"Not applicable" itself based on a closed list (query/network call, loop, UI rendering, dependency, file handling); the agent never skips it on its own judgment.

**Why:** The user corrected a missed review gate after a small Twig follow-up edit.

**How to apply:** Start the reviews in the same turn after the edit, before giving a completion response or committing: `/review-changes` and `/review-performance` first, `/review-security` last. If any was missed, stop and run it retroactively before doing anything else.
