---
name: feedback_design_tool_agnostic_handoff
description: Keep design handoffs tool-agnostic and distinct from the local coding agent.
metadata:
  type: feedback
---

Keep the design tool/workspace separate from the local coding agent. OpenDesign is one example, never a requirement; projects may use another provider or local design references.

**Why:** The user clarified that the starter must not be tied to their personal OpenDesign instance.

**How to apply:** Make workspace URLs optional. Store reviewed, versioned design references in the spec so Codex, Claude Code, OpenCode, or another agent can use them without live access or provider-specific MCP setup.
