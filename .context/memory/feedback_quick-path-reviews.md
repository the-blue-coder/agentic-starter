---
name: feedback_quick-path-reviews
description: Always run both reviews after direct code edits, including small follow-ups after a spec.
metadata:
  type: feedback
---

Run both `$review-changes` and `$review-security` immediately after every direct code edit, including quick fixes and follow-up edits after a spec workflow. Do not treat manual inspection, a clean diff check, or tests as a substitute.

**Why:** The user corrected a missed review gate after a small Twig follow-up edit.

**How to apply:** Start both reviews in the same turn after the edit, before giving a completion response or committing. If either was missed, stop and run it retroactively before doing anything else.
