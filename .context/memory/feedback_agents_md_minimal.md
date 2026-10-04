---
name: feedback_agents_md_minimal
description: AGENTS.md must contain only the mandatory-read pointer to the workflow entrypoint, no rules.
metadata:
  type: feedback
  confidence: high
---

Keep `AGENTS.md` (imported by `CLAUDE.md`) limited to the "mandatory read" pointer to `.context/ai-workflow-entrypoint.md`. Do not duplicate workflow rules such as the commit-and-push gate there.

**Why:** The user spotted the commit-and-push gate in `AGENTS.md` and said it should not be there; rules live in `.context/`.

**How to apply:** Put new workflow rules in `.context/` files (entrypoint, rules, conventions, commands), never in `AGENTS.md` or `CLAUDE.md`.
