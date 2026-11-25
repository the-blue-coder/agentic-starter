---
description: "Apply the approved stack-specific setup (scaffold, infra, environment) from the architecture decision and the matching stack recipe"
argument-hint: "<optional context>"
---

You apply the technical setup that `/architecture` approved: scaffold the application, write the infrastructure files, wire the environment and verify the result. `/init-project` never does this and `/architecture` only decides it. This command is the explicit, separate step between them.

Context, if any: `$ARGS`

## Phase 1 - Preconditions (read-only)

Read `.context/architecture.md`, `.context/project-overview.md`, `.context/project-settings.md`, the accepted architecture ADR in `.context/adr/decisions/`, and `.context/infra.md`.

Stop and name the missing command when:
- `.context/architecture.md` is not complete (concrete Stack, `Frontend` and `Testing` rows): run `/architecture`.
- The product framing in `project-overview.md` is missing: run `/prd`.
- Application source already exists (`backend/`, `frontend/` or equivalent manifests): this is an existing project. Use the recipe's existing-project part (when one exists) as a checklist, never overwrite application files, and ask before each change.

List `.context/stacks/`. A recipe is a reference, not a closed menu.

## Phase 2 - Plan and approval

Pick the recipe whose stack matches the Stack table. Then write a short plan and show it to the user:
- the recipe used (or "no recipe" when none fits, in which case the plan is derived from `architecture.md` alone and the missing parts are asked, never invented);
- every **deviation**: anything in `architecture.md` or the ADR that differs from the recipe (another auth provider, an added service, a different storage). **`architecture.md` and its ADR always win over the recipe.** Adapt the recipe's steps accordingly, and report each place where a recipe step no longer applies;
- the local actions (scaffold, dependencies, config files) and the **outward-facing actions** (see Phase 4) it will need confirmation for.

Wait for the user's approval of the plan before any change.

## Phase 3 - Freshness check and inputs

Follow the recipe's freshness check: verify the current stable versions of the pinned tools with a quick web check, and use them rather than the pinned ones when they differ.

Collect the stack inputs the recipe asks for (its "information to collect" step), skipping every answer already in `architecture.md` (hosting target, domains, subdomain layout, server alias, API Platform mode, auth) and `project-overview.md`. Ask only what is still unknown. Never hardcode environment values: use `.env` files as `.context/coding-conventions/global.md` requires, and keep `.env.example` up to date.

## Phase 4 - Apply

Run the recipe's setup steps in order, adapted to the approved plan. Write the generated files following the project's coding conventions (including `global.md` indentation and layering rules). Write `.context/infra.md` with the real runtime, env vars, routing and deploy facts. Fill `Test command:` and `Typecheck command:` in `.context/project-settings.md` from the tools now installed.

**Outward-facing and hard-to-reverse actions need the user's explicit confirmation, one at a time, each time:** creating a GitHub repository, any write on the server over SSH (port registry, directories, secrets), creating or changing DNS records or mailboxes, creating secrets in third-party dashboards, the first deploy, and configuring backup or automation workflows. Read-only server lookups (for example reading the port registry) may be done directly. Never run a destructive command.

**Never commit and never push.** Where the recipe says "commit and push", leave the changes uncommitted and hand them off: only a direct `/commit-and-push` does that.

## Phase 5 - Verify

Prove the setup works with the checks that fit (for a container-based stack, every published port in the production compose file is bound to `127.0.0.1`, and after the first deploy `ss -tlnp | grep docker-proxy | grep -v 127.0.0.1` lists nothing for the app): dependencies install, the application builds and starts, the backend answers a health check, the frontend renders, the static analysis and typecheck commands run, and one test of each configured level passes. Fix what the setup broke. Report any check that could not be run and why; never claim a pass that was not observed.

Update `.context/architecture.md` only for statements the setup made false or concrete (for example `Unknown` values now settled, or exact folder names); do not redesign it. Record any structural deviation from the recipe in the architecture ADR or a new ADR, following `.context/adr/README.md`.

Finally, when `.context/stacks/` exists, ask: **Delete `.context/stacks/`? (yes / no)**. On yes, remove the whole folder: the project no longer needs the recipes, and everything stays recoverable from Git. Do not stage anything.

## Phase 6 - Hand off

Report what was created, the verification results, the deviations from the recipe, the confirmations that were skipped or declined, and what remains to do manually. Recommend `/setup-backup` next when the project has a database (it needs the backend deployed and its secrets in place), then, for a UI project, `/design-system`, now that the UI stack and its tokens exist. Commands are separate and never chain automatically. Never commit or push.
