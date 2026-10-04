# Architecture

> **New project:** Run /prd, then /architecture to choose and document the stack before applying stack-specific setup.
>
> **Existing project:** Run /architecture to document the architecture reflected in the code. If .context/ is absent and you only want this document, the command creates only .context/architecture.md. /init-project sets up shared workflow context and never chooses a stack.

## Stack

| Layer          | Technology | Role |
| -------------- | ---------- | ---- |
| Backend        | [e.g. Symfony, Express, Django] | |
| Database       | [e.g. PostgreSQL] | |
| Frontend       | [e.g. Next.js, plain HTML; use `None` if there is no user-facing UI] | |
| Styling        | [e.g. Tailwind CSS] | |
| Auth           | [e.g. Clerk, custom sessions] | |

## Testing

> TDD scope, loop, and journal: `.context/coding-conventions/tdd.md`. Choose the tools here at `/architecture` time; never leave a row blank (write `None` with the reason when a level does not apply).

| Level | Tool | Location | Command |
| ----- | ---- | -------- | ------- |
| Backend unit | [e.g. PHPUnit, Pest, Vitest, pytest] | | |
| Backend integration / API | [e.g. PHPUnit WebTestCase, supertest] | | |
| Frontend logic (hooks, utils) | [e.g. Vitest, Jest; `None` if no frontend] | | |
| Frontend components | [e.g. Testing Library; `None` if no frontend] | | |
| End-to-end | [Playwright; `None` if no user-facing UI] | | |

Browser verification by the agent (not committed tests): Claude in Chrome under Claude Code, Playwright elsewhere.

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
