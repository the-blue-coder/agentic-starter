---
description: "Autonomously implement multiple specs in parallel in isolated worktrees, integrate them, and hand off uncommitted changes with a decision report"
argument-hint: "<spec ID or dropped spec file> <spec ID or dropped spec file> [more] | resume <batch-id>"
---

Implement two or more existing feature specs concurrently and autonomously. The primary agent is the batch orchestrator; it launches one worker per spec, integrates their uncommitted diffs, and hands the complete reviewed result to the configured local target branch.

**This command is autonomous.** Follow `.context/commands/autonomous-mode.md` for the whole run: never ask the user anything after it starts, decide ambiguities yourself, record every decision, set failed specs aside, and finish with its final report. For specs that must be built one after another because they depend on each other, use `/implement-queue` instead.

This workflow creates no commits, pushes, remote branches, or pull requests. Because the per-spec branches intentionally contain no commits, integration is patch-based in a temporary integration worktree, not `git merge --no-commit`. The final target checkout receives uncommitted, unstaged changes for the user's local review. Only a later direct `/commit-and-push` invocation authorizes a commit or push.

Arguments:

- `/implement-swarm <spec-id-or-file> <spec-id-or-file> [...]` starts a batch. Require at least two distinct exact spec IDs or validated local spec file paths/`file:` URIs. Follow `.context/commands/spec-selector-resolution.md`; do not accept fuzzy name fragments in a batch. If no selectors are supplied, select every eligible `todo` spec in ID order (at least two required) and list them in the final report.
- `/implement-swarm resume <batch-id>` resumes the recorded batch. Require exactly one safe batch ID after `resume`; it must not start a new batch in the same invocation.

Read `.context/commands/autonomous-mode.md`, `.context/ai-workflow-entrypoint.md`, `.context/project-settings.md`, `.context/project-overview.md`, `.context/architecture.md`, `.context/coding-conventions/global.md`, `.context/coding-conventions/security.md`, `.context/commands/spec-selector-resolution.md`, and the selected specs before proceeding.

## Phase 1 - Preflight

For a new batch:

1. Confirm shared framing is complete using the same gate as `/spec`. Resolve `Target branch:` (default `main`) and locate its primary checkout. Run this command from that checkout. Do not switch branches or alter the remote.
2. Resolve every argument into a spec ID using `.context/commands/spec-selector-resolution.md`; file URLs and absolute paths must resolve to direct spec files in this primary checkout. Require at least two distinct resulting IDs. Before using an ID in a path, require it to match `^[A-Za-z0-9][A-Za-z0-9._-]*$` and reject `.` or `..`; this keeps it a single safe path component. Each validated ID must exist as `.context/feature-specs/<spec-id>.md`, have `status: todo`, and have every required UI design reference or explicit prose-only approval. This initial version does not batch specs already in progress or completed specs.
3. Before creating the manifest or any worktree, confirm this agent runtime can launch and monitor at least two implementation subagents concurrently. If it cannot, stop without changing files or Git state; do not silently run the requested parallel batch sequentially.
4. Refuse to start if any other spec is `in-progress`, any feature worktree or `feature/<spec-id>` branch is already active, or an incomplete batch manifest exists. Do not guess whether existing work belongs to this batch.
5. Require the primary checkout to be on `Target branch:` and at its current `HEAD` throughout the run. The target checkout may contain only the selected specs' planning files/design directories and their entries in `.context/progress-tracker.md`; no staged changes or unrelated edits are allowed. Record the SHA-256 and kind of every allowed pre-existing changed path in `preflight_paths`. Do not stash, reset, switch, pull, or overwrite anything.
6. Confirm each selected spec path, design-reference path, worktree path, and local feature branch is unique and unused. Record the target branch's exact starting commit as `<base-sha>`.
7. Choose a unique UTC `<batch-id>` such as `batch-yyyy_mm_dd_hh_ii_ss`. Create `.worktrees/.parallel-batches/<batch-id>/manifest.json` before creating any worktree. The manifest is local ignored state, not a project artifact. Use this shape and preserve it across updates:

   ```json
   {
     "batch_id": "batch-yyyy_mm_dd_hh_ii_ss",
     "phase": "preparing",
     "target_branch": "main",
     "base_sha": "<full commit SHA>",
     "specs": [
      {
        "id": "<spec-id>",
        "worktree": ".worktrees/<spec-id>",
        "branch": "feature/<spec-id>",
        "worker": "pending",
        "worker_attempt": 0,
        "review": "pending",
        "review_round": 0,
        "worktree_cleanup": "pending",
        "branch_cleanup": "pending"
      }
    ],
    "integration_worktree": ".worktrees/.parallel-batches/<batch-id>/integration",
    "integration_cleanup": "pending",
    "transfer_verified": false,
    "preflight_paths": [],
    "paths": [],
    "artifacts": []
  }
  ```

  Each spec also has `"excluded": false`, set to `true` with a `"excluded_reason"` when the spec is set aside (see autonomous mode); excluded specs are skipped by every later phase and by cleanup. `phase` is one of `preparing`, `preparation-blocked`, `implementing`, `workers-blocked`, `reviewing`, `review-blocked`, `integrating`, `integration-blocked`, `transferring`, or `cleanup-pending`. Worker and review states are `pending`, `running`, `passed`, or `failed`; worktree/branch cleanup states are `pending`, `complete`, or `failed`. Each `preflight_paths` entry records an allowed pre-existing target change as a normalized repository-relative path, its kind (`spec`, `design`, or `progress-tracker`), and its SHA-256. Each `paths` entry records a normalized repository-relative path, its pre-transfer SHA-256 or `absent`, its expected final SHA-256 or `absent` for deletion, a registered temporary sibling path (or `null` for deletion), and a transfer state (`pending`, `applying`, or `complete`). Each `artifacts` entry records a final path under this batch directory, its registered `.tmp` sibling path, its SHA-256, and a cleanup state (`pending`, `removing`, or `complete`). Populate every path snapshot before copying the first file. Write updates to a temporary sibling file and rename it over the manifest so an interruption cannot leave a half-written manifest. Never store secrets in it.
