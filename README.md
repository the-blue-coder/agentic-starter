> **To start a new project, clone this repo. To add the starter workflow to an existing project, copy the starter files into it. Then run:**
>
> ```
> /init-project
> ```
>
> To bring a project that already uses the starter up to date later, run `/update-workflow`.

# agentic-starter

A stack-agnostic starter for building projects with Claude Code, OpenCode, or another local coding agent, following a **Spec-Driven Development (SDD)** workflow. It ships the agentic tooling layer only - no application code - so it works with whatever backend, frontend, and hosting you choose.

```mermaid
flowchart LR
  init["/init-project<br/>shared setup"] --> prd["/prd<br/>once"]
  prd --> arch["/architecture<br/>choose or document"]
  arch --> setup["Apply approved stack setup<br/>separately for new projects"]
  setup --> ui{"User-facing UI?"}
  ui -- no --> spec["/spec<br/>one per feature"]
  ui -- yes --> design["/design-system<br/>once"]
  design --> spec
  spec --> implement["/implement<br/>one spec"]
  spec --> queue["/implement-queue<br/>several specs in series, autonomous"]
  spec --> parallel["/implement-swarm<br/>several specs in parallel, autonomous"]
  implement --> handoff["Manual hand-off<br/>no automatic commit or push"]
  queue --> handoff
  parallel --> handoff
  handoff --> review["User reviews uncommitted changes<br/>on the local target branch"]
  review --> ship["Direct user invocation<br/>/commit-and-push"]
  ship --> push["Commit and push target branch"]
```

## What's included

- **`.context/`** - the project's persistent context: architecture, conventions, progress tracking, feature specs, and a small memory system for decisions and corrections. See `.context/ai-workflow-entrypoint.md` for the full read order.
- **`.context/project-settings.md`** - project-specific settings: target branch, optional design workspace URL, and the test/typecheck commands the pipeline runs. Each spec gets a temporary local worktree and branch; verified changes are reviewed on the local target branch. The workflow creates no PRs.
- **`.context/stacks/`** - stack-specific architecture and setup recipes. `/architecture` may consult them as examples after learning the product constraints; they are not a closed menu, and `/init-project` never selects or executes one. Apply an approved recipe separately after the architecture decision.
- **`.context/coding-conventions/`** - shared rules plus language/framework guidance for supported stacks (Symfony API and Twig fullstack, Next.js, Gatsby, plus TDD, security, performance, and styling). Each stack file is modeled on a real reference project and describes its `src/` layout. Keep these reference files intact; read the ones matching the architecture documented in `.context/architecture.md`.
- **Commands and agents**, mirrored across tools (`.claude/`, `.opencode/`) so the workflow is the same regardless of which local coding agent you use:
  - `/init-project` → `/prd` → `/architecture` → approved stack setup (separate step, if needed) → `/design-system` for UI projects - framing before the first `/spec`
  - `/spec` → `/implement` - the feature pipeline (TDD implementation, spec verification, conventions, performance, and security review, looped until clean)
  - `/implement-queue` - autonomously implements several specs one after another, each on top of the previous verified result, and ends with a decision report
  - `/implement-swarm` - autonomously implements several independent specs concurrently, integrates their verified diffs, and ends with a decision report
  - `/status` - shows the project's framing state and every spec's pipeline stage, derived entirely from files and read-only Git queries
  - `/review-changes`, `/review-performance`, `/review-security` - convention/performance/security sweeps over local changes
  - `/init-project` - set up shared project context and workflow settings without choosing a stack
  - `/setup-backup`, `/setup-rolling-deploy`, `/teardown-rolling-deploy` - infra runbooks (currently only implemented for the `symfony-nextjs-contabo` recipe)
  - `/update-workflow` - updates an existing project's workflow files (`.context/`, `.claude/`, `.opencode/`, git hooks) to the latest starter version and migrates legacy numeric specs to UTC IDs
  - `/commit-and-push`, `/add-new-color`, `/just-respond`
