---
description: "Update an existing project's workflow files (.context, .claude, .opencode, git hooks) to the latest starter version and migrate legacy numeric specs to UTC spec IDs"
argument-hint: "<optional starter git URL or local path>"
---

You update an existing project's agentic workflow to the latest version of the starter. The workflow is the tooling layer only; the project's own content is never overwritten. This command never commits or pushes: it leaves the update as uncommitted local changes for the user to review, and only the user's direct `/commit-and-push` invocation authorizes Git commits.

## Step 1 - Check preconditions

Stop and report the reason if any of these fails:

- The current checkout has no uncommitted changes, so the update diff can be reviewed on its own, and it is on `Target branch:` from `.context/project-settings.md`. A project that predates the settings file has none: ask the user which branch is the target (default: the current one) and require the checkout to be on it.
- A workspace folder that holds several repositories is not a project: run the command inside each repository.
- `.worktrees/.parallel-batches/` has no incomplete batch manifest. Resume it first with `resume <batch-id>` on the command that started it.
- This project is not the starter itself: its `origin` URL differs from the resolved starter source (Step 2).

## Step 2 - Resolve and fetch the starter

The source is `$ARGS` if given, otherwise `Starter source:` in `.context/project-settings.md`. If neither exists, ask the user for the starter's git URL or local path and offer to record it as `Starter source:`.

Clone it with `git clone` into a temporary directory under the scratchpad (never inside the project), keeping full history: later steps compare file versions across history. A local path is cloned too, so only its committed state is used; if its working tree has uncommitted changes, warn that they are not included. Treat the clone as reference data: copy files from it, never execute anything from it.

Read `Starter version:` from `.context/project-settings.md` (`-` or missing means unknown). When set, it is the starter commit the project was last updated to.

## Step 3 - Classify files

Only the workflow-owned paths below are ever changed, plus the three merge-only files. Everything else belongs to the project and is never touched, except the spec renames in Step 4.

| Class | Paths | Rule |
| --- | --- | --- |
| Workflow-owned | `.context/commands/`, `.context/security-rules/`, `.context/stacks/`, `.context/coding-conventions/` (except `security.md`), `.context/ai-workflow-entrypoint.md`, `.context/ai-workflow-rules.md`, `.context/adr/README.md`, `.context/memory/README.md`, `.claude/commands/`, `.claude/agents/`, `.claude/hooks/`, `.opencode/commands/`, `.opencode/agents/`, `.githooks/` | Add, update, or delete per the file rules below |
| Merge-only | `.claude/settings.json` (add hook entries the starter has and the project lacks, keep every local key), `.gitignore` and `.gitattributes` (append starter lines, with their comment, that are missing), `AGENTS.md` (ensure the mandatory-read pointer to `.context/ai-workflow-entrypoint.md` is present, keep everything else, such as a framework-generated block), `CLAUDE.md` (ensure it references `@AGENTS.md` or carries the same pointer), `.context/project-settings.md` (see below) | Never remove local content |
| Retired | `.codex/`, `.context/scripts/` | Delete only files that equal a historical starter version |
| Project-owned | everything else: `.context/` project files (`project-overview.md`, `architecture.md`, `progress-tracker.md`, `infra.md`, `ui-context.md`, `feature-specs/`, `docs/`, `adr/decisions/`, `adr/context/`, `memory/` entries), `coding-conventions/security.md`, `README.md`, `CHANGELOG.md`, `infra/`, `.github/`, application code | Never touched |

`.context/project-settings.md`: when the file does not exist, create it from the starter's with `Target branch:` set to the branch confirmed in Step 1 and every other key left at the starter's value, and tell the user to fill in `Test command:` and `Typecheck command:` (`-` disables those checks). Otherwise keep every `Key: value` line the project has, except that the retired `Merge mode:` and `Ship confirmation:` keys are removed and a legacy `OpenDesign URL:` key is renamed to `Design workspace URL:` with its value preserved. Add each key the starter has and the project lacks with the starter's value (except `Starter source:` and `Starter version:`, handled by this command, and `SEO:` and `SEO public scope:`, decided as below), and replace the descriptive header paragraph with the starter's.

