# Every command

| Group | Command | What it does |
| --- | --- | --- |
| Framing | `/init-project` | Sets up shared project context and workflow settings, and settles whether the project is SEO-friendly (`yes`, `no`, or `hybrid`), without choosing a stack |
| | `/prd` | Frames the product once: problem, perimeter, out-of-scope, success criteria |
| | `/architecture` | Chooses and documents the architecture, including the test tools (`## Testing`) and the hosting inputs (domains, DNS, server access), prunes unused stack conventions, or documents an existing codebase |
| | `/setup-stack` | Applies the approved stack-specific setup: scaffold, infra, environment and verification, adapted from the matching stack recipe and the architecture decision; confirms every outward-facing action and never commits |
| | `/setup-backup` | Sets up the database backup to S3, whatever the engine (PostgreSQL and MySQL/MariaDB out of the box; webhook, dump and upload services, retention, failure email, test) for the stack's architecture mode, then lists the scheduler workflow to duplicate; strongly recommended when the project has a database (`/spec` and `/status` remind you, it never blocks); run after the first deploy |
| | `/design-system` | UI projects only: locks design tokens, the brand identity (logo, favicon, share image) and a contrast audit into `.context/ui-context.md` |
| Features | `/spec` | Plans a feature after the framing gate: research, questions, design brief for UI specs, spec file with acceptance criteria and its `ui:` and `seo:` flags |
| | `/dev` | Implements one spec in its own worktree and branch, following the TDD loop, and writes the test map into the spec |
| | `/implement` | Recommended entry point: `/dev` plus every review in a self-correcting loop (max 5 iterations), then the handoff |
| | `/implement-queue` | Autonomous: several specs in series, each on top of the previous verified result, ending with a decision report |
| | `/implement-swarm` | Autonomous: several independent specs in parallel, integrated and reviewed together, ending with a decision report |
| Reviews | `/review-spec-implementation` | Verifies every acceptance criterion, data-model field, and API contract against real code; the only command that marks a spec `done` |
| | `/review-changes` | Checks changed files against the coding conventions and TDD rules, runs static analysis, and fixes violations |
| | `/review-performance` | Checks the diff for N+1 queries, unbounded lists, request waterfalls, leaks, heavy imports; fixes real costs only |
| | `/review-seo` | Flagged work only (`SEO:` `yes` or `hybrid`, and `seo: true` on the spec; public scope only), otherwise neither launched nor mentioned: checks metadata, canonical and robots, crawlable markup and links, status codes, structured data; fixes real defects |
| | `/review-security` | Checks the diff against `security.md` and relevant OWASP rules; always last, and owns the final handoff |
| Project | `/status` | Read-only framing state and per-spec pipeline stage, with next-command suggestions |
| | `/update-workflow` | Updates an existing project's workflow files to the latest starter, settles the SEO setting, and migrates legacy specs |
| Ship | `/commit-and-push` | Commits and pushes the reviewed changes of the current branch; only runs when you invoke it |
| Utilities | `/add-new-color` | Adds a design token (Tailwind CSS-variable systems) |
| | `/rebuild-tailwind` | Rebuilds the Tailwind CSS output with the stack's build command |
| | `/just-respond` | Answers in text only: no edits, no commands |
| Infra runbooks | `/setup-rolling-deploy`, `/teardown-rolling-deploy` | Rolling zero-downtime deploy, currently for the `symfony-nextjs-contabo` recipe |
