---
description: "Show the project's framing state and every spec's pipeline stage, derived from files - nothing is stored"
---

You are reporting the current state of the project's agentic pipeline. This command is **read-only**: it never writes, edits, or deletes any file, and never mutates git state (no commits, no branch creation, no checkout). Every git/gh command you run must be read-only (`status`, `branch --list`, `branch -r --list`, `log`, `pr list`, etc.). The files on disk (and the local/remote git refs) are the only state - this command just reads and reports them.

---

## Step 1 - Framing state

Check in order and report each prerequisite:

1. **`/init-project` shared context** - check `.context/project-overview.md` and `.context/project-settings.md`.
   - The overview must record the actual project name, a project-specific Overview, goals, core flow, scope, and success criteria, with no unresolved starter placeholders anywhere in the file.
   - Settings must have a concrete `Target branch:`, `Ship confirmation: human`, `Design workspace URL:`, `Test command:`, and `Typecheck command:` keys. A dash is valid for the optional URL or commands when they do not apply.
   - Complete -> done; missing or still using starter placeholders -> not done, suggest `/init-project`.

2. **`/prd`** - check `.context/framing/prd.md` for project-specific Problem, Core Perimeter, Out of Scope, Success Criteria, and Constraints sections.
   - Complete -> done; missing or incomplete -> not done, suggest `/prd`.

3. **`/architecture`** - open `.context/architecture.md`. The standard sections must have no unresolved starter placeholders, and the Stack table's `Frontend` row must be explicit.
   - Complete -> done; missing, incomplete, or blank Frontend row -> not done, suggest `/architecture`. For a new project, run `/prd` first so architecture can make an informed choice; for an existing project, architecture documents the detected stack. Use `None` (or `-`) for a backend-only project.

4. **`/design-system`** - only classify applicability after the architecture's Frontend row is complete. A concrete Frontend value means UI; `None` or `-` means there is no user-facing UI.
   - Blank or placeholder Frontend row -> applicability unknown; report that `/architecture` must fill the row first. Do not classify the project as backend-only or suggest `/design-system` yet.
   - No UI -> not applicable.
   - UI project: `.context/ui-context.md` must have no unresolved starter placeholders and include a finished `## Contrast Audit`: no unresolved `FAIL`, `UNVERIFIED`, or placeholder values; every exception records its scope and explicit user approval.
   - Complete -> done; missing or incomplete -> not done, suggest applying approved UI stack setup if needed, then `/design-system`.

Print one line per prerequisite and an overall result, for example:

```
Framing
  [x] /init-project - shared project context and required settings are complete
  [x] /prd           - project-specific product framing is complete
  [ ] /architecture  - Frontend row is blank -> run /architecture
  [ ] /design-system - applicability unknown until /architecture fills the Frontend row
Spec planning: blocked until all applicable framing items are complete.
```

If framing is incomplete, report the missing commands in order: `/init-project`, `/prd`, `/architecture`, then approved UI stack setup if needed and `/design-system` for UI projects. Do not suggest `/spec` until all applicable prerequisites pass.

---

## Step 2 - Collect specs

List every file matching `.context/feature-specs/*.md` (ignore `.gitkeep`). For each:

1. Derive `<spec-id>` from the complete filename stem (drop only `.md`; this supports new timestamp IDs and legacy numeric IDs) and check whether `.worktrees/<spec-id>/.context/feature-specs/<spec-id>.md` exists. If so, use that worktree copy for the status, title, criteria count, and UI metadata; it is the active execution record.
2. Read the `status:` frontmatter (`todo` / `in-progress` / `done`).
3. Read the title (the `# <spec-id> - Feature Name` heading).
4. Count acceptance criteria: `- [x]` (done) vs `- [ ]` (pending) under `## Acceptance Criteria`. Report as `done/total`.
5. Read `ui:` from the spec frontmatter (`true` / `false`). If it is absent on a legacy spec, infer from its **Design Reference** section or report the design state as `unknown`.
6. Use the corresponding design directory in the same source (repository root or active worktree).

If no spec files exist (besides `.gitkeep`) and framing is complete, print:

```
No feature specs in this checkout. If a spec PR was recently merged, fast-forward the target branch before creating the next one; otherwise run /spec to plan a feature.
```

and stop after Step 1.

