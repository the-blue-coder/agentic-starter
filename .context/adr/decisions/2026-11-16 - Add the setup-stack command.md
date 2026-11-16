---
type: decision
status: accepted
date: 2026-11-16
tags: [workflow, commands, stacks, setup]
affects: [[Stack recipes]]
---

## Context

After `/architecture`, the workflow only said "apply the approved stack-specific setup separately" with no command behind it. The recipe's Part 3 had to be followed by hand, with nothing enforcing the plan, the approval of outward-facing actions, the verification or the cleanup of `.context/stacks/`. A project whose architecture deviates from its recipe (another auth provider, an added service) had no rule saying which one wins.

## Decision

Add `/setup-stack`, an explicit command that runs after `/architecture`: it checks the framing, picks the matching recipe, shows a plan with every deviation for approval, applies the setup, verifies it, writes `infra.md` and the test and typecheck commands, and offers to delete `.context/stacks/`. The architecture and its ADR always win over the recipe. Every outward-facing action (GitHub repository, SSH writes, DNS, secrets, first deploy) needs its own confirmation, and the command never commits or pushes.

## Why not something else

- **Run the setup inside `/architecture`**: rejected because the workflow keeps the decision and its application as separate, explicit steps.
- **Run the setup inside `/init-project`**: rejected because it must stay stack-agnostic.
- **Keep following the recipe by hand**: rejected because nothing enforces approval, verification or cleanup.
- **Let the recipe win over the architecture**: rejected because the user-approved decision is the source of truth.

## Consequences

- Positive: one explicit, verifiable step between the architecture decision and the first spec, with safe handling of outward-facing actions.
- Negative / risk: a recipe that drifts from the architecture needs the command to adapt it; the plan step must surface every deviation.
- Generates: the command and its native wrappers, edits to `/init-project`, `/architecture`, `/spec`, `/status`, the entrypoint, the README and the changelog.
