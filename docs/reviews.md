# The review pipeline

| Order | Review | Subagent | Looks at | Fixes in place |
| --- | --- | --- | --- | --- |
| 1 | `/review-spec-implementation` | `spec-verifier` | Acceptance criteria, data model, API contract | Flags gaps, never invents behavior |
| 2 | `/review-changes` | `convention-reviewer` | Coding conventions, placement rules, lint, tests against `tdd.md` | Yes |
| 3 | `/review-performance` | `performance-reviewer` | Cost the diff introduces, per stack (`coding-conventions/performance/`) | Yes, with concrete cost and bounded fix only |
| 4 | `/review-seo` | `seo-reviewer` | Public pages against `seo.md` and `html.md`, only for flagged work (`SEO:` `yes` or `hybrid`, spec `seo: true`) | Yes, never invents titles, descriptions, or copy |
| 5 | `/review-security` | `security-reviewer` | Project `security.md` plus OWASP Secure Coding rules (refreshed at most weekly) | Yes |

On the quick path the order is changes, performance, SEO, then security last. `/review-performance` reports "Not applicable" by itself unless the diff has a query or network call, a loop, UI rendering, a dependency change, or file handling. `/review-seo` is flagged work: with `SEO: no`, or a spec whose `seo:` flag is `false` (set by `/spec`, like `ui:`, and `true` for `hybrid` only when the spec touches the public scope), it is neither launched nor mentioned in any report, handoff message, or status suggestion. When launched and nothing in the public scope changed, it returns "Not applicable" silently. Other subagents: `implementer` (builds from precise instructions) and `codebase-researcher` (grounds a spec in analog features and best practices).
