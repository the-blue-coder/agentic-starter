> **To initialize a project from this starter, clone the repo and run:**
>
> ```
> /init-project
> ```

# agentic-starter

A stack-agnostic starter for building projects with an AI coding agent (Claude Code, opencode, or similar), following a **Spec-Driven Development (SDD)** workflow. It ships the agentic tooling layer only - no application code - so it works with whatever backend, frontend, and hosting you choose.

![Agentic starter pipeline overview: a framing stage that runs once, feeding into a per-spec cycle that repeats for every feature](https://files.madainsight.com/images/pipeline-overview.svg)

## What's included

- **`.context/`** - the project's persistent context: architecture, conventions, progress tracking, feature specs, and a small memory system for decisions and corrections. See `.context/ai-workflow-entrypoint.md` for the full read order.
- **`.context/project-settings.md`** - project-specific settings: merge mode (`pr` vs `local`), target branch, ship confirmation, and the test/typecheck commands the pipeline runs.
- **`.context/stacks/`** - ready-made **stack recipes**. Each one is a self-contained bootstrap + reference doc for a specific combination of backend, frontend, and hosting (e.g. `symfony-nextjs-contabo.md`). `/init-project` picks one, or helps you draft a new one if none fits - the library grows over time.
- **`.context/coding-conventions/`** - one file per language/framework (`global.md` and `security.md` apply to every project; the rest - `php.md`, `symfony.md`, `typescript.md`, `nextjs.md`, `react.md`, `javascript.md`, `tailwind.md`, `twig.md`, `stimulus.md`, `ui.md` - apply only if your chosen stack uses them). `/init-project` deletes the ones your chosen recipe doesn't pair with, so a real project only ever keeps what it actually needs.
- **Commands and agents**, mirrored across tools (`.claude/`, `.opencode/`) so the workflow is the same regardless of which CLI you use:
  - `/prd` → `/architect` → `/design-system` - framing, run once per project before the first `/spec`
  - `/spec` → `/implement` - the feature pipeline (implementation, spec verification, conventions, and security review, looped until clean)
  - `/status` - shows the project's framing state and every spec's pipeline stage, derived entirely from files and read-only git/gh queries
  - `/review-changes`, `/review-changes-security-spec` - convention/security sweeps over local changes
  - `/init-project` - bootstrap or wire up a project from a stack recipe
  - `/setup-backup`, `/setup-rolling-deploy`, `/teardown-rolling-deploy` - infra runbooks (currently only implemented for the `symfony-nextjs-contabo` recipe)
  - `/commit-and-push`, `/add-new-color`, `/just-respond`
- **`infra/`** - deploy scripts and nginx configs matching the current stack recipes; irrelevant/unused pieces get removed by `/init-project` once a stack is chosen.
- **`.github/workflows/`** - CI/CD workflow(s) matching the current stack recipes.
- **`.githooks/pre-commit`** - a plain git hook (not tool-specific): refuses a commit on a `feature/<slug>` branch unless that spec exists and `/dev` has picked it up. Activated once per clone by `/init-project` (`git config core.hooksPath .githooks`), so it holds no matter which AI tool - or none - is committing.

## AI Development workflow

Context and conventions live in `.context/` - start with `.context/ai-workflow-entrypoint.md` (also linked from `AGENTS.md`/`CLAUDE.md`).

**Two paths:**

**Quick fixes** (bugs, typos, small corrections - ≤ 3 files, no new feature): write code directly, no pipeline needed.

**Features**: framing once, then the per-spec pipeline repeats for every feature:

```
/prd → /architect → /design-system     (once, before the first /spec)
/spec → /implement                     (repeats, once per feature)
```

### Framing (once)

Run `/init-project` first if the project isn't bootstrapped yet - framing then picks up from an already-initialized `architecture.md`/`ui-context.md`. Framing itself runs before the first `/spec`, and again later only if the project has drifted from what's documented.

![Framing phase: /init-project first if the project isn't initialized yet, then /prd writes prd.md, /architect reconciles architecture.md, /design-system locks ui-context.md tokens for UI projects](https://files.madainsight.com/images/framing.svg)

| Command | What it does |
| --- | --- |
| `/init-project` | Only if the project isn't initialized yet - bootstraps `architecture.md`, `ui-context.md`, etc. from a stack recipe |
| `/prd` | Frames the product: problem, perimeter, out-of-scope, success criteria - writes `.context/framing/prd.md` |
| `/architect` | Reconciles `.context/architecture.md` and conventions with the real codebase |
| `/design-system` | UI projects only - locks design tokens and a contrast audit into `.context/ui-context.md` |

### Per-spec cycle

Each spec gets its own dedicated git worktree, `.worktrees/NNN-slug/` on branch `feature/NNN-slug` - one spec, one worktree, one branch, one PR. `/dev` creates it; every later command resolves it rather than assuming the session is already sitting inside it; `/commit-and-push` removes it once the spec is proven merged.

![Per-spec cycle: /spec (includes a design pass for UI specs), /dev, /review-spec-implementation, /review-changes, /review-security, then a manual hand-off to /commit-and-push, with /implement wrapping dev through review-security into one self-correcting loop](https://files.madainsight.com/images/spec-cycle.svg)

| Command | What it does |
| --- | --- |
| `/spec` | Clarifies requirements (includes a design pass for UI specs - no separate design command), writes a spec in `.context/feature-specs/` |
| `/implement` | Runs `/dev` → `/review-spec-implementation` → `/review-changes` → `/review-security` in series, looping (up to 5 iterations) until everything checks out, and marks the spec done |

`/implement` is the recommended entry point for a feature - it's `/dev`, `/review-spec-implementation`, `/review-changes`, and `/review-security` wired together into one self-correcting loop. It never commits or pushes: `/commit-and-push` is always a separate, manual step after `/implement` hands off. Each of the four stays available individually for a narrower job (e.g. running `/review-security` alone after a manual edit).

Specs live in `.context/feature-specs/` as markdown files with `status: todo / in-progress / done`. `/commit-and-push` pushes the spec's branch and opens a PR, or squash-merges locally into the target branch, depending on `Merge mode` in `.context/project-settings.md`. Run `/status` at any point to see where every spec stands.

## Getting started

Run `/init-project` (or read `INIT.md` directly) to either bootstrap a fresh project from a stack recipe, or wire an existing project into this structure.

## Built with

[Claude Code CLI](https://claude.ai/code)
