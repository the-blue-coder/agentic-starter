---
type: decision
status: accepted
date: 2026-10-04
tags: [security, tooling, agent-workflows]
supersedes: [[2026-10-04 - Commit security rules snapshot in projects]]
affects: [[Security review workflow]]
---

## Context

Committing the OWASP rules snapshot in every project made each project carry its own updater script, GitHub Action, and pull request stream for the same files. The starter is where the workflow lives and `/update-workflow` already propagates workflow files. The upstream repository still declares no redistribution license. The starter is public; every project repository built from it is private, and the starter owner accepts the licensing risk.

## Decision

The starter commits the snapshot under `.context/security-rules/` (`rules/*.md` plus `source.json` with the upstream commit). A weekly GitHub Action in the starter refreshes it through a pull request that must be reviewed before merge. Projects receive the snapshot through `/update-workflow` as workflow-owned files; they have no updater script and no Action of their own. `.context/coding-conventions/security.md` stays authoritative.

## Why not something else

- **Snapshot and Action in every project**: duplicated tooling and a pull request per project for identical content.
- **Git ignored cache**: first review needs network and Python, and snapshots drift between machines.
- **Refresh silently**: rule changes would reach the review without anyone reading them.

## Consequences

- Positive: one reviewed refresh for all projects, reproducible reviews, nothing to install or download in a project, and no `.context/scripts/` folder.
- Negative / risk: the public starter redistributes unlicensed upstream content, which the owner accepts and which must be revisited if the upstream adds a license or a project becomes public; a project gets new rules only when it runs `/update-workflow`; the starter repository must allow Actions to create pull requests.
- Generates: older projects delete their own updater Action and `.cache/security-rules/`; `/update-workflow` removes the retired `.context/scripts/` folder.
