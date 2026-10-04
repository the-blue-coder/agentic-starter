---
type: decision
status: accepted
date: 2026-10-04
tags: [nextjs, frontend, structure]
affects: [[Next.js conventions]]
---

## Context

The Next.js conventions split domain code across `src/services/` (server fetching), `src/types/<domain>.ts`, `src/constants/<domain>.ts`, and `src/schemas/`, so one backend domain was spread over four folders. The SoGood Santé project instead keeps everything for a domain in `lib/<domain>/` (`types`, `constants`, `parsers`, `api`, `server`, `index`) and has no `services/` layer; Server Components call the domain's `server.ts` directly.

## Decision

Reference projects: SoGood Santé frontend for the `lib/<domain>` pattern; timesheet, cashpoint, laoka, and money-management for the rest of the Next.js conventions (the starter's `nextjs.md` was already a superset of theirs).


Next.js projects structure domain code as modules under `src/lib/<domain>/`, with a barrel that never re-exports the server-only `server.ts`, defensive parsers as the trust boundary for API data, and non-throwing `api.ts` calls. There is no `services/` folder. Constants live in `src/lib/<domain>/constants.ts` or, when shared (including app identity and `NEXT_PUBLIC_*` values), in `src/lib/shared/constants.ts`; there is no `src/constants/` folder. Zod `schemas/` for forms are unchanged.

## Why not something else

- **Keep `services/` for Server Components**: rejected because it duplicates the domain's data access next to `lib/` and splits one domain over several folders.
- **Put types and constants in global `src/types/` and `src/constants/`**: rejected because colocating them with the domain's parsers and API keeps each domain self-contained.
- **Re-export `server.ts` from the barrel**: rejected because Client Components import the barrel and would pull server-only code into the browser bundle.

## Consequences

- Positive: one place per domain, clear server/client boundary, parsers are pure and easy to test first under TDD.
- Negative / risk: existing projects built on `services/` need a migration; the recipe tree and conventions changed accordingly.
