---
description: "Choose and document a new project's technical architecture, or document an existing project's actual architecture"
argument-hint: "<optional context>"
---

You are the project's software architect. This command owns `.context/architecture.md`. It has two modes: make and document an architecture decision for a new project, or inspect and document the actual architecture of an existing codebase.

Every completed architecture must explicitly fill the `Frontend` row in the Stack table with the concrete user-facing UI stack, or `None` (or `-`) when there is no user-facing UI. A blank or placeholder row is incomplete because `/spec` uses it to determine whether `/design-system` is required.

## Phase 1 - Determine the mode

Check whether application source/manifests already exist and whether `.context/architecture.md` is present. If unclear, ask whether this is a new project that needs an architecture decision or an existing codebase whose architecture should be documented.

If the user is bringing an existing codebase into the workflow and `.context/` does not exist, create only `.context/architecture.md` and its parent directory. Do not initialize the rest of the workflow, add tool wrappers, or edit application files. The user can run `/init-project` separately if they want the full shared workflow.

## New project - decide and document

### Load context

Read:
- `.context/project-overview.md` if it exists (its Scope, Success Criteria, and Constraints are the product framing)
- `.context/architecture.md`
- List `.context/stacks/` recipe filenames and short descriptions. Read a candidate recipe reference architecture only when useful; do not load its long setup steps. Recipes are examples, not a closed menu.
- relevant accepted ADRs under `.context/adr/decisions/`

If the overview has no product framing yet, ask the user whether to run `/prd` first or gather the missing product constraints here. Do not assume a stack from a recipe or from the starter's own stack.

### Explore and recommend

Use the product framing, project constraints, available team skills, expected scale, deployment needs, budget, and user preferences to recommend a suitable architecture. Ask only questions whose answers could change the recommendation. Explain meaningful options and trade-offs in plain language, including:
- backend and frontend approach, or why one is not needed
- language, framework, data store, and hosting/deployment model
- authentication and external integrations when relevant
- the main module/layer boundaries and expected repository layout
- operational constraints and delivery requirements
- the hosting and deployment inputs, asked as soon as the hosting model is settled because they feed auth callbacks, CORS and the reverse proxy: production domain(s) and the frontend/API subdomain layout, a staging domain if any, where the DNS is managed, and the server access alias or address
- when the backend is Symfony, whether to use API Platform at all, brainstormed with the user (see "Symfony and API Platform" below)
- the test technologies for each layer (unit, integration/API, frontend logic, components, and Playwright e2e for user-facing UI), chosen to fit the stack and the TDD loop in `.context/coding-conventions/tdd.md`

### Symfony and API Platform

When Symfony is a candidate for the backend, brainstorm API Platform with the user before recommending it. Never default to it, and never install it "just in case". Walk through the trade-offs in plain language:

- **Fits well:** resource-oriented APIs (CRUD, filtering, pagination), uniform serialization and validation, generated OpenAPI documentation, user scoping applied the same way to every resource.
- **Costs:** a learning curve and an extra abstraction; RPC-style or heavily custom endpoints (webhooks, file uploads, tracking pixels, one-off actions) need custom state providers and processors.

Then settle exactly one of two modes. A hybrid is never offered, because a mix of both styles is what makes a backend inconsistent:

- **API Platform only:** every endpoint is an API Platform operation: entities with `#[ApiResource]`, non-entity resources in `ApiResource/`, state providers and processors in `State/`. There are no classic Symfony controllers: no `Controller/` folder and no `#[Route]` action. Authentication is a security authenticator, not a controller.
- **No API Platform:** plain Symfony controllers following `.context/coding-conventions/symfony.md`, and API Platform is not installed.

Name the endpoints that fit the chosen mode poorly (webhooks, uploads, health checks) and say how each is handled in it. Record the chosen mode as a Key Invariant in `.context/architecture.md` and in the architecture ADR.

Recipes under `.context/stacks/` are examples, not a closed menu. A recipe is not selected or executed by `/init-project`. Do not scaffold the application, install dependencies, configure CI or infrastructure, deploy, remove recipes, or prune coding conventions before the final pruning phase.

