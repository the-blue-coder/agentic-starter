---
description: "Stage all changes, write a human commit message, commit, and push to origin"
---

You are committing and pushing the current changes on behalf of the developer.

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

## Step 5 - Commit and push

**CRITICAL**: the commit message is the plain `-m` string only. No trailers. No `Co-Authored-By`. No `Generated with`. No AI attribution of any kind. A human developer wrote this commit.

```bash
git commit -m "<your message>"
```

Then branch on the current branch:

**If the current branch is `main` / the default branch (not a `feature/*` branch)** - keep the existing behavior unchanged, this covers ad-hoc doc/config commits not tied to a spec:

```bash
git push origin HEAD
```

**If the current branch is `feature/<NNN-slug>`** (tied to a spec under `.context/feature-specs/`) - read `Merge mode:` and `Ship confirmation:` from `.context/project-settings.md` (default `Merge mode: pr`, `Ship confirmation: human` if the file is missing):

- **`Merge mode: pr`**:
  ```bash
  git push -u origin HEAD
  ```
  If a PR already exists for this branch (`gh pr view feature/<NNN-slug> --json state`), check its state instead of opening a new one:
  - `MERGED` - the ship already happened on a previous run. Go straight to Step 7 (cleanup) and skip the rest of this step.
  - `OPEN` / anything else - nothing more to do here; tell the user it's still open and awaiting merge, then stop (do not clean up an unmerged worktree).

  Otherwise, open the PR against `Target branch:`:
  ```bash
  gh pr create --title "<spec title>" --body "<spec goal + link to .context/feature-specs/<id>.md>"
  ```
  If `Ship confirmation: human`, ask the user to confirm before running `gh pr create` - pushing the branch itself needs no confirmation, opening the PR does, that's the "ship" action. `automatic` skips the confirmation. A freshly opened PR is not yet merged - do not run Step 7 this time; the user re-runs `/commit-and-push` once it's merged to confirm and clean up.

- **`Merge mode: local`**:
  ```bash
  git checkout <target-branch>
  git merge --squash feature/<NNN-slug>
  git commit -m "<message>"
  git push origin <target-branch>
  ```
  Same `Ship confirmation` gate before the merge step. The squash-merge above IS the proven merge - continue straight to Step 7.

Run commands sequentially, each depending on the previous succeeding.

## Step 6 - Confirm

Report the outcome to the user. One line, matching what happened:
- Plain push: `pushed <hash> - <message>`.
- PR opened: `pushed <hash> - <message>; PR opened: <PR URL>`.
- PR still open (re-run): `PR <URL> is still open - nothing to clean up yet.`
- Local squash-merge: `pushed <hash> - <message>; squash-merged into <target-branch>`.
- Cleanup done: append `; worktree and branch removed` to whichever of the above applies.

## Step 7 - Clean up the worktree (only after a proven merge)

Only reached when the PR's state came back `MERGED`, or right after a successful local squash-merge - never on an unproven assumption:

```bash
git worktree remove .worktrees/<NNN-slug>
git branch -d feature/<NNN-slug>
git push origin --delete feature/<NNN-slug>
```

If `git worktree remove` refuses because of leftover untracked files (e.g. `node_modules`, `.env*` copied in at setup), that's expected - use `git worktree remove --force` for those, never for a worktree still holding unmerged or uncommitted work.