8. Before and after every worktree or branch mutation, update the manifest. If interrupted between the Git operation and its following manifest update, reconcile the manifest against read-only `git worktree list`, `git branch --list`, and filesystem checks before doing anything else.

If an incomplete manifest or manifest temporary file already exists, do not start a new batch. Require `resume <batch-id>` for that exact batch. If the manifest is missing, unreadable, or disagrees with Git state, stop and report the paths/branches; never delete an unknown worktree or branch automatically.

## Phase 2 - Prepare isolated spec worktrees

For every selected spec, create exactly one worktree `.worktrees/<spec-id>/` on local branch `feature/<spec-id>`, based on `<base-sha>`. Before creating anything, validate each ID is a single safe filename component and `git check-ref-format --branch feature/<spec-id>` succeeds. Record the expected path and branch in the manifest before creation and confirm the created worktree is on the expected branch and base afterward. Synchronize only that spec and its reviewed design handoff from the primary checkout into its worktree. For every source file, verify that its hash matches its saved preflight hash when listed in `preflight_paths`, or the `<base-sha>` file hash otherwise. Copy it when the worktree copy is missing or is an unchanged base-commit version; stop if the worktree has a local change at that path. Never overwrite worker changes during resume.

Do not create remote feature branches. Do not create a commit in a feature worktree. Do not edit the primary target checkout during implementation. If setup is complete, set `phase: implementing`. If any setup fails, preserve every existing worktree and the manifest, set `phase: preparation-blocked`, and report how to resume it.

## Phase 3 - Implement each spec concurrently

Launch one specialized `implementer` subagent per selected spec concurrently, to the extent the active agent runtime allows; use multiple waves only when the selected batch exceeds its concurrent-agent limit. Pass each worker the exact batch ID, spec ID, spec path, worktree path, branch name, and base SHA. If an agent cannot be launched after worktree preparation, set the batch to `workers-blocked`, preserve all worktrees, and report how to resume.

Each worker starts with fresh context, so instruct it to read `.context/commands/dev.md` and its Step 1 files (`.context/ai-workflow-entrypoint.md`, `.context/project-overview.md`, `.context/architecture.md`, `.context/coding-conventions/global.md`, and `.context/coding-conventions/security.md`), then execute Steps 6 through 10 for only its assigned spec. On a resumed worker, inspect the existing assigned worktree and continue from its current state; never recreate, reset, clean, or resynchronize it. Stop if that state cannot be safely continued. It must:

- Restrict every read/write and Git command to its assigned spec worktree, except for reading shared project context.
- Keep its worktree and local branch after implementation. Do not run reviews, hand off to the target checkout, or clean up.
- Never commit, push, create a remote branch, or edit the primary target checkout.
- Follow batch mode in `.context/commands/dev.md`: leave `.context/progress-tracker.md` and `CHANGELOG.md` untouched, and report one proposed changelog bullet to the orchestrator.
- Do not write `.context/memory/` in a worker worktree; report any memory note to the orchestrator so it can record it once.
- Follow the TDD loop of `.context/coding-conventions/tdd.md` and keep the TDD journal in the verification record.
- Complete the normal verification record and test/typecheck commands in its worktree. `git add -A` is allowed to inventory staged, unstaged, new, and deleted files; committing is not.
- Report implementation details, deviations, open questions, exact changed paths, the verification record and command results, its proposed changelog bullet, and any memory note that the orchestrator should record.

