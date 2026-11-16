---
description: "Apply the approved stack-specific setup from the architecture decision and the matching stack recipe"
argument-hint: "<optional context>"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - WebSearch
  - WebFetch
---

Context, if any: `$ARGUMENTS`

Read `.context/commands/setup-stack.md` and follow its instructions exactly, using the context above as `$ARGS`.