- **`infra/`** - reference deploy scripts and nginx configurations for the supported stack recipes; stack-specific setup is applied separately.
- **`.github/workflows/`** - CI/CD examples matching the current stack recipes; they are not installed or selected by `/init-project`.
- **`.githooks/pre-commit`** - a plain git hook (not tool-specific): refuses a commit on a `feature/<spec-id>` branch unless that spec exists and `/dev` has picked it up. The normal workflow transfers reviewed changes to the target branch before the user-authorized commit. Activated once per clone when `/init-project` initializes the shared workflow (`git config core.hooksPath .githooks`), so it applies regardless of which AI tool is committing.

**Commit and push require a direct user command.** `/spec`, `/dev`, `/implement`, `/implement-queue`, `/implement-swarm`, quick fixes, and reviews never commit, push, or invoke the commit-and-push command automatically. Only when you directly call `/commit-and-push` does the agent run its commit and push workflow.

## AI Development workflow

Context and conventions live in `.context/` - start with `.context/ai-workflow-entrypoint.md` (also linked from `AGENTS.md`/`CLAUDE.md`).

The command names below use slash notation for readability. Claude Code and OpenCode both use slash commands (for example, `/spec`, `/implement`, and `/commit-and-push`) and follow the same canonical instructions in `.context/commands/`.

### Framing (once)

Run `/init-project` to populate shared project context and workflow settings without choosing a stack. Then run `/prd` and `/architecture` manually, one at a time. For a new project, apply approved stack-specific setup separately if needed; run `/design-system` for UI projects once the UI stack and its tokens exist. `/spec` is blocked until shared initialization, the PRD, architecture, and (for UI projects) the design system are complete. Repeat framing later only if the documented product or architecture has drifted.

```mermaid
flowchart LR
  init["/init-project<br/>shared setup"] --> prd["/prd<br/>once"]
  prd --> architecture["/architecture<br/>choose or document"]
  architecture --> setup["Apply approved stack setup separately"]
  setup --> ui{"User-facing UI?"}
  ui -- no --> firstSpec["Ready for the first /spec"]
  ui -- yes --> design["/design-system<br/>once"]
  design --> firstSpec
```

| Command | What it does |
| --- | --- |
| `/init-project` | Sets up shared project context and workflow settings; does not choose or bootstrap a stack |
| `/prd` | Frames the product: problem, perimeter, out-of-scope, success criteria - writes `.context/framing/prd.md` |
| `/architecture` | Chooses and documents architecture for a new project, or documents the actual architecture of an existing codebase |
| `/design-system` | UI projects only - locks design tokens and a contrast audit into `.context/ui-context.md` |

### Day-to-day work: two paths

**Quick fixes** (bugs, typos, small corrections - ≤ 3 files, no new feature): write code directly, no pipeline needed. Once the code is written, the agent runs `/review-changes` and `/review-performance`, then `/review-security` last. `/review-performance` reports "Not applicable" on its own when the diff has no query or network call, loop, UI rendering, dependency change, or file handling.

```mermaid
flowchart LR
  fix["Quick fix<br/>≤ 3 files, no new feature"] --> code["Write code directly"]
  code --> changes["/review-changes"]
  code --> perf{"Query, loop, UI rendering,<br/>dependency or file handling<br/>in the diff?"}
  perf -- yes --> performance["/review-performance"]
  perf -- no --> na["/review-performance<br/>reports Not applicable"]
  changes --> security["/review-security<br/>always last"]
  performance --> security
  na --> security
  security --> handoff["Hand off the reviewed changes<br/>user invokes /commit-and-push"]
```

**Features**: framing once, then the per-spec pipeline repeats for every feature:

```
/init-project → /prd → /architecture → approved stack setup (if needed) → /design-system (UI projects) → /spec
/spec → /implement                     (repeats, once per feature)
```

Use `/implement-queue <spec-id-or-file> <spec-id-or-file> [...]` when at least two already planned specs are ready and should run one after another (put dependencies first), or `/implement-swarm <spec-id-or-file> <spec-id-or-file> [...]` when they are independent and can run concurrently. Both run autonomously and never commit. You can pass exact IDs or drag and drop the `.md` spec files into any of these commands; their local `file:///...` URLs are resolved and checked against the current checkout. `/dev` and `/implement` accept the same file selectors, along with their existing name-fragment lookup.

### Per-spec cycle

