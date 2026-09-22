# AI Workflow Entrypoint

Start here. Read the files below in order before writing any code.

> **Project not initialized yet?** If `project-overview.md` or `ui-context.md` still contain `[bracketed]` placeholders, stop and run `/init-project` before proceeding.

> ⛔ **Absolute Directive**: before anything else, read the "Absolute Directive" section at the top of `.context/coding-conventions/global.md` - think before coding, simplicity first (the 7-rung ladder), surgical changes with root-cause fixes, goal-directed execution. It is the foundation every other rule, command, skill, and spec here is expected to already embody; if you find something that contradicts it, that instruction is the bug - flag it instead of picking a side.

---

## 0. Framing - once per project

Before the first `/spec` on a brand-new project, run `/prd` → `/architect` → `/design-system` (skip the last one for projects with no UI layer) to establish the product perimeter, reconcile `architecture.md` with what's actually in the code, and - for UI projects - lock design tokens and audit contrast once. This only needs to happen once per project: established projects that already have `.context/framing/prd.md` can skip straight to `/spec`.

---

## 1. Mandatory read - every session, before any code

| File | What it gives you |
| --- | --- |
| `.context/project-overview.md` | What the app does, goals, features, scope |
| `.context/architecture.md` | Stack, folder structure, invariants, system boundaries |
| `.context/project-settings.md` | Project-specific settings: merge mode, target branch, test/typecheck commands - see the file's own header for what each means |
| `.context/coding-conventions/global.md` | Golden rules, cross-cutting concerns - **non-negotiable** |
| `.context/coding-conventions/security.md` | Trust boundaries, auth, webhooks, secrets, CORS - **non-negotiable** |
| `.context/progress-tracker.md` | Current phase, completed work, open questions |
| `.context/ai-workflow-rules.md` | Scoping rules, TDD mandate, protected files, doc-sync policy |
| `.context/adr/README.md` | What the ADR/context memory system is and how to use it |
| `.context/memory/MEMORY.md` | Behavioral memory index - corrections, validated approaches, ongoing project facts. Protocol in `.context/memory/README.md` |

**Before making a structural call** (architecture, process, tooling, convention) in an area you haven't touched yet this session: check `.context/adr/context/<Subject>.md` if it exists, and check `.context/adr/decisions/` for anything relevant. Never contradict a `status: accepted` decision without flagging it to the user first. Full read/write protocol - automatic, no command - in `.context/adr/README.md`.

## 2. Mandatory read - only when touching UI code

| File | What it gives you |
| --- | --- |
| `.context/ui-context.md` | Design tokens, layout decisions |

Also determine this project's actual stack from `.context/architecture.md`, then read whichever files under `.context/coding-conventions/` match the languages/frameworks you're about to touch (the folder holds one file per stack the starter supports - e.g. `typescript.md`, `react.md`, `nextjs.md`, `tailwind.md`, `ui.md`, `php.md`, `symfony.md`, `javascript.md`, `twig.md`, `stimulus.md` - only some of these apply to any given project).

## 3. Mandatory read - only when touching server/backend code

Same rule as above: check `.context/architecture.md` for the actual folder layout and stack, then read the matching `.context/coding-conventions/*.md` files.

## 4. Mandatory read - only when touching infrastructure (deploy config, env vars, hosting)

| File | What it gives you |
| --- | --- |
| `.context/infra.md` | Runtime, env vars, routing, deploy, known gotchas |

**SSH access to prod** (if applicable): check `.context/infra.md` for the host alias/connection details set up for this project. Prefer a configured alias over a raw `ssh root@<ip>`.

---

## 5. Workflow gates

Two paths depending on scope:

### Quick path - small fixes, bugs, debug, typos

```
(no command needed) → write code directly
```

Qualifies as quick if **all** of the following are true:
- Touches ≤ 3 files
- No new feature, no API contract change, no DB migration
- Can be described in one sentence
- **No spec is currently `status: in-progress`** - if one exists, run `/review-spec-implementation` first

Just write the fix. No spec required.

> ⛔ **MANDATORY, not optional**: the instant the fix is written, launch `/review-changes` and `/review-security` in subagents (each command delegates to its own specialized subagent internally - see its Step 0.5) - in the same turn, before reporting the change as done, before committing, before answering anything else the user asked. This is the single most-skipped step of the quick path precisely because nothing else enforces it (see the note below) - if you notice mid-turn (or after) that you wrote quick-path code without launching both, stop and launch them now, retroactively, before doing anything else.

**This path has no command, so no scaffolding enforces anything else on it - the Absolute Directive in `.context/coding-conventions/global.md` (think before coding, simplicity ladder, surgical changes, goal-directed execution, ponytail lazy-senior-dev-mode) is the *only* thing governing it beyond those two reviews, and it is non-negotiable regardless.**