If framing is incomplete, do not print the message above. Report `Spec planning: blocked` and the missing framing commands instead.

---

## Step 3 - Branch, verification record, and PR state (per spec)

For each spec, run read-only checks:

**Design reference:**
- `ui: false` → `n/a`.
- UI spec and its `.context/feature-specs/design/<spec-id>/` directory has at least one inspectable visual reference beyond `brief.md` and `index.md` in the chosen source (repository root or active worktree) → `present`.
- UI spec with no reviewed visual reference, but **Open Questions** contains `Prose-only design approved by user; no design files provided.` → `prose-only (approved)`.
- UI spec with no reviewed visual reference in the chosen source, with no explicit prose-only approval → `missing`.
- Legacy spec with no UI metadata or Design Reference section → `unknown`.

**Branch and worktree:**
```bash
git branch --list "feature/<spec-id>"
git branch -r --list "*/feature/<spec-id>"
git worktree list
```
Report the branch as one of: `no branch`, `local branch`, `remote branch`, `local + remote` - and separately, whether `.worktrees/<spec-id>/` shows up in `git worktree list` (`worktree: yes` / `worktree: no`). A branch with no worktree usually means the spec was shipped and cleaned up (see `/commit-and-push` Step 8) while the remote branch still lingers, or the worktree was removed manually - either way it's informational, not an error.

**Verification record:**
Check whether `.context/docs/verif/<spec-id>.md` exists in the same source selected for the spec (the active worktree when present, otherwise the repository root).
- Missing → `no verification record`.
- Present → read it and report whatever timestamp/commands it records (e.g. "verified <date>, ran: <commands>"). Do not attempt to recompute or compare tree hashes - just note the file exists and summarize what it recorded. Verifying whether that record is still current is `/review-spec-implementation`'s job, not this command's.

**Pull request:**
If the `gh` CLI is available and authenticated, run:
```bash
gh pr list --head "feature/<spec-id>" --state all --json number,state,url
```
Report the PR number/state/URL if one exists, or `no PR`.

If `gh` is not installed, not authenticated, or the command errors for any other reason, degrade gracefully: report `PR state unknown (gh unavailable)` and continue - never let this fail the whole command.

---

## Step 4 - Print the table

```
Spec                          Status        Criteria   UI design   Branch            Worktree   Verif   PR
2026_09_27_15_42_31-user-auth done          6/6        present     local + remote    no         yes     merged #12
2026_09_27_15_43_00-export-csv in-progress  4/6        n/a         local             yes        no      no PR
2026_09_27_15_44_10-dashboard-widgets todo   0/5        missing     no branch         no         no      no PR
```

Keep columns readable; truncate long titles rather than breaking alignment.

---

## Step 5 - Next command suggestions

For any spec whose PR is `MERGED` while its worktree is still present, print:

- `<spec-id> - PR merged, worktree still present: directly invoke $commit-and-push in Codex or /commit-and-push elsewhere to finish cleanup`.

For a UI spec whose approved design reference is missing and has no explicit prose-only approval, print only this line and skip the other suggestions for that spec:

- `<spec-id> - UI design reference missing: add a reviewed visual reference under .context/feature-specs/design/<spec-id>/ or record the user's prose-only approval before implementation`.

For every remaining spec whose `status` is not `done` and whose PR is not `MERGED`, print one suggestion line, tailored to its actual state:

- `todo`, no branch yet → `<spec-id> - todo, no branch yet: run $dev <spec-id> in Codex or /dev <spec-id> elsewhere to start` (or `$implement <spec-id>` in Codex / `/implement <spec-id>` elsewhere for the full self-correcting loop).
- `in-progress`, has a branch, unchecked criteria remain → `<spec-id> - has an in-progress branch, unchecked criteria: run $dev <spec-id> in Codex or /dev <spec-id> elsewhere` (or `/review-spec-implementation <spec-id>` if all criteria are already checked but status wasn't flipped to done yet).
- `in-progress`, all criteria checked, no verification record → `<spec-id> - all criteria checked, no verification record: run /review-spec-implementation <spec-id>`.
- `in-progress`, verification record present, no PR yet → `<spec-id> - verified, ready to ship: you may directly invoke $commit-and-push in Codex or /commit-and-push elsewhere to push the feature branch and open its single PR`. Never invoke that command for the user.

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