Each new spec uses a UTC ID in `yyyy_mm_dd_hh_ii_ss-spec-title` format (for example, `2026_09_27_15_42_31-add-search`). It gets its own temporary worktree, `.worktrees/<spec-id>/`, on a local branch `feature/<spec-id>` - one spec, one worktree, one branch, no PR. Existing numeric spec IDs remain supported. `/dev` creates the worktree and brings the spec and its design handoff into it; later commands resolve that worktree rather than assuming the session is already sitting inside it. Once implementation, spec verification, convention review, performance review, and security review pass, the verified changes are transferred to the configured local target branch as uncommitted, unstaged changes. The worktree and feature branch are removed after the transfer is verified.

```mermaid
flowchart TD
  spec["/spec<br/>clarify and define one feature"] --> ui{"User-facing UI?"}
  ui -- yes --> designTool["Use any design tool<br/>(e.g. OpenDesign)"]
  designTool --> export["Review brief.md and add visual references to<br/>.context/feature-specs/design/{spec-id}/"]
  ui -- no --> dev["/dev<br/>create feature/{spec-id} worktree"]
  export --> dev
  export --> batch["/implement-queue or /implement-swarm<br/>several specs, autonomous"]
  ui -- no --> batch
  batch --> dev

  subgraph reviewLoop["Implementation and review: /implement, /implement-queue, /implement-swarm, or individual commands"]
    dev --> verify["/review-spec-implementation"]
    verify --> conventions["/review-changes"]
    conventions --> performance["/review-performance"]
    performance --> security["/review-security"]
    security --> clean{"All checks pass?"}
    clean -- no --> dev
    clean -- yes --> done["Spec marked done"]
  end

  done --> handoff["Transfer verified changes to local target branch<br/>remove temporary worktree and branch"]
  handoff --> localReview["User reviews on local target branch<br/>in VS Code or terminal"]
  localReview --> gate["Manual authorization<br/>only the user invokes commit-and-push"]
  gate --> ship["/commit-and-push"]
  ship --> pushed["Commit and push the target branch"]
```

| Command | What it does |
| --- | --- |
| `/spec` | Explicitly classifies whether the feature has user-facing UI. UI specs may use any design tool (OpenDesign is one example) and include reviewed, versioned design references under `.context/feature-specs/design/`; non-UI specs skip design. The spec and handoff are shared across coding agents. |
| `/implement-queue` | Autonomous serial run: implements and reviews each selected spec in its own worktree on top of the previous verified result, then hands the combined uncommitted changes to the target branch with a decision report |
| `/implement-swarm` | Autonomous parallel run: implements and reviews multiple independent specs concurrently, integrates their diffs for local review, and records resumable cleanup state |
| `/implement` | Runs `/dev` → `/review-spec-implementation` → `/review-changes` → `/review-performance` → `/review-security` in series, looping (up to 5 iterations) until everything checks out, and marks the spec done |

`/implement` is the recommended entry point for a feature - it's `/dev`, `/review-spec-implementation`, `/review-changes`, `/review-performance`, and `/review-security` wired together into one self-correcting loop. It never commits or pushes: `/commit-and-push` is always a separate, manual step after `/implement` hands off. Each of the five stays available individually for a narrower job (e.g. running `/review-security` alone after a manual edit).

Specs live in `.context/feature-specs/` as Markdown files with `status: todo / in-progress / done`. New UI specs persist a design brief at `.context/feature-specs/design/<spec-id>/brief.md`; reviewed visual references and relevant assets live alongside it and travel with the spec worktree. The brief alone does not count as a reviewed visual reference; the user may explicitly approve a prose-only design. After review, the handoff places the changes on the local `Target branch` for manual inspection. `/commit-and-push` commits and pushes that target branch only after the user directly invokes it. Run `/status` at any point to see framing, design handoff, worktree, verification, and local-branch state.

After the user has reviewed and committed/pushed the local target-branch changes, the normal spec worktree is already gone and the target checkout is ready for the next spec. No second invocation or post-merge pull is needed. A queue or swarm batch normally removes the worktrees of every spec it transferred before handoff; if cleanup is interrupted, `/status` reports the manifest and `resume <batch-id>` on the command that started it (`/implement-queue` or `/implement-swarm`) safely resumes it before more implementation starts.

