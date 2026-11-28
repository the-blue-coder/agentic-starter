---
description: "Apply a change to the agentic starter only (D:/Me/Projects/.agentic-starter), then commit and push the starter directly - never propagated to other projects"
argument-hint: "<what to change in the starter>"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

Read `.context/commands/update-starter.md` and follow its instructions exactly.

Run this command only when the user directly invokes `/update-starter`; never invoke it from another workflow.
