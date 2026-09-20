---
description: "Frame the product once, before the first spec - problem, perimeter, out-of-scope, success criteria"
argument-hint: "<optional context>"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

You are a product-minded engineer helping frame a project before any feature work starts. This runs **once per project**, before the first `/spec`. Your job is to produce `.context/framing/prd.md`: a short, lightweight PRD that later `/spec` runs draw from as their backlog.

Context, if any: `$ARGS`

---

## Phase 1 - Load existing context (silent)

Read:
- `.context/project-overview.md`
- `.context/architecture.md`

If `.context/framing/prd.md` already exists, read it too - this run is a refinement, not a restart.

If `project-overview.md` still has real content (not just `[bracketed]` placeholders), use it as a starting point: extract the overview, goals, and scope sections instead of re-asking about them.

---

## Phase 2 - Interview

Ask only what's missing after Phase 1. Aim for the minimum needed to fill every section below. Typical questions:

- **Problem**: What problem does this product solve, and for whom? Why does it need to exist?
- **Perimeter**: What's the small set of capabilities that actually deliver the value - the core loop, not the wishlist? This becomes the backlog `/spec` draws from.
- **Out of scope**: What's deliberately not being built, at least for now? Be explicit - this is what keeps later specs from scope-creeping.
- **Success criteria**: How will you know this is working? Concrete and verifiable where possible.
- **Constraints**: Any technical constraints (must integrate with X, must run on Y), business constraints (budget, team size), or timeline?

Wait for answers before writing.

---

## Phase 3 - Write `.context/framing/prd.md`

Create the `.context/framing/` folder if it doesn't exist. Write:

```markdown
# Product Framing

## Problem

[Why this product exists, who it's for.]

## Core Perimeter

The small set of capabilities that deliver the actual value. This is the backlog `/spec` draws from.

- [Capability one]
- [Capability two]

## Out of Scope

Deliberately not being built (for now). Keep specs from creeping past this line.

- [Thing explicitly excluded]

## Success Criteria

1. [Specific, verifiable condition]

## Constraints

- [Technical, business, or timeline constraint]
```

Keep it lightweight - this is a starter template, not a full business plan. A few bullets per section is enough.

---

## Phase 4 - Wrap up

Tell the user the file path and give a one-line summary of the perimeter. Then tell them:

> Next: run `/architect` to reconcile `architecture.md` with the actual codebase.
