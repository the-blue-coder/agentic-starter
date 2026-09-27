---
name: feedback_direct_starter_edits
description: Skip the feature-spec workflow when the user asks for direct edits to the starter itself.
metadata:
  type: feedback
---

When the user asks to modify the starter's own workflow or documentation directly, edit those files in the current checkout. Do not create a feature spec, worktree, or feature branch unless the user explicitly requests that process.

**Why:** The user corrected an unnecessary spec and worktree created for a direct starter modification.

**How to apply:** Distinguish editing the starter workflow from implementing an application feature; use the requested scope and keep the commit/push gate unchanged.
