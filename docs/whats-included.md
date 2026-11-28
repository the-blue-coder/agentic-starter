# What's included

- **`.context/`** - the project's persistent context: architecture, conventions, progress tracking, feature specs, and a small memory system for decisions and corrections. See `.context/ai-workflow-entrypoint.md` for the full read order.
- **`.context/project-settings.md`** - project-specific settings: target branch, optional design workspace URL, and the test/typecheck commands the pipeline runs. Each spec gets a temporary local worktree and branch; verified changes are reviewed on the local target branch. The workflow creates no PRs.
- **`.context/stacks/`** - stack-specific architecture and setup recipes. `/architecture` may consult them as examples after learning the product constraints; they are not a closed menu, and `/init-project` never selects or executes one. Apply an approved recipe with `/setup-stack` after the architecture decision; the recipe's last step deletes `.context/stacks/` once the setup is done.
- **`.context/coding-conventions/`** - shared rules plus language/framework guidance for supported stacks (Symfony API and Twig fullstack, Next.js, Gatsby, plus TDD, security, performance, and styling). Each stack file is modeled on a real reference project and describes its `src/` layout. Keep these reference files intact; read the ones matching the architecture documented in `.context/architecture.md`.
- **Commands and agents**, mirrored across tools (`.claude/`, `.opencode/`) so the workflow is the same regardless of which local coding agent you use:
  - `/init-project` → `/prd` → `/architecture` → `/setup-stack` (if needed) → `/setup-backup` (strongly recommended if there is a database) → `/design-system` for UI projects - framing before the first `/spec`
  - `/spec` → `/implement` - the feature pipeline (TDD implementation, spec verification, conventions, performance, security, and for SEO-flagged specs SEO review, looped until clean)
  - `/implement-queue` - autonomously implements several specs one after another, each on top of the previous verified result, and ends with a decision report
  - `/implement-swarm` - autonomously implements several independent specs concurrently, integrates their verified diffs, and ends with a decision report
  - `/status` - shows the project's framing state and every spec's pipeline stage, derived entirely from files and read-only Git queries
  - `/review-changes`, `/review-performance`, `/review-seo`, `/review-security` - convention/performance/SEO/security sweeps over local changes (`/review-seo` only on SEO-friendly projects)
  - `/init-project` - set up shared project context and workflow settings without choosing a stack
  - `/setup-backup` - database backup to S3, a strongly recommended step of the setup sequence for projects with a database (never blocks `/spec`, which reminds you)
  - `/setup-rolling-deploy`, `/teardown-rolling-deploy` - infra runbooks (currently only implemented for the `symfony-nextjs-contabo` recipe)
  - `/update-workflow` - updates an existing project's workflow files (`.context/`, `.claude/`, `.opencode/`, git hooks) to the latest starter version and migrates legacy numeric specs to UTC IDs
  - `/commit-and-push`, `/add-new-color`, `/rebuild-tailwind`, `/just-respond`, `/update-starter`
- **`infra/`** - reference deploy scripts and nginx configurations for the supported stack recipes; stack-specific setup is applied separately.
- **`.github/workflows/`** - CI/CD examples matching the current stack recipes; they are not installed or selected by `/init-project`.
- **`.githooks/pre-commit`** - a plain git hook (not tool-specific): refuses a commit on a `feature/<spec-id>` branch unless that spec exists and `/dev` has picked it up. The normal workflow transfers reviewed changes to the target branch before the user-authorized commit. Activated once per clone when `/init-project` initializes the shared workflow (`git config core.hooksPath .githooks`), so it applies regardless of which AI tool is committing.

**Commit and push require a direct user command.** `/spec`, `/dev`, `/implement`, `/implement-queue`, `/implement-swarm`, quick fixes, and reviews never commit, push, or invoke the commit-and-push command automatically. Only when you directly call `/commit-and-push` does the agent run its commit and push workflow.