### Autonomous spec batches

```mermaid
flowchart TD
  specs["Several planned specs<br/>todo"] --> mode{"Dependent specs?"}

  mode -- "yes: run in the given order" --> queue["/implement-queue"]
  queue --> q1["Spec 1<br/>worktree + subagent + reviews"]
  q1 --> q2["Spec 2, built on spec 1's verified result<br/>worktree + subagent + reviews"]
  q2 --> qn["Spec N ..."]
  qn --> final["Final checks on the combined result<br/>tests, typecheck, convention, performance and security reviews"]

  mode -- "no: independent" --> swarm["/implement-swarm"]
  swarm --> w1["Worker 1<br/>worktree + reviews"]
  swarm --> w2["Worker 2<br/>worktree + reviews"]
  swarm --> wn["Worker N ..."]
  w1 --> integrate["Integrate diffs in a temporary worktree<br/>resolve overlaps, aggregate checks"]
  w2 --> integrate
  wn --> integrate
  integrate --> final

  q1 -. "fails after 5 review rounds" .-> excluded["Spec set aside<br/>worktree kept, resume with /dev"]
  w1 -. "fails after 5 review rounds" .-> excluded

  final --> transfer["Transfer to local target branch<br/>uncommitted, unstaged"]
  transfer --> report["Final report<br/>decisions made, excluded specs, checks"]
  report --> review["User reviews with git diff HEAD"]
  review --> ship["/commit-and-push<br/>direct user invocation only"]
```

`/implement-queue` and `/implement-swarm` are for unattended runs. Start one, walk away, and read the final report. Neither ever commits or pushes: the result lands uncommitted on the local target branch, and only your later `/commit-and-push` commits it. During the run they never ask you anything; ambiguities are decided by the agent following the spec, the conventions, and accepted ADRs, and every decision is listed in the final report with its reason and rejected alternative. A spec that fails after five review rounds is set aside (its worktree and branch are kept, `status: in-progress`, resumable with `/dev <spec-id>`) while the others continue. The shared rules are in `.context/commands/autonomous-mode.md`.

`/implement-queue <spec-id-or-file> <spec-id-or-file> [...]` runs the specs one after another in the given order. Each gets its own worktree, subagent, and review loop, and starts from the verified result of the previous spec, so later specs can depend on earlier ones. The combined result is checked once more and transferred at the end.

#### Parallel batch (`/implement-swarm`)

`/implement-swarm <spec-id-or-file> <spec-id-or-file> [...]` starts one implementation worker per selected `todo` spec. You can drag and drop spec files such as `file:///D:/Projects/my-app/.context/feature-specs/006-dashboard-stats.md`; the shared resolver confirms each file belongs to this checkout and derives its exact spec ID. Each worker uses its own `.worktrees/<spec-id>/` and `feature/<spec-id>` branch. The primary agent waits for every worker, runs the spec, convention, performance, and security reviews, combines their uncommitted changes in an isolated integration worktree, resolves overlaps, runs aggregate checks, and transfers the complete result to the local target branch as uncommitted, unstaged changes.

No feature worker creates commits, so this is patch-based three-way integration rather than `git merge --no-commit`. The ignored `.worktrees/.parallel-batches/<batch-id>/manifest.json` records each phase and cleanup operation. If execution is interrupted, `/status` reports the batch and its remaining worktrees; resume with `/implement-swarm resume <batch-id>` (or `/implement-queue resume <batch-id>` for a queue). The command never deletes a worktree until the full transfer to the target checkout is verified. New specs and batches wait until an incomplete batch is recovered and the target-branch changes have been reviewed and committed by the user.

### Test-driven development

Every agent that writes code follows the red-green-refactor loop in `.context/coding-conventions/tdd.md`: one failing test, the minimum code to pass it, refactor, repeat. This is deliberately not "write all the tests first", which lets an AI anticipate and over-build; the short loop is what keeps its output minimal. It is mandatory for backend code, frontend logic (hooks, utilities, schemas, state), and bug fixes. UI components get component tests when they carry behavior, and Playwright e2e tests cover the user journeys named in the spec; config, generated files, pure markup/styling, and migrations are verified by running them.

