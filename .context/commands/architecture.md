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
- `.context/framing/prd.md` if it exists
- `.context/project-overview.md` if it exists
- `.context/architecture.md`
- List `.context/stacks/` recipe filenames and short descriptions. Read a candidate recipe reference architecture only when useful; do not load its long setup steps. Recipes are examples, not a closed menu.
- relevant accepted ADRs under `.context/adr/decisions/`

If there is no PRD, ask the user whether to run `/prd` first or gather the missing product constraints here. Do not assume a stack from a recipe or from the starter's own stack.

### Explore and recommend

Use the PRD, project constraints, available team skills, expected scale, deployment needs, budget, and user preferences to recommend a suitable architecture. Ask only questions whose answers could change the recommendation. Explain meaningful options and trade-offs in plain language, including:
- backend and frontend approach, or why one is not needed
- language, framework, data store, and hosting/deployment model
- authentication and external integrations when relevant
- the main module/layer boundaries and expected repository layout
- operational constraints and delivery requirements
- the test technologies for each layer (unit, integration/API, frontend logic, components, and Playwright e2e for user-facing UI), chosen to fit the stack and the TDD loop in `.context/coding-conventions/tdd.md`

Recipes under `.context/stacks/` are examples, not a closed menu. A recipe is not selected or executed by `/init-project`. Do not scaffold the application, install dependencies, configure CI or infrastructure, deploy, remove recipes, or prune coding conventions here.

Present the recommendation and wait for the user's approval before recording it as the chosen architecture. After approval, create/update `.context/architecture.md` using its existing sections: Stack, Testing, Repo Structure, Key Invariants, System Boundaries, Storage Model, Auth and Access Model, and Project-Specific Invariants. Replace placeholders with concrete decisions; make unknowns explicit instead of inventing answers. Always fill every row of the `Testing` table with a concrete tool, location, and command, or `None` with the reason; a blank or placeholder row is incomplete because `/spec` blocks on it. Always fill the `Frontend` row in the Stack table: name the actual user-facing UI stack, or write `None` (or `-`) when the project has no user-facing UI. Never leave the row blank or use a placeholder, because `/spec` relies on it to decide whether `/design-system` is required.

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

Do not edit coding conventions or application code. Report any convention drift separately. If the project has a UI, recommend `/design-system` only when its real stack and tokens are available.

When running in the existing-project, architecture-only mode described in Phase 1, the only created file must be `.context/architecture.md`.

## Completion report

Summarize what was documented, what could not be inferred, and the next useful command. For a newly approved architecture, mention that applying its stack-specific bootstrap is a separate, explicit step. Never commit or push.
