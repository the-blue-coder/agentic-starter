---
name: project_convention_reference_projects
description: Which real projects are the reference models for each stack's coding conventions and src layout.
metadata:
  type: project
  confidence: high
---

Reference projects under `D:\Me\Projects\` for the starter's coding conventions: Symfony API Platform = `freelance/spontaneit/sogoodsante/backend`; Symfony fullstack Twig = `freelance/spontaneit/oai`; Gatsby = `freelance/spontaneit/archipiade`; Next.js = `mine/timesheet`, `mine/cashpoint`, `mine/laoka`, `mine/money-management`, with the `lib/<domain>` pattern from `freelance/spontaneit/sogoodsante/frontend`.

**Why:** The user wants conventions grounded in real code. Next.js has no `services/` or `src/constants/`: server data access lives in `lib/<domain>/server.ts`, constants in `lib/<domain>/constants.ts` or `lib/shared/constants.ts`. Ownership scoping uses `OwnedByUserInterface` + `CurrentUserOwnershipExtension` (sogoodsante), not a class-string list.

**How to apply:** When changing a stack's conventions or recipe tree, check the matching reference project first. Gatsby keeps its own `src/constants/`. See [[feedback_batch_autonomy_and_tdd]].