Increment `worker_attempt` and mark that worker `running` before each launch; record it as `passed` or `failed` after its report arrives. Compute the report SHA-256, register its final path, `.tmp` sibling path, and hash in `artifacts` with an atomic manifest update, then write it to the registered `.tmp` file and rename it into `.worktrees/.parallel-batches/<batch-id>/reports/<spec-id>/implementation-attempt-<n>.md`. Wait until every worker has stopped and reported. Workers decide open questions themselves and report each decision (spec ID, question, choice, reason, rejected alternative). If a worker fails, retry it once; if it fails again, mark the spec `excluded` and continue. If a worker leaves its result uncertain (for example it may still be running), set the batch to `workers-blocked`, preserve all worktrees, and stop. If every spec is excluded, stop without integrating. Resume only after confirming no prior worker is still running.

## Phase 4 - Verify and review every spec

Once all workers pass, set `phase: reviewing`. Run a batch-level review loop with a maximum of five rounds. Review pipelines for different specs may run concurrently; within one spec, run the read-only verifier, convention reviewer, performance reviewer, and security reviewer sequentially because the last three may edit that spec's worktree. For each implemented spec, run:

- A `spec-verifier` subagent following `.context/commands/review-spec-implementation.md` Steps 3 through 8 for that exact worktree. It returns the structured criterion verdicts and evidence; it must not set `status: done` or hand off.
- A `convention-reviewer` subagent following `.context/commands/review-changes.md` Steps 2 through 7 for that exact worktree and spec scope. It must not inspect other batch worktrees or run Step 8's user reminder/handoff.
- A `performance-reviewer` subagent following `.context/commands/review-performance.md` Steps 2 through 6 for that exact worktree. It must not do the manual reminder.
- A `security-reviewer` subagent following `.context/commands/review-security.md` Steps 2 through 6 for that exact worktree. It must not do the manual reminder or target handoff.

Pass the batch ID, role `worker`, spec ID, worktree path, branch, and base SHA to each reviewer so it bypasses ambiguous worktree discovery safely. Update each spec's `review` to `running` and `review_round` before starting. For each report, compute its SHA-256 and atomically register its final path, `.tmp` sibling path, and hash in `artifacts` before writing it to that temp file and renaming it into place: use `spec-verification.md`, `conventions.md`, `performance.md`, and `security.md` under `.worktrees/.parallel-batches/<batch-id>/reports/<spec-id>/round-<n>/`. Save any targeted fixer report as `fixes.md` in that round directory. This lets resume inspect the last completed round. Collect all reports before starting another round. If any finding needs a code change, send only that spec's precise fixes to an `implementer` in its assigned worktree, then rerun all four reviews for that spec. Do not mark a spec done until all criteria and reviews pass. After a spec passes, mark its worktree copy `done`, run `git add -A` there to capture that final status and any new/deleted files, and update its `review` state to `passed`. Shared tracker and changelog remain untouched.

If a spec has not passed after five review rounds, set its `review` state to `failed` and mark it `excluded`; it keeps its worktree, branch, and `status: in-progress`. Continue with the specs that passed and integrate only those. If no spec passed, set the batch to `review-blocked`, preserve every worktree, and stop.

Before integration, independently confirm for every passing, non-excluded spec that its worktree copy is `done`, every acceptance criterion is checked, its verification record exists, all four reviews passed, its worktree is on the expected branch, and the branch still points to `<base-sha>`. If a branch HEAD moved, stop and preserve it; workers are not authorized to commit.

## Phase 5 - Integrate and review in a temporary checkout

