---
description: "Commit reviewed local target-branch changes and push them to origin"
argument-hint: "<optional spec ID>"
---

You are committing and pushing the developer's reviewed local changes.

**Invocation gate:** execute this workflow only when the user directly invoked `$commit-and-push` in Codex or `/commit-and-push` in another command environment. No other workflow, review result, completed spec, or handoff authorizes a commit or push.

This workflow never creates or updates a pull request and never pushes a feature branch. Feature changes must already have been transferred from their reviewed spec worktree into the configured local target branch, where the user can inspect them before invoking this command.

## Step 1 - Resolve the target checkout

Read `Target branch:` from `.context/project-settings.md` (default to `main` if the file is missing). The current checkout must be on that branch. If the current branch is `feature/<spec-id>`, stop and tell the user that the verified changes must first be handed off to the local target branch for review. Never switch branches or merge a feature branch here.

Confirm that `origin` exists before committing. If there is no `origin`, stop and report that the project remote must be configured before this command can push.

Inspect `.worktrees/.parallel-batches/` for an incomplete `manifest.json` before staging. If any batch manifest exists outside the `cleanup-pending` phase, or its target transfer is not verified, stop without staging; require `$parallel-implement resume <batch-id>` / `/parallel-implement resume <batch-id>`. In `cleanup-pending`, allow the user-authorized commit only after independently confirming every final path/hash in the manifest is present in the target checkout and all pending target changes are represented by the manifest's `paths` or `preflight_paths`. Cleanup may then be resumed separately. A corrupt manifest is a hard stop; never guess that a partial batch is safe to commit.

## Step 2 - Memory check

Before touching Git, record any user correction, confirmed non-obvious approach, or project fact from this session that is not already in `.context/memory/`, following `.context/ai-workflow-rules.md` and the memory protocol.

## Step 3 - Understand what changed

Run these in parallel:

```bash
git status --short
git diff HEAD
git log --format="%s" -10
```

Read the output carefully. Identify whether this is a completed spec handoff, an ad-hoc change, or a mixture. If the changes contain work from more than one unfinished spec, stop and ask the user to resolve the overlap before committing. If `$ARGS` names a spec, verify that spec is the one represented by the local changes.

Find every changed `.context/feature-specs/<spec-id>.md` in the target diff. Confirm each changed implementation spec is `status: done` and every acceptance criterion is checked; stop before staging if any check fails. For a parallel batch whose manifest remains in `cleanup-pending`, also confirm the selected IDs match the manifest, transfer is verified, and the target diff still matches the manifest's final hashes. Compare all staged, unstaged, untracked, and deleted target paths against the manifest allowlist; stop before staging if an unrelated path is present. When cleanup already removed the manifest, validate every changed spec independently and treat multiple completed specs as the reviewed batch handoff.

## Step 4 - Stage changes

```bash
git add -A
```

If nothing is staged after this step, report that there is nothing to commit and stop.

## Step 5 - Write the commit message

Read the last 10 commit subjects (`git log --format="%s" -10`). If any contain `Co-Authored-By` or AI attribution, look further back until you find commits without it. Mimic the style of those human commits (casing, tone, prefix conventions).

Write one commit-message line following these rules:

- **Imperative mood** - "add login page", "fix redirect loop", "update auth config". Not "added", "fixed", or "updated".
- **Lowercase** - no capital first letter.
- **Specific** - name what actually changed.
- **No period** at the end.
- **Under 72 characters**.
- **Single-spec implementation**: if one spec is represented in the diff, include its full spec ID and title, for example `implement 2026_09_27_15_42_31-batch-ingredient-add`.
- **Parallel batch**: if multiple completed specs are represented, use the manifest's batch ID when it remains available, for example `implement batch-2026_09_27_15_42_31-catalog-and-search`; after cleanup removed the manifest, use `implement parallel batch of <n> specs`.

## Step 6 - Commit and push the target branch

The commit message is the plain `-m` string only. No trailers, `Co-Authored-By`, `Generated with`, or AI attribution.

Confirm again that `git branch --show-current` equals `Target branch:`. Then, and only because the user directly invoked this command, commit the staged changes and push the current target branch:

```bash
git commit -m "<commit message>"
git push origin HEAD
```

Run commands sequentially, each depending on the previous succeeding. Never use `--force`. If the commit succeeds but the push fails, leave the commit intact and report its hash and the push error; do not reset or create another commit to hide the failure.

## Step 7 - Confirm

Report one concise line:

- Successful push: `pushed <hash> - <message>`.
- No changes: `nothing to commit; no push was made`.
- Push failed after commit: `committed <hash> - <message>; push failed: <reason>`.

There is no PR creation, PR confirmation, remote feature-branch push, post-merge invocation, or worktree cleanup in this command. The worktree and feature branch are removed by the verified local-main handoff before the user reviews the target-branch changes.