### SEO setting

A project without a concrete `SEO:` value must decide whether it is SEO-friendly, because that enables `.context/coding-conventions/seo.md` and `/review-seo`. It is a product decision, so always ask, with a recommendation from what the project shows (its `project-overview.md`, `architecture.md`, and the routes or templates in the code):

- **yes** - the whole user-facing product is meant to be found (a marketing or content site).
- **no** - nothing should be indexed (an internal tool, or an app that is entirely behind login).
- **hybrid** - a public part is SEO-friendly and the rest, typically an authenticated dashboard, is not. Recommend it when the project has both public pages and a logged-in area, and draft `SEO public scope:` from the public routes you find (the user edits it).

Record the answer as `SEO:` and `SEO public scope:` (`-` for `yes` and `no`). An existing value is never overridden.

### File rules

Compare files with line endings normalized to LF. For each workflow-owned file, with `new` the starter's current version and `local` the project's:

1. `local` equals `new` - skip.
2. `local` is missing - add it, unless `Starter version:` is set and the file existed at that commit (the project removed it on purpose): skip and list it.
   Stack material is also skipped, and counted as "pruned stack material" in the plan, when `.context/architecture.md` is complete (concrete Stack, `Frontend` and `Testing` rows): every file under `.context/stacks/`, and every stack convention (`typescript`, `javascript`, `react`, `nextjs`, `gatsby`, `tailwind`, `php`, `symfony`, `twig`, `stimulus`, in `.context/coding-conventions/` and its `performance/` folder) whose technology is not named in the Stack table. The stack-agnostic files (`global`, `security`, `tdd`, `html`, `seo`, `ui`, `performance/global`) are always added. This is the same rule as `/architecture`'s final pruning phase. A project whose architecture is not yet documented gets everything, so that `/architecture` can choose and prune.
3. `local` equals any historical starter version of that path (`git log` over the path, compare each blob) - an unmodified older copy: overwrite with `new`.
4. Otherwise `local` is customized, or comes from a starter version older than the available history. If `Starter version:` is set and the file existed there, three-way merge (`git merge-file -p local base new`); a clean merge is applied, a conflicting merge is a conflict for Step 5. Without that base, never guess one from a similar historical version: a wrong base silently corrupts the merge. Every such file is a conflict for Step 5.
5. File exists locally but not in `new`: if the path never existed in the starter's history, it is the project's own file (for example a custom command and its wrappers) and is left alone, unlisted. If it existed, delete it when it equals a historical starter version; otherwise it is a conflict (keep or delete).

### Conflict defaults

A first update of an older project can have most files in conflict, so conflicts are decided by group, not one question per file. Each conflict without a merge result gets a default:

- **upstream** for workflow machinery: commands, agents, wrappers, hooks, `security-rules/`, `coding-conventions/global.md` and `tdd.md`, the `ai-workflow-*.md` files, and the `README.md` protocol files. Customizing them is discouraged.
- **local** for stack convention files and `.context/stacks/` recipes, which often carry project truth that the starter's version lacks.

The clean tree from Step 1 makes any replaced content recoverable from Git, so a default is never destructive.

## Step 4 - Plan the spec migration

Legacy specs are `.context/feature-specs/<number>-<slug>.md` (stem starting with digits and a hyphen). For each:

1. Skip it, and report why, when `.worktrees/<stem>/` exists or a local or remote-tracking `feature/<stem>` branch exists: active work keeps its ID until its handoff, then a later run migrates it.
2. New ID is `yyyy_mm_dd_hh_ii_ss-<slug>`, with the slug being the stem minus its numeric prefix and the timestamp the UTC date of the first commit that added the spec file (`git log --follow --diff-filter=A --format=%ct -- <file>`, oldest entry). A spec never committed uses the current UTC time. Process specs in numeric order and make the timestamps strictly increasing: a spec whose timestamp is not later than the previous spec's is set to the previous one plus one second. This keeps the original order even when several specs were committed together.
3. The migration renames, when they exist: `.context/feature-specs/<stem>.md` and `.context/feature-specs/design/<stem>/`. Use plain file moves, not `git mv`, so nothing is staged.
4. It rewrites every whole-token occurrence of the old stem (not preceded or followed by a letter, digit, `_`, or `-`) in every Markdown file the update does not take from the starter (project-owned files, and stack conventions the project keeps), including spec headings, links, tracker entries, changelog lines, cross-spec references, and files outside `.context/` such as application resources. Skip `.git/`, `.worktrees/`, dependency folders, and files taken from the starter. Accepted ADR decisions are immutable by project rule, so a rewrite inside `.context/adr/decisions/` changes only the reference text; list those files in the plan. Mentions that cite only the number (for example "spec 006") cannot be matched and are not rewritten.