1. Set `phase: integrating`. Create a detached integration worktree at `<base-sha>` under `.worktrees/.parallel-batches/<batch-id>/integration/`. Record it in the manifest. This keeps integration failures away from the user's target checkout. Install dependencies there only if needed, following `.context/architecture.md` and the existing dev workflow. If `.context/progress-tracker.md` is in `preflight_paths`, verify the target file still matches its recorded SHA-256, then copy that version into this worktree before patch application so selected entries and allowed existing tracker content are preserved. Stop if it differs.
2. In deterministic spec-ID order, capture each worker's complete staged diff against `<base-sha>` as a binary Git patch. Preserve its bytes without text encoding or newline conversion. Compute its SHA-256, atomically register its final path, `.tmp` sibling path, and hash in `artifacts`, and write it to the registered temp file before renaming it under `.worktrees/.parallel-batches/<batch-id>/patches/<spec-id>.patch`. Then apply it to the integration worktree with Git's three-way patch application. This combines uncommitted edits without creating commits. Do not use `git merge` or `git cherry-pick`, and do not create commits.
3. Resolve overlapping application-file changes only when both specs' behavior and acceptance criteria can be preserved. If a conflict cannot be resolved confidently, record the conflicting paths, mark the later spec (in ID order) `excluded` with the conflicting paths as its reason, and rebuild the integration from the remaining specs in a fresh integration worktree; remove the abandoned one only after recording that in the manifest. Never discard part of a worker's change to make a patch apply, and never reset a scratch worktree blindly. If the state is ambiguous, set `integration-blocked`, preserve every worktree, and stop.
4. Reconcile shared metadata once: preserve the target's current tracker content and remove only the selected specs' entries from `Next Up`/`In Progress`; combine each worker's proposed changelog bullet under the existing `Unreleased` section. Record any valid worker memory note only if it captures user feedback not already documented, following `.context/ai-workflow-rules.md`. Do not copy one worker's entire tracker or changelog over another.
5. Run the configured `Test command:` and `Typecheck command:` from `.context/project-settings.md` once against the integrated result when not `-`. Then run the convention, performance, and security reviews on the complete integrated diff, passing batch context with role `integration`, the selected spec IDs, and the integration worktree path; do not emit standalone user reminders or handoffs from these reviewers. If integration resolved any code conflict or changed a spec's implementation, rerun spec verification for every affected spec in that integration worktree. Keep the standard five-iteration cap. If a final check still fails, set `integration-blocked`, preserve all worktrees, and stop without changing the primary target checkout.
6. After the integrated result passes, run `git add -A` in the integration worktree (no commit), derive the final path inventory from its staged diff against `<base-sha>`, and record the expected final content hash for every created, changed, or deleted path. Then set `phase: transferring`.

## Phase 6 - Transfer the complete batch to the local target checkout

The target checkout must still be on `Target branch:` at `<base-sha>`. Recheck its status and compare each destination against the preflight snapshots recorded in `preflight_paths`. Selected spec files, reviewed design files, and progress-tracker changes are the only allowed pre-existing planning changes. For every other path, the destination must still match `<base-sha>` or be absent if the integration creates it. If a user edit, unexpected staged change, or file mismatch appeared, stop and preserve the source worktrees.

Before copying anything, populate the manifest's complete `paths` list with the expected pre-transfer and final hashes and a unique temporary sibling path for every regular-file replacement/creation; use `null` for deletions. For an allowed pre-existing path, the pre-transfer hash must equal its saved preflight hash; otherwise it must equal the base-commit file hash or `absent`. Require normalized repository-relative paths, reject absolute paths and `..`, and confirm the resolved destination stays inside the target checkout. Do not follow symlinked parent directories; if a source or destination path is a symlink or another non-regular file, stop and preserve the worktrees. For each regular file, copy to its registered temporary sibling, verify its final hash, then atomically rename it into place; preserve bytes and executable mode. For each path, atomically set `state: applying` immediately before copying or deleting it, then set `state: complete` after verifying the destination hash. On resume, a destination matching the final hash is transferred; if its registered temp file also exists, remove it only after verifying the same final hash. For a deletion (`final_sha256: absent`), accept the absent destination only when its state is `applying` or `complete`. If the destination still matches its pre-transfer snapshot and a registered temporary sibling exists, require that sibling's hash to match the final hash before renaming it into place; if no temporary sibling exists, copy again. Stop on any third value or unexpected temporary-file hash. For spec files, require that only the `status:` value and acceptance-criteria checkboxes changed from the preflight copy. Design-reference file lists and contents must remain identical to the approved preflight handoff.

After all paths are copied and every registered temporary sibling is absent, verify that the target checkout contains the complete integrated result, all selected specs are `done`, only the selected progress entries were reconciled, all design references are preserved, and no unrelated changes were included. Confirm that the final target-branch diff is uncommitted and unstaged. Record `transfer_verified: true` and `phase: cleanup-pending` in the manifest. At this point the user can review the complete batch locally even if cleanup later fails.

## Phase 7 - Idempotent cleanup and handoff

Clean up only after the complete target transfer has been verified and recorded. Excluded specs are never cleaned up: keep their worktree and `feature/<spec-id>` branch so `/dev <spec-id>` can resume them, and ignore them in every check below.