Anything past the thresholds above (more files, a new feature, an API contract change, a DB migration) is not "quick" - go through the feature path below instead, even for something that doesn't feel big enough for a full spec.

### Feature path - anything consequent

```
/spec → /implement
```

`/implement` is the recommended entry point - it runs `/dev`, `/review-spec-implementation`, `/review-changes`, and `/review-security` in a self-correcting loop (up to 5 iterations) and marks the spec done once everything checks out. The individual commands below still exist and are what `/implement` calls under the hood - reach for one directly for a narrower job (e.g. re-running `/review-security` alone after a manual edit), but the rules in the table apply either way.

Each spec gets its own dedicated worktree, `.worktrees/<NNN-slug>/` on branch `feature/<NNN-slug>` - `/dev` creates it, every command after that resolves it rather than assuming the session's own working directory is inside it, and `/commit-and-push` removes it once the spec is proven merged. See `.context/commands/dev.md` for the exact mechanics.

| Rule | Detail |
| --- | --- |
| No code without a spec | Never write feature code without a spec in `.context/feature-specs/` with `status: todo` or `status: in-progress`. Run `/spec` first. |
| No `/dev` with pending `/review-spec-implementation` | Before starting `/dev` on any spec, check `.context/feature-specs/` for specs with `status: in-progress` that have unchecked acceptance criteria (`- [ ]`). If any exist, run `/review-spec-implementation` on them first. |
| `/review-spec-implementation` owns `done` | Only `/review-spec-implementation` may set `status: done` on a spec. `/dev` never marks a spec done. |
| Always finish with `/review-security` | Run `/review-security` after `/review-spec-implementation` on any change touching auth, user input, secrets, an API endpoint, a webhook, or payment - and by default on every feature. `/implement` runs it automatically at the end of its loop. |
| `/spec` is always allowed | You may run `/spec` at any time regardless of pipeline state. |

**Before writing feature code**, check the current pipeline state:
1. List all specs in `.context/feature-specs/`.
2. If any spec is `status: in-progress` with unchecked criteria → tell the user and suggest `/review-spec-implementation` before proceeding.
3. If no spec covers the requested change → tell the user and suggest `/spec` first.

---

## 6. How to work

See `.context/ai-workflow-rules.md` - scoping rules, protected files, doc sync policy, and the checklist to complete before moving to the next unit.

---

## 7. Maintaining commands, hooks, and subagents

**All commands and hooks must be agent-agnostic**: the logic lives in `.context/` and is mirrored to every tool directory. Never add logic only to one tool's folder.

Command logic lives in `.context/commands/` - that is the single source of truth.

Each tool has thin wrapper files that delegate to the shared source:

| Tool | Commands | Hooks / Rules | Specialized subagents |
| --- | --- | --- | --- |
| Claude Code | `.claude/commands/` | `.claude/settings.json` + `.claude/hooks/` | `.claude/agents/` |
| opencode | `.opencode/commands/` | - | `.opencode/agents/` |

One hook isn't per-tool: **`.githooks/pre-commit`** is a plain git hook, activated once per clone with `git config core.hooksPath .githooks` (done by `/init-project`). It enforces the same "no code on a `feature/<slug>` branch without its spec" rule as `.claude/hooks/enforce-spec-pipeline.sh`, but at the git level - it holds regardless of which tool (or none) is committing, so it isn't mirrored per-tool and never goes in the table above.

**When the user asks you to modify a command**, you MUST propagate the change to all tool directories in the same operation:

- Edit the source in `.context/commands/` first
- Mirror to `.claude/commands/` (add `allowed-tools` frontmatter if needed)
- Mirror to `.opencode/commands/`

**Specialized subagents have no shared `.context/` source** - each tool defines them natively (`.claude/agents/*.md` with `tools:` frontmatter, `.opencode/agents/*.md` with `mode: subagent` + `permission:` frontmatter). The delegation instructions that reference them (e.g. "launch a subagent specialized for implementation work, agent type: `implementer`") live in `.context/commands/` and stay tool-agnostic - they name the agent generically and fall back to a general subagent if the tool doesn't support named types.

**When the user asks you to add or modify a specialized subagent**, propagate to every tool's native format in the same operation, keeping the persona, rules, and tool/permission restrictions equivalent across formats:

- Create/update `.claude/agents/<name>.md`
- Create/update `.opencode/agents/<name>.md`
- If new, add its name to the relevant delegation step(s) in `.context/commands/`

**When the user asks you to modify a hook**, update `.claude/hooks/<hook>.sh` (Claude Code). If the hook is new, create the file.
