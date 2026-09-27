---
description: "Implement a feature from its spec in .context/feature-specs/"
argument-hint: "<spec number or name fragment>"
---

Pick up and implement a feature from its spec.

Do not commit or push the implementation. Only a later, direct user invocation of `$commit-and-push` (Codex) or `/commit-and-push` (other tools) authorizes those actions; this command must not invoke it automatically.

Spec to work on (optional - skip to show the menu): `$ARGS`

---

## Step 1 - Load project context (silent)

Read:
- `.context/ai-workflow-entrypoint.md`
- `.context/project-overview.md`
- `.context/architecture.md`
- `.context/coding-conventions/global.md`
- `.context/coding-conventions/security.md`

---

## Step 2 - Find specs

List all files in `.context/feature-specs/` and read the `status:` frontmatter field from each.

**If the directory is empty or no files have `status: todo` or `status: in-progress`:**
> No specs to implement. Run `/spec` first to define a feature, then come back.
Stop.

**If `$ARGS` is provided**, find the matching spec (by numeric prefix or name fragment, case-insensitive) and jump to Step 4.

**Otherwise**, display the menu in two sections:

```
▶ In progress
  1. 002 - Feature name

◦ Todo
  2. 001 - Feature name
  3. 003 - Feature name
```

Ask: **Which feature do you want to implement? (enter a number)**
Wait for the answer.

---

## Step 3 - Show the spec summary

Read the chosen spec file. Display:
- Title and goal
- Acceptance criteria (checklist)
- Scope: Frontend / Backend / Full-stack (inferred from the spec)

Ask: **Ready to start? (yes / no)**
Wait for confirmation.

---

## Step 4 - Mark in progress

Update the spec file's frontmatter: `status: todo` → `status: in-progress`.

Also update `.context/progress-tracker.md`: move the feature from **Next Up** to **In Progress** if it isn't already there.

---

## Step 4.5 - Delegate implementation to a specialized subagent

If you were spawned by another command to execute only a subset of these steps, skip this delegation and go straight to Step 5 - the worktree setup at the top of Step 5 runs unconditionally either way, whoever invokes it.

Otherwise, launch a subagent specialized for implementation work (agent type: `implementer`, if your tool supports named subagent types - otherwise a general coding subagent). Since the subagent starts with a fresh context and does not inherit what you already read in Step 1, instruct it to first read `.context/project-overview.md`, `.context/architecture.md`, `.context/coding-conventions/global.md`, and `.context/coding-conventions/security.md`, then execute Steps 5 through 8.5. Give it the spec file path and the scope. Wait for its report (files created/modified, deviations, open questions), then continue to Step 9.

**Every command that runs after `/dev`** (`/review-spec-implementation`, `/review-changes`, `/review-security`, `/status`, `/commit-and-push`) resolves `.worktrees/<NNN-slug>/` itself and runs its git commands there (`git -C .worktrees/<NNN-slug>/ <command>`) rather than assuming the session's own working directory is inside it - the session invoking those commands is very often still sitting at the repo root.

---

## Step 5 - Load layer-specific context (silent)

**Worktree setup - the first thing this step does, no matter who invoked it (main `/dev` context, the delegated `implementer` subagent, or `/implement`'s own dev subagent):**

1. Check whether `.worktrees/<NNN-slug>/` already exists. If it does, `cd` into it and confirm it's on `feature/<NNN-slug>` (hard stop - tell the user - if it's on a different branch, detached HEAD, or missing entirely despite the directory existing; never `git switch`, `checkout`, or `stash` your way out of that state).
2. If it doesn't exist yet, read `Target branch:` from `.context/project-settings.md` (default to `main` if the file doesn't exist yet) and create it: `git worktree add .worktrees/<NNN-slug> -b feature/<NNN-slug> <target-branch>` (drop `-b` and just pass `feature/<NNN-slug>` if that branch already exists without a worktree). Then `cd .worktrees/<NNN-slug>/`.
3. Copy/symlink any untracked `.env*` files from the repo root into the worktree, and run the project's install command (per `.context/architecture.md`) if dependencies aren't already present there - a fresh worktree has none of the root's untracked or installed state.
4. Every remaining step (5 through 8.5) runs from inside `.worktrees/<NNN-slug>/`, not the repo root. One worktree per spec, one spec per worktree - if another spec's worktree exists with uncommitted changes, that's not this spec's problem and must not be touched.
5. Synchronize the selected spec from the repository root into the worktree so its latest requirements are included in the PR. If the spec file is missing in the worktree, copy it. If it exists and differs from the root copy, inspect the worktree's version and Git status for that path: update it only when the worktree copy has no local changes; if it has local changes, stop and report the conflict instead of overwriting either copy.
6. If the spec has `ui: true`, synchronize `.context/feature-specs/design/<NNN-slug>/` from the repository root into the same path in the worktree. Copy missing files. For a differing file, replace it only when it has no local worktree changes; otherwise stop and report the conflict. If the approved design reference is explicitly waived in the spec, preserve that note and continue without an export. Never execute exported HTML, scripts, or binaries.
7. Update only this feature's entry in the worktree's `.context/progress-tracker.md`: move it from **Next Up** to **In Progress**, or add it there if missing. Do not copy the entire tracker from the repository root, since it may contain another spec's uncommitted status.
8. Set the worktree spec's `status` to `in-progress`. Confirm the spec and, when applicable, its design export are present before implementation. The worktree copy is what will be included in this spec's PR.

