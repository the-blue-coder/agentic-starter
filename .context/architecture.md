# Architecture

> **Project not initialized yet?** If this file still contains `[bracketed]` placeholders, stop and run `/init-project`. The chosen stack recipe under `.context/stacks/` fills this file in.

## Stack

| Layer          | Technology | Role |
| -------------- | ---------- | ---- |
| Backend        | [e.g. Symfony, Express, Django] | |
| Database       | [e.g. PostgreSQL] | |
| Frontend       | [e.g. Next.js, plain HTML] | |
| Styling        | [e.g. Tailwind CSS] | |
| Auth           | [e.g. Clerk, custom sessions] | |

## Repo Structure

```
[Describe the top-level folder layout once known -
e.g.:
/
├── backend/   - API/server code
├── frontend/  - UI code
├── infra/     - deploy scripts + configs
]
```

## Key Invariants

1. [Add invariants here as the project evolves - e.g. "the backend defines all API routes, frontend never invents routes".]

## System Boundaries

- [Layer] - owns [what].
- [Layer] - owns [what].

## Storage Model

- [Describe persistence: what's stored where, key data-modeling rules - e.g. money as integer cents, UUID vs auto-increment IDs.]

## Auth and Access Model

- [Describe how auth works: provider, guard location, ownership/access rules for user-owned resources.]

## Project-Specific Invariants

1. [Add invariants here as the project evolves.]
