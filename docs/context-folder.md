# What lives in `.context/`

| Path | Role |
| --- | --- |
| `project-overview.md`, `architecture.md`, `infra.md`, `ui-context.md` | The project's framing: product (problem, perimeter, success criteria, constraints), architecture, infrastructure, design tokens |
| `project-settings.md` | `Target branch:`, `Design workspace URL:`, `Test command:`, `Typecheck command:`, `SEO:` (`yes`, `no`, `hybrid`), `SEO public scope:`, `Starter source:`, `Starter version:` |
| `progress-tracker.md`, `feature-specs/` | Work in progress, specs (each ends with its test map) |
| `coding-conventions/` | `global.md`, `security.md`, `tdd.md`, `html.md`, `seo.md`, `performance/`, and one file per supported stack |
| `stacks/` | Stack recipes: `symfony-nextjs-contabo`, `symfony-twig-stimulus` |
| `adr/`, `memory/` | Decisions with rejected alternatives, and corrections or validated approaches, both loaded automatically, with no command |
| `commands/`, `security-rules/`, `ai-workflow-*.md` | Canonical commands, the committed OWASP rules snapshot, the entrypoint and workflow rules |

**Supported stacks:** Symfony API with API Platform, Symfony with Twig and Stimulus, Next.js, and Gatsby, with TypeScript, JavaScript, React, PHP, HTML, Tailwind, and UI conventions. PHP runs on FrankenPHP, static analysis is PHPStan (level 8, locally and in the GitHub workflow), and JavaScript dependencies are managed with pnpm. Each stack file is modeled on a real reference project.

**Quality rules in force:** a red-green-refactor TDD loop per acceptance criterion for business logic and bug fixes, with test tools chosen per stack at `/architecture` time; the simplicity ladder from the Absolute Directive; per-stack performance rules; HTML and SEO rules for SEO-friendly projects; and OWASP-backed security review.
