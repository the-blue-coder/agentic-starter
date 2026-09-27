---
description: "Stage all changes, write a human commit message, commit, and push to origin"
---

You are committing and pushing the current changes on behalf of the developer.

**Invocation gate:** execute this workflow only when the user directly invoked `$commit-and-push` in Codex or `/commit-and-push` in another command environment. Do not run it because another workflow, status report, or agent suggested it. If this command was invoked by another command or agent rather than the user, stop without staging, committing, or pushing.

## Step 0 - Resolve where the work actually is

Each spec's work happens in its own worktree (`.worktrees/<NNN-slug>/`, branch `feature/<NNN-slug>` - see `.context/commands/dev.md`), not in the main checkout. Check the current branch (`git branch --show-current`):

- Already `feature/<NNN-slug>` - the session's own working directory is already the right place (either it's the worktree itself, or, in a tool that doesn't isolate subagent working directories, this repo's root happens to be on that branch). Proceed from here.
- `main` / the default branch - this is almost always an ad-hoc commit unrelated to any spec (docs, config, a quick fix). Proceed as-is UNLESS exactly one spec has `status: in-progress` with an existing `.worktrees/<NNN-slug>/` holding uncommitted changes (check `git -C .worktrees/<NNN-slug>/ status --short` for each in-progress spec's worktree) - if there's exactly one such match, resolve every command below to run there (`git -C .worktrees/<NNN-slug>/ <command>` or `cd` into it first). If more than one matches, ask the user which spec they mean rather than guessing.

## Step 1 - Memory check

Before touching git: did this session include a correction from the user ("no, don't do X"), a confirmation of a non-obvious approach ("yes exactly, keep doing that"), or a project fact not derivable from the diff (a deadline, a stakeholder ask)? If so and it isn't already recorded, write it to `.context/memory/` now, per `.context/ai-workflow-rules.md` → "Recording Feedback (Memory)" - this is the last checkpoint before the session's context is gone.

## Step 2 - Understand what changed

Run these in parallel:

```bash
git status --short
git diff HEAD
git log --format="%s" -10
```

Read the output carefully. Identify the nature of the changes: new feature, bug fix, refactor, config change, docs update, etc.

## Step 3 - Stage everything

```bash
git add -A
```

## Step 4 - Write the commit message

First, read the last 10 commit subjects (`git log --format="%s" -10`). If any of them contain "Co-Authored-By" or AI attribution, look further back until you find commits without it. Mimic the style of those human commits (casing, tone, prefix conventions).

Then write a single commit message line following these rules:

- **Imperative mood** - "add login page", "fix redirect loop", "update auth config". Not "added", "fixed", "updated".
- **Lowercase** - no capital first letter.
- **Specific** - name what actually changed, not just "update files".
- **No period** at the end.
- **Under 72 characters**.
- If multiple unrelated things changed, pick the most significant one and mention others briefly: `"add auth flow, wire i18n routing"`.
- **Spec implementation**: if the diff marks a spec `status: done`, the message must include the spec number and title - e.g. `"implement 005 - batch ingredient add"` or `"add batch ingredient add (spec 005)"`.

## Step 5 - Commit and ship to the right destination

**CRITICAL**: the commit message is the plain `-m` string only. No trailers. No `Co-Authored-By`. No `Generated with`. No AI attribution of any kind. A human developer wrote this commit.

Determine the current branch (`git branch --show-current`):

- **Default branch** (`main` or the configured target branch, not `feature/*`) - commit staged changes if any, then run `git push origin HEAD`. This remains the path for ad-hoc work that is not tied to a spec.
- **Feature branch** (`feature/<NNN-slug>`) - follow the PR-only steps below. Never squash-merge locally or push a spec branch directly into the target branch.

### Feature branch: one spec, one PR

1. Confirm the matching `.context/feature-specs/<NNN-slug>.md` exists, its frontmatter says `status: done`, and every acceptance criterion is checked. If any check fails, stop without committing or pushing.
2. Read `Target branch:` and `Ship confirmation:` from `.context/project-settings.md` (default to `main` and `human` if the file is missing).
3. Before committing, query all PR states for this head:
   ```bash
   gh pr list --head "feature/<NNN-slug>" --state all --json number,state,url,baseRefName
   ```
   If `gh` is unavailable or errors, stop before commit/push because the one-PR guarantee cannot be checked.
   - More than one PR: stop and report the duplicate; never create another.
   - One PR with a base other than `Target branch:`: stop and report the mismatch; do not create another PR.
   - One `MERGED` PR: do not commit or push new changes after merge. If the worktree is clean, go to Step 7; otherwise stop and report the uncommitted changes for a new spec.
   - One `OPEN` PR: continue to commit and push updates to that same PR.
   - One `CLOSED` PR: continue to push updates, then reopen that same PR. Never create a replacement PR for the spec.
   - No PR: continue to commit and push, then create the one PR for this spec.
4. If there are staged changes, commit using the message from Step 4. Do not create an empty commit.
5. Push the feature branch:
   ```bash
   git push -u origin HEAD
   ```
6. If a PR is already `OPEN`, report that it was updated and stop without cleanup. If a PR is `CLOSED`, ask for confirmation when `Ship confirmation: human`, then run `gh pr reopen <number>`; if the user declines, leave it closed and report the pushed branch. If there was no PR, ask for confirmation when `Ship confirmation: human`, then open one against `Target branch:`:
   ```bash
   gh pr create --base <target-branch> --title "<spec title>" --body "<spec goal + link to .context/feature-specs/<id>.md>"
   ```
   `automatic` skips only the PR confirmation. A newly opened or reopened PR is not yet merged; do not run Step 7 this time. The user re-runs `/commit-and-push` after it is merged.

Run commands sequentially, each depending on the previous succeeding.

## Step 6 - Confirm

Report the outcome to the user. One line, matching what happened:
- Plain push: `pushed <hash> - <message>`.
- PR opened: `pushed <hash> - <message>; PR opened: <PR URL>`.
- Existing PR updated: `pushed <hash> - <message>; updated PR <PR URL>`.
- Closed PR reopened: `pushed <hash> - <message>; reopened PR <PR URL>`.
- PR already merged: `PR <URL> is merged - no new commit or push was made`.
- Cleanup done: append `; worktree and branch removed` to whichever of the above applies.

## Step 7 - Clean up the worktree (only after a proven merge)

Only reached when the PR's state came back `MERGED` - never on an unproven assumption:

Before removing the feature worktree, clean the temporary source copies that `/spec` and `/dev` left in the primary checkout, so the user can fast-forward that checkout after the PR merge:

1. Find the primary checkout from `git worktree list` and inspect `.context/feature-specs/<NNN-slug>.md` there. If it is an untracked copy, compare it with the merged worktree spec after normalizing only the `status:` value and acceptance-criteria checkboxes. Delete the root copy only if everything else matches exactly. If the spec path is tracked, or any other content differs, stop cleanup and report the conflict; never delete a tracked file or user edits.
2. If the root `.context/feature-specs/design/<NNN-slug>/` exists, compare its complete file list and contents with the merged worktree's design directory. Remove only exact duplicate files. If any file differs or exists only in the root, stop cleanup and report it. Remove the now-empty per-spec design directory only after all its files were confirmed as duplicates.
3. In the primary checkout's `.context/progress-tracker.md`, remove only the selected spec's single entry from **Next Up** or **In Progress**. If it appears more than once or the tracker is otherwise ambiguous, stop cleanup and report the conflict. Do not modify other tracker content.

If any source copy cannot be safely reconciled, leave the worktree and branch in place and tell the user what needs review. After cleanup succeeds, tell the user to fast-forward the primary checkout with `git pull --ff-only origin <target-branch>` before starting the next spec.

```bash
git worktree remove .worktrees/<NNN-slug>
git branch -D feature/<NNN-slug>
git push origin --delete feature/<NNN-slug>
```

`git branch -D` is safe here only because the PR was verified as merged and the worktree has already been removed; squash-merged commits are not necessarily ancestors of the target branch.

If `git worktree remove` refuses because of leftover untracked files (e.g. `node_modules`, `.env*` copied in at setup), that's expected - use `git worktree remove --force` for those, never for a worktree still holding unmerged or uncommitted work.
