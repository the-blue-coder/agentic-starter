---
name: feedback_step-numbering
description: Command step lists must use plain sequential numbering - never "Step 0" or "Step 8.5" bolt-ons
metadata:
  type: feedback
---

Never insert a new step into an existing `.context/commands/*.md` file as "Step 0" or "Step N.5" to avoid renumbering. Always renumber every subsequent step so the sequence stays plain integers starting at 1 (Step 1, Step 2, Step 3...).

**Why:** the user explicitly rejected a "Step 0 - Memory check" inserted before "Step 1 - Understand what changed" in `commit-and-push.md`, and the equivalent "Step 8.5" in `dev.md` - asked to shift everything down by one instead.

**How to apply:** whenever a new step is added anywhere in the middle of an existing numbered command sequence (not just for memory-check steps), renumber the whole list rather than reaching for a fractional/zero index. Check every place that references a step by number elsewhere in the same file (e.g. "then continue to Step 9") and update those too.
