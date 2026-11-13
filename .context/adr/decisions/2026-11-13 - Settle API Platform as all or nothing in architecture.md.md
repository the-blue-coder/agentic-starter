---
type: decision
status: proposed
date: 2026-11-13
tags: [architecture, symfony, api-platform, workflow]
affects: [[Stack recipes]]
---

## Context

The Symfony conventions describe classic controllers for JSON endpoints, and the Symfony + Next.js recipe asked only a yes/no question about API Platform at setup time. A project that installs API Platform and still adds controllers ends up with two ways to expose behavior. The user wants this decided deliberately, as a brainstorm, when Symfony is chosen.

## Decision

When Symfony is a candidate, `/architecture` brainstorms API Platform with the user and settles exactly one of two modes: "API Platform only" (every endpoint is an API Platform operation, no classic controllers) or "No API Platform" (plain controllers, API Platform not installed). The chosen mode is recorded as a Key Invariant.

## Why not something else

- **A hybrid (API Platform for CRUD, controllers for the rest)**: rejected by the user, who wants one consistent style.
- **Asking only at setup time (the recipe's yes/no)**: rejected because the choice shapes the architecture and the conventions that apply, so it belongs to `/architecture`.
- **Always API Platform by default**: rejected because it is a poor fit for some products, and a default skips the brainstorm.

## Consequences

- Positive: one consistent backend style per project, decided early and recorded.
- Negative / risk: "API Platform only" needs custom providers and processors for non-CRUD endpoints; `symfony.md` keeps its controller rules for projects without API Platform.
- Generates: edits to `architecture.md` (command), `symfony.md`, the Symfony + Next.js recipe and the changelog.