- **Tools are chosen per stack.** `/architecture` fills a mandatory `## Testing` table in `.context/architecture.md` (backend unit and integration, frontend logic, components, e2e), and `/spec` is blocked until it is complete. Stack recipes under `.context/stacks/` provide defaults.
- **Acceptance criteria drive the cycles.** Each criterion becomes one or more test cases, worked from simplest to richest, and every criterion must end up covered by a test.
- **Evidence.** The implementing agent records a `## TDD journal` (criterion, test, red failure reason, minimal change) in the verification record. `/review-spec-implementation` checks that every criterion maps to a test and can run a neutralization check (break the logic, confirm its test goes red, restore); `/review-changes` checks that tests assert behavior rather than mirror the implementation.
- **Browser verification.** After UI work the agent checks the result in a real browser, using Claude in Chrome under Claude Code and Playwright elsewhere. That is inspection only; committed e2e tests use Playwright.

### Design tools and local coding agents

Use any design process that fits the project: a design workspace such as Figma or OpenDesign, another design application, or existing local references. `/spec` saves a self-contained `brief.md`; review it, create or inspect the design in your preferred tool, then place the reviewed visual references and relevant assets beside it under `.context/feature-specs/design/<spec-id>/`. For derived screens, the brief describes changes from the existing screen instead of repeating its design. The local coding agent reads the files synchronized into the feature worktree; it does not connect to or inspect the live design workspace. After verified handoff, the spec and design references are preserved in the local target checkout. A workspace URL is optional, and this file handoff does not require provider-specific MCP setup. Supplied HTML and other active content are inspected as source and never executed; use a screenshot or static export for visual review.

## Getting started

For a new project or an existing project that does not yet have `.context/`, run `/init-project` first. It inspects the existing codebase and initializes shared project context without choosing or bootstrapping a stack. Then run `/prd` followed by `/architecture`, apply any approved stack setup separately, and run `/design-system` if the project has a UI. `/architecture` alone is only the narrow documentation path when you want to record an existing project's architecture; it creates only `.context/architecture.md` and does not replace `/init-project` or unlock `/spec`.

The workflow does not require the GitHub CLI. Configure the project's `origin` remote and local target branch so the user-authorized `/commit-and-push` command can push after local review.

### Updating an already initialized project

Do not rerun `/init-project` when the shared project settings are already populated. Run `/update-workflow` instead, once per repository (a workspace folder holding several repositories is not a project: run it inside each one). It clones the starter named by `Starter source:` in `.context/project-settings.md`, or the git URL or local path you pass as its argument, and changes only what the starter owns:

| Class | Files | What the command does |
| --- | --- | --- |
| Workflow-owned | `.context/commands/`, `scripts/`, `stacks/`, `coding-conventions/` (except `security.md`), `ai-workflow-*.md`; `.claude/` and `.opencode/` commands, agents, and hooks; `.githooks/` | Adds, updates, or deletes them |
| Merge-only | `.claude/settings.json`, `.gitignore`, `.gitattributes`, `AGENTS.md`, `CLAUDE.md`, `.context/project-settings.md` | Adds what the starter has and the project lacks, never removes local content (a framework-generated block in `AGENTS.md` survives) |
| Project-owned | overview, architecture, tracker, specs, ADRs, memory entries, `security.md`, README, changelog, `infra/`, code, and any custom command of yours | Never touched, except the spec renames below |

**First update versus later ones.** A project copied from an older starter has no `Starter version:` stamp, and its files often predate the starter's history, so the command cannot know which differences are your customizations. It never guesses a merge base: each differing file becomes a conflict, decided by group with one confirmation. Workflow machinery (commands, agents, hooks, `global.md`, `tdd.md`) defaults to the starter's version; stack convention files and recipes default to yours. You can flip a group or choose per file, and because the working tree must be clean, anything replaced is recoverable from Git. The command then stamps `Starter version:`, so later updates do a real three-way merge against it and only ask about true conflicts. If the project has no `project-settings.md` yet, the command asks for the target branch (default: the current one) and creates it; fill in `Test command:` and `Typecheck command:` afterwards.

