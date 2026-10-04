---
name: feedback_batch_autonomy_and_tdd
description: Multi-spec runs are autonomous but never commit; testing follows a strict TDD loop, not test-first.
metadata:
  type: feedback
  confidence: high
---

`/implement-queue` (series) and `/implement-swarm` (parallel) run unattended: the agent decides open questions, records them for a final decision report, sets failed specs aside, and never commits or pushes. Testing uses the red-green-refactor loop (one failing test, minimum code) for backend code, frontend logic, and bug fixes, with test technologies chosen per stack in `/architecture`'s `## Testing` section. Codex support was dropped; only Claude Code and OpenCode are supported.

**Why:** The user wants to start a batch and read one report, keeps Git history under their control, and considers batch test-first a way for AI to over-build.

**How to apply:** Never add Codex wrappers or `$`-syntax. Keep autonomous commands free of questions and commits. Keep the TDD scope in `.context/coding-conventions/tdd.md` as the single source. See [[feedback_commit_push_gate]].
