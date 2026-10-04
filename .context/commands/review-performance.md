---
description: "Review pending local changes for performance problems introduced by the diff (queries, loops, rendering, dependencies, I/O) and fix violations in-place"
argument-hint: ""
---

You are a strict performance reviewer. Your job is to collect every locally modified or new file, check the code it introduces against this project's performance conventions, and fix real, demonstrable costs in-place. Never optimize speculatively: a finding needs a concrete cost the diff introduces.

## Step 1 - Delegate the review to a specialized subagent

If you were spawned by another command to execute only a subset of these steps, skip this delegation and go straight to Step 2.

Otherwise, launch a subagent specialized for performance review (agent type: `performance-reviewer`, if your tool supports named subagent types - otherwise a general coding subagent) to resolve the correct worktree and execute Steps 2 through 6 below. Wait for its summary table, then continue to Step 7.

---

## Worktree resolution (before Step 2)

If this review was spawned with a valid batch context, use only the exact assigned spec worktree from its manifest, or the exact integration worktree when the parent requests a combined batch review. Do not scan or modify another batch worktree. If an incomplete batch exists but no valid batch context was supplied, stop and direct the user to `resume <batch-id>` on the command that started it (`/implement-swarm` or `/implement-queue`); do not guess which diff to review.

Outside batch mode, if the current checkout is already on `feature/<spec-id>`, review that checkout. Otherwise, inspect the specs and `git worktree list`: if exactly one `status: in-progress` or `status: done` spec has an active `.worktrees/<spec-id>/` on its matching feature branch, run every Git command and apply every fix in that worktree (`git -C .worktrees/<spec-id>/ ...`). If more than one matches, ask which spec to review. If none matches, review the current checkout's local changes; after a completed spec handoff, those changes are on the local target branch.

## Step 2 - Load performance conventions

Read `.context/coding-conventions/performance/global.md` first, plus `.context/architecture.md` to learn the actual stack. Then read the files in `.context/coding-conventions/performance/` matching the languages and frameworks of the changed files (`typescript.md`, `javascript.md`, `react.md`, `nextjs.md`, `gatsby.md`, `php.md`, `symfony.md`, `twig.md`, `stimulus.md` - only some apply to any given project). A stack file applies on top of the base language files it names.

## Step 3 - Collect changed files

Run all three commands and union the results:

```bash
git diff HEAD --name-only          # tracked, unstaged changes
git diff --cached --name-only      # tracked, staged changes
git ls-files --others --exclude-standard  # untracked (new) files
```

If there are no files at all, report "No changes to review" and stop.

## Step 4 - Applicability check

Review only the code the diff introduces or modifies, not pre-existing code. The review applies when the diff contains at least one of:

- a database query or a network/API call
- a loop or any processing of a collection
- UI rendering code (components, templates, client-side event handling)
- an added or changed dependency or import
- file, stream, or large-payload handling

If none of these appear, report "Not applicable - the diff contains none of: query/network call, loop/collection processing, UI rendering, dependency change, file handling" and stop. Do not make this call on a hunch: the list above is closed.

## Step 5 - Analyze violations

For each changed file with an applicable construct, read it in full and check the introduced code against the conventions loaded in Step 2. Do not keep a separate checklist here; re-open the convention files rather than trusting a paraphrase that can drift.

Only report a violation when you can state the concrete cost (for example "one query per order in the loop at line 42") and a bounded fix. Skip code marked with a `shortcut:` comment that names its ceiling and upgrade path, and cold paths where the cost cannot grow. When the right fix needs a product decision (page size, cache TTL, async queue choice), flag it with the options instead of choosing silently.

## Step 6 - Fix violations and summarize

For each violation found:
1. State clearly: **file**, **line(s)**, **rule violated** (the convention file and rule), the **cost**, and **what you're changing**.
2. Apply the smallest fix that removes the cost, preserving behavior. If the fix changes a query or contract, add or adjust the covering test per `.context/coding-conventions/tdd.md`.
3. Do not refactor unrelated code or restructure layers. Touch only what violates a performance rule.

After all fixes, output a concise table:

| File | Violations found | Fixed |
|------|-----------------|-------|
| ...  | ...             | ✅/❌  |

If nothing was wrong, say so explicitly. List any flagged decisions that need the user.

---

## Step 7 - Manual check reminder

If this review was spawned with a valid batch context, return the summary table to the parent orchestrator and stop. Do not message the user or perform a target-branch handoff; the orchestrator owns batch review and handoff.

Otherwise tell the user:
> Automated review cannot measure real load. For anything on a hot path, profile or load-test before relying on this result.
> I will not commit or push after this review. Only your direct invocation of `/commit-and-push` authorizes those actions.

This command never performs the target-branch handoff; `/review-security` runs last and owns it.
