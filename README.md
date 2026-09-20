> **To initialize a project from this starter, clone the repo and run:**
>
> ```
> /init-project
> ```

# agentic-starter

A stack-agnostic starter for building projects with an AI coding agent (Claude Code, opencode, or similar), following a **Spec-Driven Development (SDD)** workflow. It ships the agentic tooling layer only - no application code - so it works with whatever backend, frontend, and hosting you choose.

## What's included

- **`.context/`** - the project's persistent context: architecture, conventions, progress tracking, feature specs, and a small memory system for decisions and corrections. See `.context/ai-workflow-entrypoint.md` for the full read order.
- **`.context/stacks/`** - ready-made **stack recipes**. Each one is a self-contained bootstrap + reference doc for a specific combination of backend, frontend, and hosting (e.g. `symfony-nextjs-contabo.md`). `/init-project` picks one, or helps you draft a new one if none fits - the library grows over time.
- **`.context/coding-conventions/`** - one file per language/framework (`global.md` and `security.md` apply to every project; the rest - `php.md`, `symfony.md`, `typescript.md`, `nextjs.md`, `react.md`, `javascript.md`, `tailwind.md`, `twig.md`, `stimulus.md`, `ui.md` - apply only if your chosen stack uses them).
- **Commands and agents**, mirrored across tools (`.claude/`, `.opencode/`) so the workflow is the same regardless of which CLI you use:
  - `/spec` → `/dev` → `/review-spec-implementation` → `/review-security` - the feature pipeline
  - `/review-changes`, `/review-changes-security-spec` - convention/security sweeps over local changes
  - `/init-project` - bootstrap or wire up a project from a stack recipe
  - `/setup-backup`, `/setup-rolling-deploy`, `/teardown-rolling-deploy` - infra runbooks (currently only implemented for the `symfony-nextjs-contabo` recipe)
  - `/commit-and-push`, `/add-new-color`, `/just-respond`
- **`infra/`** - deploy scripts and nginx configs matching the current stack recipes; irrelevant/unused pieces get removed by `/init-project` once a stack is chosen.
- **`.github/workflows/`** - CI/CD workflow(s) matching the current stack recipes.

## AI Development workflow

Context and conventions live in `.context/` - start with `.context/ai-workflow-entrypoint.md` (also linked from `AGENTS.md`/`CLAUDE.md`).

**Two paths:**

**Quick fixes** (bugs, typos, small corrections - ≤ 3 files, no new feature): write code directly, no pipeline needed.

**Features**: follow the pipeline:

```
/spec → /dev → /review-spec-implementation → /review-security
```

| Command | What it does |
| --- | --- |
| `/spec` | Clarifies requirements, writes a spec in `.context/feature-specs/` |
| `/dev` | Implements a spec, checks off acceptance criteria |
| `/review-spec-implementation` | Verifies every criterion against the code, marks the spec done |
| `/review-security` | Security review against `.context/coding-conventions/security.md` + a generic OWASP checklist |

Specs live in `.context/feature-specs/` as markdown files with `status: todo / in-progress / done`.

## Getting started

Run `/init-project` (or read `INIT.md` directly) to either bootstrap a fresh project from a stack recipe, or wire an existing project into this structure.

## Built with

[Claude Code CLI](https://claude.ai/code)
