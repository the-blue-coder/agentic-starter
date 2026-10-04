---
type: decision
status: accepted
date: 2026-09-27
tags: [workflow, product]
---

# Make reference product framing conditional

## Context

Some projects replace an existing product, compete with a named service, or intentionally use a reference product to shape their core workflow. The lightweight PRD does not currently capture what should be emulated, excluded, or differentiated. Asking these questions for every project would add noise where no reference product exists.

## Decision

The PRD asks about a reference product only when project context indicates a replacement, competitor, or benchmark. When applicable, record the target product, the relationship and reason for using it, workflows or capabilities to emulate, what to exclude, and the product's differentiator. Complexity scoring from 1–5 is optional and applies only when it helps prioritize replicated capabilities; a score of 4–5 requires a brief justification.

## Why not something else

- **Ask every project to name a competitor**: rejected because many projects have no useful reference and the question would add boilerplate.
- **Copy a reference product without explicit exclusions or differentiation**: rejected because it encourages unbounded scope and an undifferentiated clone.
- **Require complexity scores for every capability**: rejected because scoring is only useful for some product decisions.

## Consequences

- Positive: relevant product comparisons become actionable without turning the PRD into a copy checklist.
- Positive: normal project framing stays lightweight.
- Negative / risk: the PRD author must recognize when a reference-product path applies and capture the user's reason and boundaries.
