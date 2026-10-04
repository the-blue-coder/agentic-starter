---
type: decision
status: accepted
date: 2026-10-04
tags: [workflow, spec, process]
supersedes: [[2026-09-27 - Require complete framing before feature specs]]
affects:
  - '[[spec-workflow]]'
---

# Fold the PRD into the project overview

## Context

The project overview and the PRD both carried the problem, the perimeter, and the success criteria, so the same facts lived in two files that drifted apart. The PRD was a separate file mainly because it was copied from another starter; the overview already had Overview, Scope, and Success Criteria sections.

## Decision

Keep `/prd` as the framing interview, but write its result into `.context/project-overview.md`: the problem in `## Overview`, the core perimeter in `### In Scope`, exclusions in `### Out of Scope`, then `## Success Criteria`, `## Constraints`, and `## Reference Product` when it applies. There is no `.context/framing/prd.md` any more. `/spec` stays blocked until shared initialization, this product framing, architecture, and (for UI projects) the design system are complete; `/spec` and `/status` check those overview sections instead of a PRD file. `/update-workflow` folds a legacy PRD into the overview and deletes `framing/`.

## Why not something else

- **Keep the PRD file and trim the overview**: the duplication moves around but remains, and a short overview loses its role as the session's orientation.
- **Delete `/prd`**: a new project would lose the step where the perimeter is decided before the first spec.
- **Make the PRD optional for mature projects**: two framing shapes to maintain and explain.

## Consequences

- Positive: one source of product framing, no duplicated success criteria, one fewer file and folder.
- Negative / risk: the overview grows, and an existing project must run the migration; a tool that expected `framing/prd.md` no longer finds it.
- Generates: `/prd`, `/init-project`, `/spec`, `/status`, `/architecture`, `/update-workflow`, the entrypoint, and the README describe the same single-source framing.
