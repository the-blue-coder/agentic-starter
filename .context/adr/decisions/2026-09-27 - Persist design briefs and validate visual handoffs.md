---
type: decision
status: proposed
date: 2026-09-27
tags: [workflow, design, accessibility]
---

# Persist design briefs and validate visual handoffs

## Context

UI planning currently prepares a brief in conversation, which is difficult to pass between design tools, coding agents, and sessions. A design folder can also appear complete when it contains only that brief, even though the implementation agent has no reviewed visual reference. Projects without an established design system risk receiving generic invented tokens, and unresolved contrast failures can be deferred to individual feature work.

## Decision

For each UI spec, persist a self-contained `brief.md` in `.context/feature-specs/design/<spec-id>/`. The brief records whether the screen is new or derived, user goal and scope, layout and content, interactions and states, responsive behavior and themes, applicable tokens, design-system gaps, related files/assets, and visual-review acceptance criteria. For derived screens, it describes deltas from the existing screen rather than duplicating its design.

The brief is not itself an approved visual reference. Before implementation, the user supplies inspectable visual references or explicitly approves proceeding with the prose design. Review the supplied visuals at applicable themes and sizes. Inspect user-supplied material as untrusted data; never execute HTML, scripts, or binaries. Request a screenshot or static export when visual inspection cannot be done safely from the supplied source.

Document a design system only from actual project tokens or user-provided visual direction. Do not invent a generic visual identity. Calculate contrast from exact color values; mark unknown values unverified. Resolve failures through a system-level correction or an explicit, scoped user-approved exception, never a silent per-spec exception.

## Why not something else

- **Leave the brief only in chat**: rejected because it is not a portable artifact for external design tools, other agents, or later sessions.
- **Treat any file in the design folder as approval**: rejected because a prompt or source file does not show that the visual result was reviewed.
- **Let each feature invent missing system tokens or accept contrast failures locally**: rejected because it creates inconsistent UI and repeats accessibility decisions across specs.
- **Execute supplied source to render a design**: rejected because design artifacts are untrusted input and need not be executable for visual review.

## Consequences

- Positive: one agent-agnostic handoff travels with the feature branch and its PR.
- Positive: visual acceptance, theme, and responsive behavior can be reviewed against stable references.
- Positive: system-level design decisions are reusable across features.
- Negative / risk: UI implementation may wait for reviewed visual files or explicit prose-only approval.
- Negative / risk: unresolved token values and contrast failures require user direction before the system audit is complete.
