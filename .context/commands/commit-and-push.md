---
description: "Stage all changes, write a human commit message, commit, and push to origin"
---

You are committing and pushing the current changes on behalf of the developer.

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
- **Spec implementation**: if the diff marks a spec `status: done`, the message must include the spec number and title — e.g. `"implement 005 - batch ingredient add"` or `"add batch ingredient add (spec 005)"`.

## Step 5 - Commit and push

**CRITICAL**: the commit message is the plain `-m` string only. No trailers. No `Co-Authored-By`. No `Generated with`. No AI attribution of any kind. A human developer wrote this commit.

```bash
git commit -m "<your message>"
git push origin HEAD
```

Run commit first, then push sequentially (push depends on commit succeeding).

## Step 6 - Confirm

Report the commit hash and message to the user. One line: `pushed <hash> - <message>`.
