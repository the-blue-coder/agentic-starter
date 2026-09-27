---
name: feedback_local_agent_opendesign_handoff
description: Keep the local coding agent distinct from OpenDesign's design-generation runtime.
metadata:
  type: feedback
---

Treat OpenDesign as a separate design workspace. The coding agent that reads and implements the project may be Codex, Claude Code, OpenCode, or another local tool; do not assume the coding agent is the agent running inside OpenDesign.

**Why:** The user clarified that agent agnosticism refers to the local coding agent, not OpenDesign's own agent runtime.

**How to apply:** Keep workflow logic in `.context/commands/`. For UI work, hand the local agent a versioned design export so it can consume the same reference regardless of its MCP support or configuration.