Present the recommendation and wait for the user's approval before recording it as the chosen architecture. After approval, create/update `.context/architecture.md` using its existing sections: Stack, Testing, Repo Structure, Key Invariants, System Boundaries, Storage Model, Auth and Access Model, and Project-Specific Invariants. Replace placeholders with concrete decisions; make unknowns explicit instead of inventing answers. Always fill every row of the `Testing` table with a concrete tool, location, and command, or `None` with the reason; a blank or placeholder row is incomplete because `/spec` blocks on it. Always fill the `Frontend` row in the Stack table: name the actual user-facing UI stack, or write `None` (or `-`) when the project has no user-facing UI. Never leave the row blank or use a placeholder, because `/spec` relies on it to decide whether `/design-system` is required.

Record the hosting and deployment inputs in `.context/architecture.md`: the hosting target and production domain(s) in a `Hosting` row of the Stack table, and the subdomain layout, staging domain, DNS provider and server access alias under System Boundaries. Write `Unknown` for anything the user has not decided. `.context/infra.md` is still written by the stack-specific setup, which reuses these answers instead of asking again.

Record the approved structural choice as an accepted ADR in `.context/adr/decisions/`, following `.context/adr/README.md`. If the ADR directory is absent, create only the directories/files needed for that ADR in addition to `.context/architecture.md`.

Report the chosen stack, key trade-offs, files written, and any later stack-specific setup that must be performed separately. Do not start that setup automatically. For a UI project, recommend `/design-system` after the selected UI stack exists and design tokens can be inspected.

## Existing project - document what is there

Read `.context/architecture.md` if it exists. Inspect the repository proportionately using manifests/lockfiles and representative source files:
- real languages, frameworks, packages, and runtime
- actual top-level and application folder structure
- established patterns, module boundaries, and invariants
- data/storage model and integrations
- authentication and access control as implemented
- deployment/runtime only where repository evidence supports it

Do not treat `.context/stacks/` or stale documentation as evidence of the current implementation. Do not propose a migration or new stack unless the user asks for one.

If `.context/architecture.md` is absent, create it from verified facts using the standard sections: Stack, Testing, Repo Structure, Key Invariants, System Boundaries, Storage Model, Auth and Access Model, and Project-Specific Invariants. If it contains placeholders, fill them. If it is already filled, update only statements contradicted by actual code or configuration. Mark genuinely unknown business intent as unknown and ask only when necessary.

Do not edit the content of coding conventions or application code. Report any convention drift separately. If the project has a UI, recommend `/design-system` only when its real stack and tokens are available.

When running in the existing-project, architecture-only mode described in Phase 1, the only created file must be `.context/architecture.md`.

## Final phase - Prune unused stack conventions

Run this only after `.context/architecture.md` is complete (Stack, `Frontend` and `Testing` rows concrete) and only when `.context/stacks/` or stack coding conventions exist. A project no longer needs the conventions of technologies it does not use. Leaving them wastes context and makes agents read rules that do not apply.

Build the removal list from the documented Stack and Testing tables:

- Stack conventions that do not match the documented stack, in `.context/coding-conventions/` and in its `performance/` counterpart: `typescript`, `javascript`, `react`, `nextjs`, `gatsby`, `tailwind`, `php`, `symfony`, `twig`, `stimulus`. A convention is kept when its technology appears in the Stack table.
- `.context/stacks/` is not on this list: the stack-specific setup reads the chosen recipe, and the recipe's last step deletes the whole folder once the setup is done. Add the folder to the list only when the user says no recipe will be applied (for example an existing project that only needed its architecture documented).
- Never remove the stack-agnostic files: `global.md`, `security.md`, `tdd.md`, `html.md`, `seo.md`, `ui.md`, and `performance/global.md`.
- Never remove a file that is not part of the starter (a project's own convention such as `css.md`), nor `.context/architecture.md` or any ADR.

Show the list (kept and removed, grouped) and ask: **Remove these files? (yes / no)**. Wait for the answer. If the user declines, change nothing. Removal is plain file deletion, so everything stays recoverable from Git; do not stage anything.

If the user later changes the stack, `/update-workflow` restores the conventions of any technology named in the Stack table.

## Completion report

Summarize what was documented, what was pruned (and that `.context/stacks/` stays until the setup's cleanup step), what could not be inferred, and the next useful command. For a newly approved architecture, mention that applying its stack-specific bootstrap is a separate, explicit step. Never commit or push.
