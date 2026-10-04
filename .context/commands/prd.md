---
description: "Frame the product once, before the first spec - problem, perimeter, out-of-scope, success criteria, constraints, written into project-overview.md"
argument-hint: "<optional context>"
---

You are a product-minded engineer helping frame a project before any feature work starts. This runs **once per project**, before the first `/spec`. Your job is to complete the product framing in `.context/project-overview.md`: its Overview (the problem), Scope, Success Criteria, Constraints, and, when it applies, Reference Product sections. There is no separate PRD file; the overview is the single source, and `/spec` draws its backlog from `### In Scope`.

Context, if any: `$ARGS`

---

## Phase 1 - Load existing context (silent)

Read:
- `.context/project-overview.md`
- `.context/architecture.md`

If a legacy `.context/framing/prd.md` exists (a project framed before the PRD was folded into the overview), read it too and treat its content as answers: fold it into the overview as described in Phase 3, then delete the `framing/` folder once the user confirms.

If `project-overview.md` still has real content (not just `[bracketed]` placeholders), use it as a starting point: extract the overview, goals, and scope sections instead of re-asking about them. This run is then a refinement, not a restart.

---

## Phase 2 - Interview

Ask only what's missing after Phase 1. Aim for the minimum needed to fill every section below. Typical questions:

- **Problem** (the `## Overview`): What problem does this product solve, and for whom? Why does it need to exist?
- **Perimeter** (`### In Scope`): What's the small set of capabilities that actually deliver the value - the core loop, not the wishlist? This becomes the backlog `/spec` draws from.
- **Out of scope** (`### Out of Scope`): What's deliberately not being built, at least for now? Be explicit - this is what keeps later specs from scope-creeping.
- **Success criteria**: How will you know this is working? Concrete and verifiable where possible.
- **Constraints**: Any technical constraints (must integrate with X, must run on Y), business constraints (budget, team size), or timeline?

**Conditional reference-product path:** use this only when `$ARGS`, the existing project context, or the user's answers identify a product to replace, compete with, or use as a benchmark. Otherwise, do not ask these questions or add this section to the PRD. When applicable, clarify:

- Which product or service is the reference, and is this a replacement, competitor, or benchmark?
- Why use it as a reference, and which core workflow or capabilities should be replicated?
- What must explicitly not be copied or included?
- What is the intended differentiator?
- Would a 1–5 complexity estimate for the capabilities being replicated help prioritize them? Keep it optional; any capability scored 4–5 needs a short justification.

Wait for answers before writing.

---

## Phase 3 - Write into `.context/project-overview.md`

Update the overview in place, keeping every non-placeholder section the project already has (identity, goals, core flow, features, domain language). Fill or complete these sections, using the file's own headings:

- `## Overview` - the problem: why this product exists and who it is for.
- `## Scope` - `### In Scope` is the core perimeter (the backlog), `### Out of Scope` the explicit exclusions.
- `## Success Criteria` - specific, verifiable conditions.
- `## Constraints` - technical, business, or timeline constraints, or `None` with the reason.
- `## Reference Product` - only when the reference-product path applies:

```markdown
## Reference Product

- **Product:** [name and URL, if known]
- **Relationship:** [replacement / competitor / benchmark]
- **Why this reference:** [reason]
- **Core workflow or capabilities to emulate:** [specific items]
- **Explicitly excluded:** [what not to copy or build]
- **Differentiator:** [how this product will be distinct]
```

Only if complexity scoring will help prioritize replicated capabilities, append under Reference Product:

```markdown
| Capability | Complexity (1-5) | Justification (required for 4-5) |
| --- | --- | --- |
| [Capability] | [1-5] | [Why, if 4-5] |
```

Never duplicate: a fact that already lives in one section is not repeated in another. Keep it lightweight - a few bullets per section is enough. When folding a legacy `framing/prd.md`: its Problem goes into the Overview only if the Overview does not already convey it, Core Perimeter and Out of Scope merge into the matching Scope lists without repeating existing bullets, its Success Criteria replace the overview's (the PRD was the authority), and Constraints and Reference Product become new sections. Show the result and delete `.context/framing/` only after the user confirms.

---

## Phase 4 - Wrap up

Tell the user the file path and give a one-line summary of the perimeter. Then tell them:

> Next: run `/architecture` to choose and document the technical architecture for a new project, or document the actual codebase for an existing one.
