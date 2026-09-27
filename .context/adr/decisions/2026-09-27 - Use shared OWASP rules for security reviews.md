---
type: decision
status: accepted
date: 2026-09-27
tags: [security, tooling, agent-workflows]
affects: [[Security review workflow]]
---

## Context

The security review uses project-specific rules plus a copied ECC checklist. The user wants the more complete `vchirrav-eng/owasp-secure-coding-md` rules and weekly updates that work across Codex, Claude Code, and OpenCode. The upstream repository currently declares no redistribution license.

## Decision

Keep `.context/coding-conventions/security.md` authoritative and use a shared, Git ignored local snapshot of the upstream Markdown rules as supplementary guidance. Refresh it from the common workflow entrypoint at most once every seven days after a successful download, and record the upstream commit in security review reports.

## Why not something else

- **Keep the ECC checklist**: it duplicates supplementary guidance and has no shared update path.
- **Use only upstream rules**: general rules cannot encode this project's Clerk, webhook, data isolation, and deployment decisions.
- **Run the upstream MCP server**: it adds per-agent configuration and a runtime dependency for rules that can be read as local Markdown.
- **Commit a copy of the rules**: the upstream repository does not currently declare redistribution terms.

## Consequences

- Positive: all three agents read the same rule snapshot and cite stable rule IDs with an exact source commit.
- Positive: the project-specific security policy remains stable when upstream guidance changes.
- Negative / risk: a new clone needs Git, Python, and network access before its first full supplementary review.
- Generates: older projects need a one-time workflow migration; their own `security.md` must be preserved.
