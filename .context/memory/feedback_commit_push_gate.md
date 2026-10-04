---
name: feedback_commit_push_gate
description: Commit and push only when the user directly invokes the commit-and-push command.
metadata:
  type: feedback
---

Run `git commit` and `git push` only when the user directly invokes `/commit-and-push`. That direct invocation authorizes the command's commit and push workflow. No other request, command, completed review, spec status, or workflow handoff authorizes an agent to commit or push.

**Why:** The user corrected an agent that committed and pushed outside this explicit command gate, then clarified that the command itself is the intended authorization.

**How to apply:** `/spec`, `/dev`, `/implement`, quick path, reviews, initialization, and all other workflows stop before commit and push. They may tell the user to invoke the command, but may never invoke it for them. When the user directly invokes it, follow its canonical workflow and perform the commit and push.
