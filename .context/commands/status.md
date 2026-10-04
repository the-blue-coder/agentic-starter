---
description: "Show the project's framing state and every spec's pipeline stage, derived from files - nothing is stored"
---

You are reporting the current state of the project's agentic pipeline. This command is **read-only**: it never writes, edits, or deletes any file, and never mutates git state (no commits, no branch creation, no checkout). Every Git command you run must be read-only (`status`, `branch --list`, `log`, `worktree list`, etc.). The files on disk and local Git refs are the only state - this command just reads and reports them. There is no pull-request state in this workflow.

Before reporting spec state, scan the primary checkout's `.worktrees/.parallel-batches/` for `manifest.json` and interrupted `manifest.json.tmp` files. For each readable incomplete manifest, report its batch ID, phase, worker passed/total/failed count, review passed/total/failed count, and which recorded worktree paths or feature branches still exist according to `git worktree list`, `git branch --list`, and filesystem checks. If a manifest is corrupt, a temporary manifest remains, or a recorded integration worktree exists without a manifest, report `batch recovery needed`; never repair or delete anything. If a batch is incomplete, recommend `resume <batch-id>` on the command that started it (`/implement-swarm` or `/implement-queue`), and do not recommend starting another spec. A `cleanup-pending` batch may coexist with a fully transferred local target diff; say so explicitly so the user can review it.

---

## Step 1 - Framing state

Check in order and report each prerequisite:

1. **`/init-project` shared context** - check `.context/project-overview.md` and `.context/project-settings.md`.
   - The overview must record the actual project name, a project-specific Overview, goals, core flow, scope, and success criteria, with no unresolved starter placeholders anywhere in the file.
   - Settings must have a concrete `Target branch:`, `Design workspace URL:`, `Test command:`, and `Typecheck command:` keys. A dash is valid for the optional URL or commands when they do not apply. `SEO:` must be exactly `yes`, `no`, or `hybrid`, and `hybrid` also needs a concrete `SEO public scope:`.
   - Complete -> done; missing or still using starter placeholders -> not done, suggest `/init-project`.

2. **`/prd`** - check `.context/framing/prd.md` for project-specific Problem, Core Perimeter, Out of Scope, Success Criteria, and Constraints sections.
   - Complete -> done; missing or incomplete -> not done, suggest `/prd`.

3. **`/architecture`** - open `.context/architecture.md`. The standard sections (including `Testing`) must have no unresolved starter placeholders, and the Stack table's `Frontend` row must be explicit.
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

Use `git worktree list` to locate the primary checkout where the configured target branch is checked out, then inspect it with read-only `git -C <primary-checkout> status --short`. Report `Target checkout: clean` or `Target checkout: local changes present`. Do not infer that every pending file belongs to a specific spec.

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
No feature specs in this checkout. If the target checkout is clean, run /spec to plan a feature; if local changes are pending review, review and resolve them first.
```

and stop after Step 1.

If framing is incomplete, do not print the message above. Report `Spec planning: blocked` and the missing framing commands instead.

---

## Step 3 - Local branch, worktree, and verification state (per spec)

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
git worktree list
```
Report the branch as `local branch` or `no branch`, and separately whether `.worktrees/<spec-id>/` appears in `git worktree list` (`worktree: yes` / `worktree: no`). A completed spec with no worktree and no feature branch has already been handed off to the local target checkout or cleaned up manually.

**Verification record:**
Check whether `.context/docs/verif/<spec-id>.md` exists in the same source selected for the spec (the active worktree when present, otherwise the repository root).
- Missing → `no verification record`.
- Present → read it and report whatever timestamp/commands it records (e.g. "verified <date>, ran: <commands>"). Do not attempt to recompute or compare tree hashes - just note the file exists and summarize what it recorded. Verifying whether that record is still current is `/review-spec-implementation`'s job, not this command's.

---

## Step 4 - Print the table

```
Spec                          Status        Criteria   UI design   Branch       Worktree   Verif
2026_09_27_15_42_31-user-auth done          6/6        present     no branch    no         yes
2026_09_27_15_43_00-export-csv in-progress  4/6        n/a         local branch yes        no
2026_09_27_15_44_10-dashboard-widgets todo   0/5        missing     no branch    no         no
```

Keep columns readable; truncate long titles rather than breaking alignment.

---

## Step 5 - Next command suggestions

If an incomplete parallel-batch manifest exists, print a **Parallel batch** summary with its ID, phase, worker counts, review counts, and remaining worktrees/branches. Recommend only `resume <batch-id>` on the command that started it (`/implement-swarm` or `/implement-queue`) and skip all new-spec/new-implementation suggestions below. If its phase is `cleanup-pending` and transfer is verified, say the target files are ready for local review (or may already have been committed) and the user can directly invoke `/commit-and-push` if changes remain uncommitted; cleanup still must be resumed before starting further implementation.

For a UI spec whose approved design reference is missing and has no explicit prose-only approval, print only this line and skip the other suggestions for that spec:

- `<spec-id> - UI design reference missing: add a reviewed visual reference under .context/feature-specs/design/<spec-id>/ or record the user's prose-only approval before implementation`.

For every remaining spec whose `status` is not `done`, print one suggestion line, tailored to its actual state:

- `todo`, no branch yet → `<spec-id> - todo, no branch yet: run /dev <spec-id> to start` (or `/implement <spec-id>` for the full self-correcting loop).
- `in-progress`, has a branch, unchecked criteria remain → `<spec-id> - has an in-progress branch, unchecked criteria: run /dev <spec-id>` (or `/review-spec-implementation <spec-id>` if all criteria are already checked but status wasn't flipped to done yet).
- `in-progress`, all criteria checked, no verification record → `<spec-id> - all criteria checked, no verification record: run /review-spec-implementation <spec-id>`.
- `in-progress`, verification record present → `<spec-id> - verification recorded; run /review-spec-implementation followed by /review-performance and /review-security (with /review-seo before /review-security only when the spec has `seo: true`; never mention it otherwise) to finish the reviews and hand the changes to the local target branch`.

If `Target checkout` has local changes and at least one `status: done` spec has no active worktree, remind the user to review with VS Code or `git diff HEAD`; only the user's direct `/commit-and-push` invocation authorizes committing and pushing. If the target checkout is clean or a spec is still being implemented, do not print a commit-and-push suggestion.

If no incomplete batch exists, every spec is `done`, and `Target checkout` is clean, print:

```
All specs are done. Run /spec to plan the next feature.
```

If no incomplete batch exists, every spec is `done`, but `Target checkout` has local changes, print:

```
All specs are done. Review the local target-branch changes and directly invoke /commit-and-push when ready; start another spec after the target checkout is clean.
```

---

## Rules

- Never write, edit, or delete any file.
- Never run a Git command that mutates state (no `commit`, `push`, `branch <name>` creation, `checkout`, `merge`, etc.) - only listing/reading commands.
- If any individual check fails (e.g. a file unreadable), report that one line as unknown/unavailable and continue - never abort the whole report over one failed sub-check.
- This command produces a report only. It does not update `.context/progress-tracker.md` or any spec's frontmatter - that stays the job of `/spec`, `/dev`, and `/review-spec-implementation`.
