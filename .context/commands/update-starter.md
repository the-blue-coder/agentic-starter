---
description: "Apply a change to the agentic starter only (D:\\Me\\Projects\\.agentic-starter), then commit and push the starter directly"
argument-hint: "<what to change in the starter, or empty to use the current request>"
---

You are updating the **agentic starter**, the template every new project starts from, so a rule or fix learned in the current project is the default in every future project.

**The starter lives at `D:\Me\Projects\.agentic-starter`.** Work there with absolute paths, whatever the current project is.

**Scope: the starter ONLY.** Never edit, commit or push any other project from this command, and never propagate the change to other projects (that is a separate, explicit request). The current project's own files are not part of this command either: if the current project also needs the change, it is done (and committed) separately, as the user asks.

## Step 1 - Define the change

Take the change from `$ARGUMENTS`. When it is empty or refers to the conversation ("this", "the same", "what we just did"), take it from the current request and the work just done in this session. Restate the change in one sentence before touching anything. If what to change is still ambiguous, ask once; never guess the scope.

## Step 2 - Check the starter

- `git -C D:/Me/Projects/.agentic-starter status --short`: if the working tree holds uncommitted changes that are not yours, stop and report them instead of mixing them into this commit.
- Note the current branch (`git branch --show-current`) and confirm `origin` exists.
- Read the starter files the change belongs in (conventions in `.context/coding-conventions/`, commands in `.context/commands/` with their wrappers, stack recipes in `.context/stacks/`, templates, `docs/`), and find every place that already states the rule so it is changed everywhere at once and never contradicts itself.

## Step 3 - Apply the change

- **Write it generically.** The starter serves every future project: never name the current project, its domain, its brand or its real values. Use the starter's placeholders and examples (`[project_slug]`, `APP_NAME`, "for example ...").
- **Write it explicitly.** A rule says what to do, what never to do, and why in one line, with a ❌/✅ example when it is a code rule and a Quick Reference row when the file has one.
- Follow the starter's own conventions for the files you touch (headings, tables, wording, line endings).
- A **new command** gets its body in `.context/commands/<name>.md` and both thin wrappers, `.claude/commands/<name>.md` and `.opencode/commands/<name>.md` ("Read `.context/commands/<name>.md` and follow its instructions exactly."), plus its row in `docs/commands.md` and its mention in `docs/whats-included.md`.
- Add one line to `CHANGELOG.md` under `## [Unreleased]` (in the matching `### Added`, `### Changed`, `### Removed` or `### Fixed` section) saying what changed and where.

## Step 4 - Commit and push the starter directly

Invoking `/update-starter` authorizes this commit and push; do not ask again.

1. Stage only the files this change touched, by name (never `git add -A` or `git add .`).
2. Commit with one imperative, lowercase line under 72 characters, no period, in the style of the starter's recent human commits (`git log --format="%s" -10`), with no AI attribution or trailers.
3. `git push origin HEAD`, never `--force`. If the push fails, leave the commit as it is and report the error.

## Step 5 - Report

One short summary: what changed, the files touched, and `pushed <hash> - <message>` (or the push error). Say nothing was propagated to other projects.