```mermaid
flowchart TD
  start["/update-workflow<br/>clean checkout on the target branch, no incomplete batch"] --> fetch["Clone the starter<br/>Starter source: or argument"]
  fetch --> classify{"Each workflow-owned file<br/>compared with the starter"}
  classify -- "same" --> skip["Nothing to do"]
  classify -- "unmodified older copy" --> overwrite["Overwrite with the latest version"]
  classify -- "differs" --> base{"Starter version: stamped?"}
  base -- "yes" --> merge{"Three-way merge"}
  merge -- "clean" --> overwrite
  merge -- "conflict" --> ask
  base -- "no: first update" --> ask["Defaults by group, you confirm<br/>machinery: starter, stack conventions: yours<br/>override per group or file"]
  classify -- "removed in the starter" --> remove["Delete if unmodified<br/>otherwise ask"]
  classify -- "only in your project" --> own["Left alone<br/>custom commands stay"]
  start --> specs["Legacy numeric specs<br/>no active worktree or branch"]
  specs --> rename["Rename to UTC IDs from the first-commit date<br/>specs, design folders, verification records, references"]
  overwrite --> plan["Plan shown, you confirm"]
  ask --> plan
  remove --> plan
  rename --> plan
  plan --> apply["Apply, check the .claude and .opencode mirrors<br/>stamp Starter version:"]
  apply --> framing["Report the framing state<br/>PRD, Testing section, design system still missing for /spec"]
  framing --> review["Uncommitted changes<br/>you review, then /commit-and-push"]
```

**Spec migration.** Legacy `NNN-slug` specs get a UTC ID from the date of their first commit, kept strictly increasing in numeric order so specs committed together keep their original order. The rename covers the spec file, its design folder, its verification record, and every reference in the Markdown files the update does not take from the starter, including application resources outside `.context/`. References inside accepted ADRs are retargeted too (only the reference text changes) and the plan lists those files. Specs with an active worktree or `feature/<spec-id>` branch keep their numeric ID until their handoff; run `/update-workflow` again afterwards. Mentions that cite only a spec number (for example "spec 006") are not rewritten, and old IDs remain in Git history.

**After the update.** An older project usually lacks the product framing that `/spec` now requires, so the report lists the framing commands to run next (`/prd`, `/architecture` for the `## Testing` section, `/design-system` for UI projects). Obsolete leftovers outside the workflow's reach, such as the old `security-review-ecc` skill folder, are yours to delete. The command also removes the retired `Merge mode` and `Ship confirmation` settings and renames a legacy `OpenDesign URL:` key to `Design workspace URL:`, preserving its value. Existing pull requests or remote feature branches are not changed automatically; resolve any old pipeline work separately before switching to this local-review workflow. The command never commits or pushes.

**Expected effort.** Roughly 10 to 25 minutes per repository for a project with dozens of specs, most of it spent reading the plan and confirming the defaults (an estimate from a dry run, not a measurement). A project that is already stamped and has no legacy specs takes a few minutes.

## Security review rule updates

`/review-security` keeps `.context/coding-conventions/security.md` as the project's authority and uses the [OWASP Secure Coding Markdown compilation](https://github.com/vchirrav-eng/owasp-secure-coding-md) for supplementary rule IDs. The shared updater downloads only `rules/*.md` into the Git ignored `.cache/security-rules/` directory. Agents run it from `.context/ai-workflow-entrypoint.md` when a session starts; it checks upstream at most once every seven days after a successful download, retries failed refreshes at the next session, and keeps the last valid snapshot if the network is unavailable. Review reports include the source commit SHA.

An existing project created from an older starter gets the updater script, the startup instruction in `.context/ai-workflow-entrypoint.md`, the `security-reviewer` agent, and the `.cache/security-rules/` ignore line from `/update-workflow`; its own `security.md` is preserved. Delete the old `security-review-ecc` skill copies yourself. The first session after the update downloads the rules.

On a new computer, clone the project and make sure Python 3 and Git are available. The first session needs network access to create the cache. Because the upstream repository currently declares no redistribution license, this starter does not commit a copy of its rules; a new clone without network access cannot complete the supplementary review until its first download succeeds.
