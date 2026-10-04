---
description: "Implement a feature from its spec in .context/feature-specs/"
argument-hint: "<spec ID, name fragment, or dropped spec file>"
---

Pick up and implement a feature from its spec.

When this workflow runs inside `/parallel-implement` / `/parallel-implement`, the parent supplies a batch ID and exact assigned worktree. Follow the batch-specific rules below: never create another worktree, never update the shared progress tracker or changelog, and leave the worktree intact for the parent integration.

Before a normal `/dev` run, inspect `.worktrees/.parallel-batches/`. If an incomplete manifest exists, stop and require `/parallel-implement resume <batch-id>` / `/parallel-implement resume <batch-id>`. Only a worker with a valid matching batch context may continue while that batch is active.

Do not commit or push the implementation. Only a later, direct user invocation of `/commit-and-push` authorizes those actions; this command must not invoke it automatically.

Spec to work on (optional - skip to show the menu): `$ARGS`

---

## Step 1 - Load project context (silent)

Read:
- `.context/ai-workflow-entrypoint.md`
- `.context/project-overview.md`
- `.context/architecture.md`
- `.context/coding-conventions/global.md`
- `.context/coding-conventions/security.md`
- `.context/commands/spec-selector-resolution.md`

---

## Step 2 - Find specs

List all files in `.context/feature-specs/` and read the `status:` frontmatter field from each.

**If the directory is empty or no files have `status: todo` or `status: in-progress`:**
> No specs to implement. Run `/spec` first to define a feature, then come back.
Stop.

**If `$ARGS` is provided**, resolve it using `.context/commands/spec-selector-resolution.md`, then jump to Step 4. A dropped spec file URI/path resolves to its exact spec ID after validation; text selectors continue to match by full filename stem or unambiguous name fragment, case-insensitive. New spec IDs use `yyyy_mm_dd_hh_ii_ss-spec-title`; legacy numeric IDs remain supported.

**Otherwise**, display the menu in two sections:

```
▶ In progress
  1. 2026_09_27_15_42_31-feature-name

◦ Todo
  2. 2026_09_26_11_05_00-feature-name
  3. 2026_09_28_09_30_12-feature-name
```

Ask: **Which feature do you want to implement? (enter a menu number, spec ID/name, or provide a local spec file)**
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

## Step 5 - Delegate implementation to a specialized subagent

If you were spawned by another command to execute only a subset of these steps, skip this delegation and go straight to Step 6 - the worktree setup at the top of Step 6 runs unconditionally either way, whoever invokes it.

Otherwise, launch a subagent specialized for implementation work (agent type: `implementer`, if your tool supports named subagent types - otherwise a general coding subagent). Since the subagent starts with a fresh context and does not inherit what you already read in Step 1, instruct it to first read `.context/project-overview.md`, `.context/architecture.md`, `.context/coding-conventions/global.md`, and `.context/coding-conventions/security.md`, then execute Steps 6 through 10. Give it the spec file path and the scope. Wait for its report (files created/modified, deviations, open questions), then continue to Step 11.

**Every review or status command that runs after `/dev`** (`/review-spec-implementation`, `/review-changes`, `/review-security`, `/status`) resolves `.worktrees/<spec-id>/` itself and runs its git commands there (`git -C .worktrees/<spec-id>/ <command>`) rather than assuming the session's own working directory is inside it. After the final handoff, `/commit-and-push` / `/commit-and-push` runs in the primary target checkout, where the user reviews the pending changes.

---

## Step 6 - Load layer-specific context (silent)

