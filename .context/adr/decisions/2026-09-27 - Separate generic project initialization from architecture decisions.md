---
type: decision
status: accepted
date: 2026-09-27
tags: [workflow, architecture, tooling]
affects:
  - '[[init-project]]'
  - '[[architecture-workflow]]'
  - '[[stack-recipes]]'
---

# Separate generic project initialization from architecture decisions

## Context

The starter's init-project workflow previously selected and executed a stack recipe, including application bootstrap and infrastructure work. That mixed shared agent-workflow setup with product-specific architecture choices, before product framing was complete. The old architect command only reconciled a prefilled architecture document with the codebase, so there was no clear command responsible for choosing a new project's stack.

## Decision

Keep init-project stack-agnostic and limited to shared project context/settings; make architecture choose and document a new project's technical architecture or document the actual architecture of an existing project, with stack-specific setup performed separately after approval.

## Why not something else

- **Keep stack selection inside init-project:** rejected because it forces technical decisions before the product requirements have been framed and makes initialization opinionated about application stacks.
- **Have architecture automatically execute the selected recipe:** rejected because recording an architecture decision and making application, infrastructure, or deployment changes are separate actions that need a reviewable handoff.
- **Require full starter initialization before documenting an existing repository:** rejected because an existing-project architecture audit should be usable on its own; when .context/ is absent, that mode creates only .context/architecture.md.

## Consequences

- Positive: shared project setup and technical architecture have distinct, predictable responsibilities.
- Positive: architecture can be documented for an existing repository without migrating its workflow or changing application files.
- Negative / risk: fresh projects need a separate, explicit step to apply stack-specific scaffolding after architecture is approved.
- Generates: the old INIT.md guide is retired; its shared setup questions and settings now live in the canonical init-project command, while stack recipes remain available as references and setup guides.
