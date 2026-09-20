---
description: "Show the project's framing state and every spec's pipeline stage, derived from files - nothing is stored"
---

You are reporting the current state of the project's agentic pipeline. This command is **read-only**: it never writes, edits, or deletes any file, and never mutates git state (no commits, no branch creation, no checkout). Every git/gh command you run must be read-only (`status`, `branch --list`, `branch -r --list`, `log`, `pr list`, etc.). The files on disk (and the local/remote git refs) are the only state - this command just reads and reports them.

---

## Step 1 - Framing state

Check, in order:

1. **`/prd`** - does `.context/framing/prd.md` exist?
   - Exists → done.
   - Missing → not done, suggest `/prd`.

2. **`/architect`** - open `.context/architecture.md`. Does it still contain `[bracketed]` placeholders (e.g. `[e.g. Symfony, Express, Django]`)?
   - No placeholders left → done.
   - Still has placeholders → not done, suggest `/architect` (or `/init-project` if the project hasn't been bootstrapped at all).

3. **`/design-system`** - only applicable to UI projects. Determine this from `.context/architecture.md`'s Stack table: if the `Frontend` row is filled in (not a `[bracketed]` placeholder) and not something like "none" / "-", treat the project as a UI project.
   - Not a UI project → skip this line entirely (don't print it).
   - UI project: open `.context/ui-context.md` and check whether it has a `## Contrast Audit` section.
     - Present → done.
     - Absent → not done, suggest `/design-system`.

Print one line per applicable step, e.g.:

```
Framing
  [x] /prd          - .context/framing/prd.md exists
  [ ] /architect     - .context/architecture.md still has [bracketed] placeholders -> run /architect
  [ ] /design-system - .context/ui-context.md has no ## Contrast Audit section -> run /design-system
```

---

## Step 2 - Collect specs

List every file matching `.context/feature-specs/*.md` (ignore `.gitkeep`). For each:

1. Read the `status:` frontmatter (`todo` / `in-progress` / `done`).
2. Read the title (the `# NNN - Feature Name` heading).
3. Count acceptance criteria: `- [x]` (done) vs `- [ ]` (pending) under `## Acceptance Criteria`. Report as `done/total`.
4. Derive `NNN-slug` from the filename (drop the `.md` extension) - this is the expected branch name suffix: `feature/NNN-slug`.

If no spec files exist (besides `.gitkeep`), print:

```
No feature specs yet. Run /spec to create the first one.
```

and stop after Step 1.

---

## Step 3 - Branch, verification record, and PR state (per spec)

For each spec, run read-only checks:

**Branch:**
```bash
git branch --list "feature/<NNN-slug>"
git branch -r --list "*/feature/<NNN-slug>"
```
Report one of: `no branch`, `local branch`, `remote branch`, `local + remote`.

**Verification record:**
Check whether `.context/docs/verif/<NNN-slug>.md` exists.
- Missing → `no verification record`.
- Present → read it and report whatever timestamp/commands it records (e.g. "verified <date>, ran: <commands>"). Do not attempt to recompute or compare tree hashes - just note the file exists and summarize what it recorded. Verifying whether that record is still current is `/review-spec-implementation`'s job, not this command's.

**Pull request:**
If the `gh` CLI is available and authenticated, run:
```bash
gh pr list --head "feature/<NNN-slug>" --state all --json number,state,url
```
Report the PR number/state/URL if one exists, or `no PR`.

If `gh` is not installed, not authenticated, or the command errors for any other reason, degrade gracefully: report `PR state unknown (gh unavailable)` and continue - never let this fail the whole command.

---

## Step 4 - Print the table

```
Spec                          Status        Criteria   Branch            Verif   PR
001 - user-auth               done          6/6        local + remote    yes     merged #12
002 - export-csv               in-progress   4/6        local             no      no PR
003 - dashboard-widgets        todo          0/5        no branch         no      no PR
```

Keep columns readable; truncate long titles rather than breaking alignment.

---

## Step 5 - Next command suggestions

For every spec whose `status` is not `done`, print one suggestion line, tailored to its actual state:

- `todo`, no branch yet → `NNN - todo, no branch yet: run /dev NNN to start` (or `/implement NNN` for the full self-correcting loop).
- `in-progress`, has a branch, unchecked criteria remain → `NNN - has an in-progress branch, unchecked criteria: run /dev NNN` (or `/review-spec-implementation NNN` if all criteria are already checked but status wasn't flipped to done yet).
- `in-progress`, all criteria checked, no verification record → `NNN - all criteria checked, no verification record: run /review-spec-implementation NNN`.
- `in-progress`, verification record present, no PR yet → `NNN - verified, ready to ship: run /commit-and-push` (branch checked out) or note the PR should be opened per `Merge mode` in `.context/project-settings.md`.

If every spec is `done`, print:

```
All specs are done. Run /spec to plan the next feature.
```

---

## Rules

- Never write, edit, or delete any file.
- Never run a git or gh command that mutates state (no `commit`, `push`, `branch <name>` creation, `checkout`, `merge`, `pr create`, `pr merge`, etc.) - only listing/reading commands.
- If any individual check fails (e.g. `gh` missing, a file unreadable), report that one line as unknown/unavailable and continue - never abort the whole report over one failed sub-check.
- This command produces a report only. It does not update `.context/progress-tracker.md` or any spec's frontmatter - that stays the job of `/spec`, `/dev`, and `/review-spec-implementation`.
