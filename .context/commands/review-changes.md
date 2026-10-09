---
description: "Review all local changes (tracked + untracked) against project conventions and fix violations. Args: frontend | backend | all"
argument-hint: "frontend | backend | all"
---

You are a strict code reviewer. Your job is to collect every locally modified or new file in the declared scope, check them against the project's conventions, and fix all violations in-place.

## Scope

Argument: `$ARGS`

Check `.context/architecture.md` for this project's actual layer folders (frontend/UI vs. server/backend), then apply:

- `frontend` → only files inside the UI layer's folder
- `backend` → only files inside the server/backend layer's folder
- `all` → files in both layers
- **Never touch** infra/config folders, `.claude/`, `.opencode/`, `.github/`, or any file outside the declared scope.

## Step 1 - Delegate the review to a specialized subagent

If you were spawned by another command to execute only a subset of these steps, skip this delegation and go straight to Step 2.

Otherwise, launch a subagent specialized for convention review (agent type: `convention-reviewer`, if your tool supports named subagent types - otherwise a general coding subagent) to resolve the correct worktree and execute Steps 2 through 7 below with the declared scope. Wait for its summary table, then continue to Step 8.

---

## Worktree resolution (before Step 2)

If this review was spawned with a valid batch context, use only the exact assigned spec worktree from its manifest, or the exact integration worktree when the parent requests a combined batch review. Do not scan or modify another batch worktree. If an incomplete batch exists but no valid batch context was supplied, stop and direct the user to `resume <batch-id>` on the command that started it (`/implement-swarm` or `/implement-queue`); do not guess which diff to review.

Outside batch mode, if the current checkout is already on `feature/<spec-id>`, review that checkout. Otherwise, inspect the specs and `git worktree list`: if exactly one `status: in-progress` or `status: done` spec has an active `.worktrees/<spec-id>/` on its matching feature branch, run every Git command and apply every fix in that worktree (`git -C .worktrees/<spec-id>/ ...`). If more than one matches, ask which spec to review. If none matches, review the current checkout's local changes; after a completed spec handoff, those changes are on the local target branch.

## Step 2 - Load conventions

Read the convention files that apply to the declared scope:

- Always read `.context/coding-conventions/global.md` (cross-cutting rules), `.context/coding-conventions/security.md` (trust boundaries, auth, webhooks, secrets, CORS), and `.context/architecture.md` (file/module placement rules can live here rather than in a coding-convention file, and are just as much a rule as anything in those files)
- Whichever layers are in scope, also read the `.context/coding-conventions/*.md` files matching that layer's actual languages/frameworks per `.context/architecture.md` (e.g. `typescript.md`/`nextjs.md`/`react.md`/`tailwind.md`/`ui.md`/`html.md` for a UI layer, `php.md`/`symfony.md`/`javascript.md` for a server layer - only some of these exist for any given project)

## Step 3 - Collect changed files

Run all three commands and union the results:

```bash
git diff HEAD --name-only          # tracked, unstaged changes
git diff --cached --name-only      # tracked, staged changes
git ls-files --others --exclude-standard  # untracked (new) files
```

Filter to only files inside the declared scope folders.

If there are no files at all in scope, report "No changes in scope" and stop.

## Step 4 - Static analysis

Run the static analysis / lint command for each in-scope layer that has changed files, per `.context/architecture.md` (or the project's stack file under `.context/stacks/`) - e.g. `composer phpstan` for a Symfony backend, `pnpm lint` for a Next.js frontend. Fix every reported error before continuing. Do not suppress errors (baseline entries, `@phpstan-ignore`, `eslint-disable`, etc.) unless the user explicitly approves it.

## Step 5 - Analyze violations

For each changed file in scope, read the full file and check it against every rule in the convention files you loaded in Step 2 - read them in full, don't rely solely on their "Quick Reference" tables, which are abbreviated indexes, not complete rule sets. Do not maintain a separate checklist here that duplicates their content - if you need a reminder of what to check, re-open the relevant convention file rather than trusting a paraphrase that can silently drift out of sync with it.

Placement rules (e.g. `nextjs.md`'s "pure helper functions belong in `src/lib/utils.ts`, even if only one file uses it today") need an active check, not a passive one: reading a file top to bottom for style issues will not surface "this function is in the wrong file" unless you specifically ask that question of every function definition you pass. Ask it.

Also check tests against `.context/coding-conventions/tdd.md`: every changed unit in the strict TDD scope (business logic) has a test, while simple CRUD, serialization groups, trivial utilities, and config need none; tests assert observable behavior rather than mirror the implementation or mock the code under test; no test was weakened to pass; no production code exists that no test or spec requirement justifies. Missing or behavior-less tests are violations to fix by adding or correcting the tests (one criterion at a time), not by skipping.

## Step 6 - Fix violations

For each violation found:
1. State clearly: **file**, **line(s)**, **rule violated**, **what you're changing**.
2. Apply the fix.
3. Do not refactor unrelated code. Touch only what violates the rules.

## Step 7 - Summary

After all fixes, output a concise table:

| File | Violations found | Fixed |
|------|-----------------|-------|
| ...  | ...             | ✅/❌  |

If nothing was wrong, say so explicitly.

---

## Step 8 - Manual check reminder

If this review was spawned with a valid batch context, return the summary table to the parent orchestrator and stop. Do not message the user or perform a target-branch handoff; the orchestrator owns batch review and handoff.

Tell the user:
> Before committing, do a quick manual scan of the diff (`git diff HEAD`) to catch anything automated review may have missed - dead code, stray debug logs, TODO comments, or anything that looks off.
> I will not commit or push after this review. Only your direct invocation of `/commit-and-push` authorizes those actions.