Determine this project's actual layer folders and stack from `.context/architecture.md`, then based on the spec's scope:
- Touches the UI layer → read the matching files under `.context/coding-conventions/` (e.g. `typescript.md`, `nextjs.md`, `react.md`, `tailwind.md`, `ui.md`) and `.context/ui-context.md`
- Touches the server/backend layer → read the matching files under `.context/coding-conventions/` (e.g. `php.md`, `symfony.md`, `javascript.md`)
- Touches infra / env vars → read `.context/infra.md`

Then explore the codebase silently:
- Find the closest existing analog feature (entity, repo, service, page, hook) and read it.
- Identify which files will be created vs. modified.

---

## Step 6 - Implement

**TDD checkpoint - mandatory for critical business logic and bug fixes, no exceptions:** before writing a single line of implementation/fix code for a service, domain logic, or regression, write the failing test first, run it, and confirm it fails for the right reason. State this explicitly to the user (e.g. "Red: wrote failing test for X, confirmed failing") before moving on to the implementation. Skipping this step is a process violation, not a shortcut - see `.context/ai-workflow-rules.md`. Simple CRUD, UI components, and config keep the existing test-after convention.

The spec's **API Contract** table is a strict contract - implement exactly what's specified: method, route, request body fields (names, types, constraints), success status code, response shape, error responses, and auth. Do not add, remove, or rename fields.

Work through the spec systematically, in dependency order:
**backend entities and domain behavior → repositories (queries) → application services (use-case orchestration) → migrations → API → frontend schemas → hooks → components → pages**

For Symfony work, put a rule that protects one entity's state on that entity; keep application services for coordination and transaction boundaries. See `.context/coding-conventions/symfony.md` for the responsibility split and examples.

For each unit of work:
- Follow all conventions from `.context/coding-conventions/` strictly.
- Run required commands (migrations, `pnpm install`, etc.) as needed.
- After completing each acceptance criterion, check it off in the spec file:
  `- [ ] criterion` → `- [x] criterion`

Do not cut corners. Implement completely and correctly before moving on.

---

## Step 7 - Verify

Quick sanity check against whichever `.context/coding-conventions/*.md` files apply to this project's stack (see Step 5) - typical checks: no syntax issues, no hardcoded strings, no swallowed errors, no debug logging left behind, naming/placement conventions respected.

---

## Step 8 - Update CHANGELOG.md

Add one bullet under `## [Unreleased]` (create it if missing) following Keep a Changelog format (`Added` / `Changed` / `Fixed`). Describe the user-facing outcome, not the files touched.

---

## Step 8.5 - Write verification record

Run `git add -A` (stages everything without committing - the "never commit" rule is unaffected), then `git write-tree` to get a tree hash. Run the project's `Test command:` and `Typecheck command:` from `.context/project-settings.md` (skip either if its value is `-`). Write `.context/docs/verif/<NNN-slug>.md` (create the `.context/docs/verif/` folder if missing) recording: the tree hash, each command run with its exit code, and a timestamp. This lets `/review-spec-implementation` trust a clean run instead of re-executing the whole suite on unchanged code.

---

## Step 9 - Memory check

If the user corrected an approach or confirmed a non-obvious one during this implementation, and it isn't already recorded, write it to `.context/memory/` now, per `.context/ai-workflow-rules.md` → "Recording Feedback (Memory)".

---

## Step 10 - Hand off

Do NOT mark the spec as done yet - that's `/review-spec-implementation`'s job.

Tell the user:
- What was implemented (files created/modified).
- Any deviations from the spec, and why.
- Whether there are open questions left in the spec.

Then:
> Run `/review-changes` and `/review-security`, then `/review-spec-implementation` to check every acceptance criterion, data model, and API contract against the code before marking this spec done.
> If context is getting long, start a fresh session before running it.

---

## Rules

- Never mark a spec done before all acceptance criteria are checked off.
- Never invent behavior not described in the spec - add open questions instead.
- The user manages Git. Never commit or push here, even after successful implementation. Only the user's direct invocation of `$commit-and-push` (Codex) or `/commit-and-push` (other tools) authorizes those actions.
- Follow all conventions from `.context/coding-conventions/`. When in doubt, re-read them.
