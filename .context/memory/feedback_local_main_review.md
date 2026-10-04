---
name: feedback_local_main_review
description: The user wants feature changes reviewed on the local target branch and never wants pull requests.
metadata:
  type: feedback
  confidence: high
---

After implementation and automated reviews pass, transfer the spec's changes from its temporary worktree into the local target checkout so the user can review in VS Code or the terminal. Do not create a pull request or push a feature branch. Leave target-branch changes uncommitted and unpushed until the user directly invokes `/commit-and-push`.

**Why:** The user explicitly confirmed this local-review workflow and rejected PRs entirely.

**How to apply:** Keep one temporary worktree and local feature branch per spec during implementation. Once verified, safely apply the changes to the configured target branch, clean up the temporary worktree/branch, and hand off for local review. Commit and push only inside the directly invoked command.
