---
type: decision
status: accepted
date: 2026-11-16
tags: [workflow, commands, backup, api-platform, setup]
affects: [[Add the setup-stack command]]
---

## Context

`/setup-backup` was listed only among the "Infra runbooks" and nothing in the framing sequence or the diagrams pointed to it, so a deployed project could go without backups. The command also installed a classic Symfony controller, which contradicts the "API Platform only" mode that `/architecture` can settle (no `Controller/` folder, no `#[Route]` action), and it assumed the compose service was called `backend` and that the base image was Alpine.

## Decision

`/setup-backup` becomes a step of the setup sequence: `/init-project` → `/prd` → `/architecture` → `/setup-stack` → `/setup-backup` (when the project has a database) → `/design-system` → `/spec`. It appears in the README sequences and diagrams, in `/init-project`, `/architecture`, `/setup-stack`, the entrypoint and the recipe's backup step. It is recommended but is not a `/spec` gate. The command detects the backend mode from `architecture.md`: API Platform only gets a `BackupRun` resource, a state processor and a secret authenticator (firewall `webhook`); plain controllers keep the controller. It requires a functional test, uses the real compose service name, supports Debian and Alpine images, and keeps the webhook secret out of committed files.

## Why not something else

- **Making it a `/spec` gate**: rejected because a project without production data can reasonably defer backups, and a gate would block unrelated work.
- **Keeping the controller for every project**: rejected because it breaks the architecture's API Platform only invariant.
- **Two separate commands (one per mode)**: rejected because one command with a mode branch avoids duplicating the shared services and steps.
- **Leaving it in the infra runbooks only**: rejected because the user wants it treated as a step to do, visible in the diagrams.

## Consequences

- Positive: backups are part of the visible path to a production-ready project, and the command no longer contradicts the architecture.
- Negative / risk: the command is longer; the Mode A security setup (a `webhook` firewall, a `memory` provider) must be checked by the test it requires.
- Generates: edits to the README, the entrypoint, `/init-project`, `/architecture`, `/setup-stack`, the recipe and the changelog.