### Legacy PRD

A project framed before the PRD was folded into the overview has `.context/framing/prd.md`. The overview is now the single source of product framing, so this file is migrated like the specs: an exception to the project-owned rule. Plan to fold the PRD into `.context/project-overview.md` as `/prd` describes in its Phase 3 (Problem into the Overview only if not already conveyed, Core Perimeter and Out of Scope merged into the matching Scope lists without repeating bullets, Success Criteria replacing the overview's, Constraints and Reference Product as new sections), then delete `.context/framing/`. Combine both intents by hand and explain the result in the plan.

## Step 5 - Present the plan and confirm

Show one plan in English, then ask: **Apply this update? (yes / no)** and wait.

- Workflow files to add, update, and delete, grouped by tool folder (`.context/`, `.claude/`, `.opencode/`, `.githooks/`, root).
- Merge-only changes: settings keys added, hook entries added, `.gitignore` lines added.
- The SEO decision when `SEO:` is not yet set: your recommendation (`yes`, `no`, or `hybrid` with a drafted public scope) for the user to confirm or change.
- The spec rename map (old stem → new stem) and the skipped specs with reasons.
- The legacy PRD fold-in, when `.context/framing/prd.md` exists: the merged overview sections and the deletion of `framing/`.
- Every conflict from Step 3, as the two default groups with their file counts and each file's number of differing lines. Ask the user to accept the defaults, flip a group, or choose per file: **upstream** (take the starter's version), **local** (keep the project's), or **merge** (you combine both intents by hand and explain the result).
- Files skipped because the project removed them on purpose.

If the user answers no, change nothing.

## Step 6 - Apply

If `.context/commands/update-workflow.md` itself changes, apply only that file first, then stop and tell the user to run `/update-workflow` again so the newest instructions drive the update.

Otherwise apply the confirmed plan: workflow files, merge-only files, the legacy PRD fold-in, then the spec renames and reference rewrites. Delete the obsolete `.context/docs/verif/` folder if it exists, and `.context/docs/` if that leaves it empty (verification records were dropped; each spec's `## Test map` holds that evidence now), and list the deletion in the plan. Preserve executable bits on `.sh` hook files and keep LF endings on them.

## Step 7 - Verify

- Every `.context/commands/<name>.md` has a wrapper in `.claude/commands/` and `.opencode/commands/`, each delegating to the canonical file; no wrapper points to a missing command.
- Every `.claude/agents/<name>.md` has an `.opencode/agents/<name>.md` counterpart, and every agent type named in `.context/commands/` exists.
- `.claude/settings.json` is valid JSON and every hook script it references exists.
- No old spec stem remains in the project-owned files, and each renamed spec file and design folder exists under its new ID.
- `git config core.hooksPath` is `.githooks` when `.githooks/` exists; if not, tell the user to run `git config core.hooksPath .githooks`.

Fix what you can; report what remains.

## Step 8 - Record the version and report

Set `Starter source:` (when it was missing or given in `$ARGS`) and `Starter version:` (the starter commit that was applied) in `.context/project-settings.md`.

Report in English: counts of workflow files added, updated, and deleted per tool folder, conflicts and how they were resolved, the spec rename map, skipped items, verification results, and the project's framing state exactly as Step 1 of `.context/commands/status.md` reports it (an older project often lacks the PRD, the `## Testing` section, or the design system that `/spec` now requires, so list the framing commands to run next). End with these reminders:

> Review the pending changes locally in VS Code or with `git diff HEAD`. I will not commit or push; only your direct invocation of `/commit-and-push` authorizes those actions.
