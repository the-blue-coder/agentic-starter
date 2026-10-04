---
type: decision
status: accepted
date: 2026-10-04
tags: [security, tooling, agent-workflows]
supersedes: [[2026-09-27 - Use shared OWASP rules for security reviews]]
affects: [[Security review workflow]]
---

## Context

The previous decision kept the OWASP rules snapshot Git ignored and refreshed it from each session. In practice that made every clone depend on Python, Git, and the network for its first review, and let two machines review against different rule versions. The upstream repository still declares no redistribution license. The starter is public; every project repository built from it is private.

## Decision

Each project commits the snapshot under `.context/security-rules/` (`rules/*.md` plus `source.json` with the upstream commit). `.context/scripts/update-security-rules.py` refreshes it, and a weekly GitHub Action (template in `.context/scripts/update-security-rules.workflow.yaml`, installed by `/update-workflow`) opens a pull request that must be reviewed before merge, because the rules are reference data fed to the security review. `.context/coding-conventions/security.md` stays authoritative. The public starter does not commit a copy of the rules.

## Why not something else

- **Keep the Git ignored cache**: first review needs network and Python, and snapshots drift between machines.
- **Commit the snapshot in the starter**: the starter is public, so it would redistribute unlicensed content. Revisit if the upstream adds a license or its author agrees.
- **Refresh silently on every session**: rule changes would reach the review without anyone reading them.

## Consequences

- Positive: reproducible reviews, no network or Python needed in a new clone, and rule changes are reviewed in a pull request.
- Negative / risk: each private project holds a copy of unlicensed upstream content, which the owner accepts; every project needs GitHub Actions allowed to create pull requests; the Action runs on the default branch, not on `Target branch:`.
- Generates: older projects get the script, template, and workflow file from `/update-workflow`, and delete any old `.cache/security-rules/` themselves.