1. Before any cleanup, verify every target path still matches its recorded final hash. If the user has committed and pushed the target branch, its `HEAD` may have advanced, but the checked-out file contents must still match. If any path differs, stop and preserve all worktrees and branches. Then, for each spec worktree, confirm its changes are present in the verified integration result and target checkout, and that its feature branch still points to `<base-sha>`. Remove that worktree only after these checks. A forced worktree removal is allowed only after this verification because the staged worker diff is already preserved in the integration result and target checkout.
2. After its worktree is gone, delete that local feature branch only if it still points to `<base-sha>` and is not checked out elsewhere. Never force-delete a branch whose commit differs from the recorded base.
3. Remove the integration worktree only after confirming its final diff is fully represented in the target checkout.
4. Record each successful worktree and branch removal immediately. If any removal fails or the process is interrupted, leave the manifest with `phase: cleanup-pending`; do not report cleanup complete. A resume must skip already-removed paths/branches and retry only verified remaining cleanup.
5. After all recorded worktrees and branches are confirmed absent and target hashes remain verified, remove only the registered artifacts whose current SHA-256 still matches the manifest. Before deleting an artifact, set its cleanup state to `removing`; verify and remove its final file and registered `.tmp` sibling, then set the state to `complete`. On resume, accept both files as absent only if cleanup is `removing` or `complete`. Preserve any artifact with a different hash and any unregistered file; stop and report it. Delete the manifest last and remove the now-empty batch state directory. If a worktree exists without a readable manifest, do not remove it automatically; report it for inspection.

When cleanup succeeds, deliver the final report defined in `.context/commands/autonomous-mode.md`. State that the combined changes are on the configured target branch, uncommitted and unstaged, and that only the user's later direct `/commit-and-push` invocation can commit and push.

## Resume behavior

For `resume <batch-id>` (an autonomous resume likewise never asks questions), first require exactly one ID, validate it as a single safe filename component, and confirm it exactly matches the manifest's `batch_id`. Read the manifest and reconcile it with actual Git worktrees, branches, paths, artifacts, and hashes before any mutation. Validate every manifest path before using it: spec worktrees and branches must exactly derive from the validated spec IDs, the integration worktree and artifacts must remain under this batch's `.worktrees/.parallel-batches/<batch-id>/` directory, and every transfer path must be normalized, unique, and contained inside the repository. Resolve the primary checkout from `git worktree list`; the manifest is under that checkout even when the command is invoked from a feature worktree. If `manifest.json.tmp` exists, validate it and the last committed manifest against actual Git state; if they cannot be reconciled unambiguously, stop and preserve both files.

For each registered artifact before cleanup, accept a final file only when its hash matches the manifest. If only its registered `.tmp` sibling exists and matches the expected hash, rename it to the final path. If both exist, require both hashes to match and remove the redundant temp file. Stop and preserve the batch if either file has unexpected content.

- `cleanup-pending`: resume cleanup only; never relaunch workers. The target branch may have advanced after the verified transfer because the user may already have committed it; verify target file hashes, not the original target `HEAD`.
- `transferring`: if every path has pre-transfer and final hashes recorded, resume the recorded copy only; never relaunch workers. If the path inventory is incomplete, stop and preserve all data.
- `preparing` or `preparation-blocked`: reconcile worktrees and branches, then continue only the missing setup for this batch.
- `workers-blocked` or interrupted implementation: preserve all state and relaunch only workers recorded failed or not started, after confirming that any previously running worker has stopped. Do not restart workers already recorded passed.
- `reviewing`, `review-blocked`, or interrupted review: preserve all state, confirm no prior reviewer or fixer is still running, inspect saved reports, and continue only the affected spec's review/fix loop. Do not reset or recreate a worktree.
- `integrating` or `integration-blocked`: inspect the recorded integration worktree and conflicts. Continue only when you can determine exactly which worker patches and metadata updates are already present; if a patch may have been partially applied or its state is ambiguous, set `integration-blocked`, preserve every worktree, and report the paths. Never reapply blindly or reset the scratch worktree.
- A missing or invalid manifest, an unexpected feature-branch SHA, an unknown worktree, or a destination hash that matches neither its recorded pre-transfer nor final hash is a hard stop. Preserve all data and report exact paths.

`/status` remains read-only and reports incomplete manifests, their phase, worker counts, and any expected worktree/branch that still exists. New `/spec`, `/dev`, `/implement`, and parallel batches must stop while an incomplete batch needs recovery. `/commit-and-push` must stop before staging if transfer is partial; it may run during `cleanup-pending` only after verifying the full target transfer, since the user can review and authorize the target-branch commit independently of cleanup.

There is no PR, remote feature branch, automatic commit/push, automatic stash/reset, or deletion of an untracked/unknown worktree in this workflow.
