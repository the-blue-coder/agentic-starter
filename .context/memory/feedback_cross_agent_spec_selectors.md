---
name: feedback_cross_agent_spec_selectors
description: Accept dropped spec files in implementation commands consistently across local coding agents.
metadata:
  type: feedback
---

Support dropped local spec files and their `file:` URLs in `dev`, `implement`, and `implement-swarm` across Claude Code, OpenCode, and other local coding agents.

**Why:** The user clarified that selecting specs by drag and drop should not be tied to a single agent.

**How to apply:** Keep argument parsing in shared canonical workflow documentation and make native wrappers pass arguments through unchanged.
