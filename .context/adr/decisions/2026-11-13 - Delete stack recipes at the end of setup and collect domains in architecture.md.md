---
type: decision
status: proposed
date: 2026-11-13
tags: [architecture, stacks, workflow, infra]
affects: [[Stack recipes]]
---

## Context

`/architecture` deleted `.context/stacks/` in its final phase, before the stack-specific setup it tells the user to run next. The setup lives in the recipe, so a project could lose its own setup guide. Also, the domains were only asked at the recipe's setup step 3.0, after the architecture decision, although they affect auth callbacks, CORS and the reverse proxy.

## Decision

`/architecture` prunes only unused stack conventions and asks the hosting and deployment inputs (domains, subdomain layout, staging, DNS, server alias) during its exploration, recording them in `architecture.md`. Each recipe's last step deletes `.context/stacks/` after the setup is verified, and its setup step 3.0 reuses the answers already in `architecture.md`.

## Why not something else

- **Delete the recipes in `/architecture`**: rejected because the setup still needs the chosen recipe.
- **Keep `.context/stacks/` in the project permanently**: rejected by the user, who does not want the recipes to stay.
- **Run the setup inside `/architecture`**: rejected because the workflow keeps the setup a separate, explicit step.
- **Read recipes from the starter at setup time**: rejected because it makes setup depend on access to the starter.
- **Ask the domains in `/init-project`**: rejected because it must not collect hosting or deployment details; those depend on the hosting decision.

## Consequences

- Positive: the setup guide is never lost, no recipe lingers after the setup, and domains are known before auth and infra decisions.
- Negative / risk: a project that never runs the setup keeps the recipes; the recipes must keep their cleanup step.
- Generates: edits to `architecture.md`, `update-workflow.md`, both recipes, the README and the changelog.