**Worktree setup - the first thing this step does, no matter who invoked it (main `/dev` context, the delegated `implementer` subagent, or `/implement`'s own dev subagent):**

If a batch ID was supplied by `/parallel-implement`, first verify the manifest lists this exact spec, worktree, branch, and base SHA. A batch worker must stop if the manifest is absent or disagrees with Git; it must never provision, switch, or clean up worktrees itself.

1. Resolve the selected spec's complete filename stem as `<spec-id>` (this also supports existing numeric IDs). Check whether `.worktrees/<spec-id>/` already exists. If it does, `cd` into it and confirm it's on `feature/<spec-id>` (hard stop - tell the user - if it's on a different branch, detached HEAD, or missing entirely despite the directory existing; never `git switch`, `checkout`, or `stash` your way out of that state).
2. If it doesn't exist yet, a normal `/dev` run reads `Target branch:` from `.context/project-settings.md` (default to `main` if the file doesn't exist yet) and creates it: `git worktree add .worktrees/<spec-id> -b feature/<spec-id> <target-branch>` (drop `-b` and just pass `feature/<spec-id>` if that branch already exists without a worktree). A batch worker must stop instead; only the orchestrator creates batch worktrees. Then `cd .worktrees/<spec-id>/`.
3. Copy/symlink any untracked `.env*` files from the repo root into the worktree, and run the project's install command (per `.context/architecture.md`) if dependencies aren't already present there - a fresh worktree has none of the root's untracked or installed state.
4. Every remaining step (6 through 10) runs from inside `.worktrees/<spec-id>/`, not the repo root. One worktree per spec, one spec per worktree. A batch worker may see other worktrees listed in the same valid batch manifest but must never read or modify their contents; any unlisted active worktree is a hard stop.
5. In batch-worker mode, use the exact spec copy the orchestrator synchronized before the first worker launch. Never resynchronize from the primary checkout; a resumed worker must preserve partial work. Stop if the assigned spec is missing. In normal mode, synchronize the selected spec from the repository root into the worktree so its latest requirements are included in the verified local handoff. If the spec file is missing in the worktree, copy it. If it exists and differs from the root copy, inspect the worktree's version and Git status for that path: update it only when the worktree copy has no local changes; if it has local changes, stop and report the conflict instead of overwriting either copy.
6. For batch workers, verify the assigned design references are present in the worktree and never copy them again; a resumed worker must preserve partial work. Stop if any required reference is missing. In normal mode, if the spec has `ui: true` and `.context/feature-specs/design/<spec-id>/` exists, synchronize the brief and references from the repository root into the same path in the worktree. Copy missing files. For a differing file, replace it only when it has no local worktree changes; otherwise stop and report the conflict. In either mode, `brief.md` or `index.md` alone is not a reviewed visual reference: require at least one visual reference that can be inspected without executing it, or the explicit prose-only approval in **Open Questions**. If the folder contains only source that cannot be visually inspected safely, ask for a screenshot/static export or that prose-only approval. Never execute HTML, scripts, or binaries supplied as design references.
7. In normal mode, update only this feature's entry in the worktree's `.context/progress-tracker.md`: move it from **Next Up** to **In Progress**, or add it there if missing. In batch-worker mode, do not edit `.context/progress-tracker.md`; the orchestrator reconciles it once for the batch. Never copy the entire tracker from the repository root.
8. Set the worktree spec's `status` to `in-progress`. Confirm the spec and either reviewed visual references beyond `brief.md`/`index.md` or the explicit prose-only approval are present before implementation. The worktree copy is the execution record and will be synchronized back to the local target checkout after the full review pipeline passes.

Determine this project's actual layer folders and stack from `.context/architecture.md`, then based on the spec's scope:
- Touches the UI layer → read the matching files under `.context/coding-conventions/` (e.g. `typescript.md`, `nextjs.md`, `react.md`, `tailwind.md`, `ui.md`) and `.context/ui-context.md`
- Touches the server/backend layer → read the matching files under `.context/coding-conventions/` (e.g. `php.md`, `symfony.md`, `javascript.md`)
- Touches infra / env vars → read `.context/infra.md`

Then explore the codebase silently:
- Find the closest existing analog feature (entity, repo, service, page, hook) and read it.
- Identify which files will be created vs. modified.

---

## Step 7 - Implement

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

## Step 8 - Verify

Quick sanity check against whichever `.context/coding-conventions/*.md` files apply to this project's stack (see Step 6) - typical checks: no syntax issues, no hardcoded strings, no swallowed errors, no debug logging left behind, naming/placement conventions respected.

---

## Step 9 - Update CHANGELOG.md

In normal mode, add one bullet under `## [Unreleased]` (create it if missing) following Keep a Changelog format (`Added` / `Changed` / `Fixed`). Describe the user-facing outcome, not the files touched. In batch-worker mode, do not edit `CHANGELOG.md`; report one proposed user-facing bullet to the orchestrator, which combines all batch entries once.

---

## Step 10 - Write verification record

Run `git add -A` (stages everything without committing - the "never commit" rule is unaffected), then `git write-tree` to get a tree hash. Run the project's `Test command:` and `Typecheck command:` from `.context/project-settings.md` (skip either if its value is `-`). Write `.context/docs/verif/<spec-id>.md` (create the `.context/docs/verif/` folder if missing) recording: the tree hash, each command run with its exit code, and a timestamp. This lets `/review-spec-implementation` trust a clean run instead of re-executing the whole suite on unchanged code.

---

## Step 11 - Memory check

If the user corrected an approach or confirmed a non-obvious one during this implementation, and it isn't already recorded, write it to `.context/memory/` now, per `.context/ai-workflow-rules.md` → "Recording Feedback (Memory)". In batch-worker mode, report it to the orchestrator instead of editing shared memory concurrently; the orchestrator records it once if needed.

---

## Step 12 - Hand off

Do NOT mark the spec as done yet - that's `/review-spec-implementation`'s job.

In normal mode, tell the user:
- What was implemented (files created/modified).
- Any deviations from the spec, and why.
- Whether there are open questions left in the spec.

Then:
> Run `/review-spec-implementation` to check every acceptance criterion, data model, and API contract. Then run `/review-security`; after it passes, the verified changes will be transferred to the local target branch for your review in VS Code or the terminal.
> If context is getting long, start a fresh session before running it.

In batch-worker mode, report the same implementation details to the parent orchestrator, include the proposed changelog bullet and any memory note, and do not tell the user to run a separate review command. The parent owns review, integration, handoff, and cleanup.

---

## Rules

- Never mark a spec done before all acceptance criteria are checked off.
- Never invent behavior not described in the spec - add open questions instead.
- The user manages Git. Never commit or push here, even after successful implementation. Only the user's direct invocation of `/commit-and-push` authorizes those actions.
- Follow all conventions from `.context/coding-conventions/`. When in doubt, re-read them.

## Verified feature handoff to the local target branch

This handoff happens only after the selected spec is `done`, every acceptance criterion is checked, and both convention and security reviews pass. `/dev` itself must stop in Step 12; do not run this handoff early. The standalone path invokes it after `/review-security`; `/implement` invokes it after its complete review loop succeeds.

The handoff puts the changes into the configured target checkout as ordinary uncommitted, unstaged local changes. It does not create a commit, push a branch, contact GitHub, or create a pull request.

1. Read `Target branch:` from `.context/project-settings.md` (default `main`). Use `git worktree list` to locate the primary checkout where that branch is checked out. Stop if the target branch is not checked out locally, or if its current commit differs from the feature worktree's branch commit. Do not switch, pull, rebase, merge, or overwrite changes to make the handoff fit.
2. Inspect both worktrees with `git status --short`. In the primary checkout, allow only the selected spec's source copy, its design-reference directory, and that spec's single progress-tracker entry as temporary framing changes. If any unrelated local change exists, stop and preserve both worktrees. For every other changed path from the feature worktree, confirm the corresponding target-checkout path has no local edits before copying it.
3. In the feature worktree, run `git add -A` to include staged, unstaged, new, and deleted files in the transfer inventory. This only stages the feature worktree; it does not commit. Record all changed paths relative to its branch HEAD.
4. Reconcile the spec artifacts safely:
   - Compare the primary checkout's spec copy with the worktree copy after normalizing only the `status:` value and acceptance-criteria checkboxes. If any other content differs, stop. Copy the final `status: done` spec from the worktree into the primary checkout.
   - Compare the complete design-reference file lists and contents in both locations. They must match exactly; otherwise stop and preserve both copies.
   - In the primary `.context/progress-tracker.md`, remove only this spec's single entry from **Next Up** or **In Progress**. Never replace the whole tracker with the feature-worktree copy. If the entry is missing, duplicated, or ambiguous, stop.
5. Copy each remaining changed or new file from the feature worktree to the same relative path in the primary checkout, and apply deletions there. This includes application changes, `CHANGELOG.md`, and the verification record. Preserve file bytes. Do not overwrite a target file with local edits. If any path cannot be reconciled exactly, stop and leave the feature worktree and branch intact.
6. Verify that the primary checkout now contains every application, documentation, and verification change from the feature worktree; that the final spec copy is identical; that the design handoff matches; and that only the selected spec entry was reconciled in the progress tracker. No unrelated root edits may be included. The primary target checkout must show the complete feature diff for local review.
7. Only after that verification, remove `.worktrees/<spec-id>/` and delete the local `feature/<spec-id>` branch. The branch must still point to the same commit as the target branch; if it does not, stop. A forced worktree removal is allowed only after every changed file has been verified in the primary checkout.
8. Tell the user the spec is verified and its changes are now on the local target branch, uncommitted and unpushed. Ask them to review with VS Code or `git diff HEAD`; when satisfied, they may directly invoke `/commit-and-push`.

There is no remote feature branch, pull request, GitHub CLI prerequisite, post-merge cleanup, or automatic commit/push in this workflow.
