---
description: "Set up the starter's shared, agent-agnostic project context and workflow settings without choosing a stack"
argument-hint: "<optional context>"
---

You initialize the starter's shared project context. Stack and technical architecture decisions belong to `/architecture`, after product framing where applicable. This command is stack-agnostic and must not bootstrap the application.

## Phase 1 - Determine the project state

Ask whether this is a fresh project or an existing codebase being connected to the workflow. Inspect the repository and current `.context/` files before asking for information. Preserve useful project documentation and any non-placeholder settings.

`/architecture` can be run independently on an existing project with no `.context/`; in that architecture-only path it creates only `.context/architecture.md`. Use `/init-project` when the user wants the broader shared workflow initialized.

## Phase 2 - Collect only shared project information

Ask only for facts that cannot be inferred:
- Project display name and a stable project slug
- A short product objective and intended users
- Whether it has a user-facing UI and public pages; if relevant, whether public pages should be indexed
- For UI products: visual preferences already known (theme, colors, typography, layout, references)
- Optional design workspace URL, or `-`; a provider is never required because design references can be local
- Existing GitHub repository URL if one exists; do not create a repository unless the user explicitly asks
- Target branch when it cannot be inferred from repository configuration or `origin`
- Test and typecheck commands when they cannot be inferred; use `-` if not applicable (test technologies per layer are chosen later in `/architecture`'s `## Testing` section)

Do not ask the user to decide a stack here. Do not collect stack-specific hosting, database, auth, port, or deployment details; `/architecture` handles those when selecting a new architecture.

Inspect the configured Git remote and target branch with read-only Git commands when available. The workflow does not require GitHub CLI because it creates no pull requests. The `origin` remote must exist before `/commit-and-push` can push; do not add or change a remote without the user's request.

## Phase 3 - Populate shared context

Update the starter's shared context files while preserving non-placeholder, project-specific content:
- `.context/project-overview.md`: identity, objective, audience, goals, core flow, scope, and success criteria; leave unanswered product details explicit rather than invented.
- `.context/project-settings.md`: target branch, optional `Design workspace URL:`, and test/typecheck commands. Keep one temporary feature branch and worktree per spec. `/implement-queue` (in series) and `/implement-swarm` (in parallel) may coordinate multiple spec worktrees autonomously through a resumable local batch manifest; both single and batch flows hand reviewed changes to the local target branch without pull requests.
- `.context/ui-context.md`: record only visual preferences the user knows. Leave implementation-derived tokens and component details for `/design-system` after the UI architecture exists.

If a relevant file is missing, create only that shared context file from the starter's format. Do not overwrite custom non-placeholder content. Record the supplied repository URL in the appropriate project context if the current template has a suitable field; otherwise report it without adding a new schema just for the URL.

Activate the shared git hook only when `.githooks/pre-commit` exists and the repository does not already use a different hooks path:

    git config core.hooksPath .githooks

Do not edit `.context/architecture.md` or `.context/infra.md`; architecture and approved stack-specific setup own those files. Do not change application source, manifests, environment files, CI, infrastructure, hosting, or deployment. Do not install dependencies, scaffold a stack, generate a recipe, remove `.context/stacks/`, or prune coding conventions. Keep the available stack recipes and conventions intact for `/architecture` and later project work.

## Phase 4 - Hand off

Report the context/settings created or updated and any unknowns. For a fresh project, recommend this manual sequence:

1. `/prd` to settle the product perimeter.
2. `/architecture` to choose and document the technical architecture.
3. Apply the approved stack-specific setup as a separate step.
4. `/design-system` for a UI project once its UI stack and tokens exist.

For an existing project, `/architecture` may be run before or after this command; if the user only wants the architecture documented, use `/architecture` directly. Commands are separate and never chain automatically. Never commit or push.

Shared initialization is complete for `/spec` only when `.context/project-overview.md` records the actual project name, a project-specific Overview, goals, core flow, scope, and success criteria, with no unresolved starter placeholders anywhere in the file. `.context/project-settings.md` must have a concrete `Target branch:`, `Design workspace URL:`, `Test command:`, and `Typecheck command:` entries. A dash is valid for the optional URL or commands when they do not apply. Completing this command alone does not make a project ready for `/spec`; the PRD, architecture, and UI design system (for UI projects) must also pass `/spec`'s framing gate.
