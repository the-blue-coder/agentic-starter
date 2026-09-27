# Progress Tracker

Update this file after every meaningful implementation change.

## Current Phase

- Complete

## Current Goal

- Maintain a consistent, agent-agnostic feature workflow in the starter.

## Completed

- Standardized project framing, UI design handoff, and local-target review after isolated per-spec implementation across Codex, Claude Code, and OpenCode.
- Clarified Symfony domain behavior, repository, and application-service responsibilities.
- Generalized the per-spec design handoff across design tools and local references.
- Separated generic project initialization from architecture selection and documentation.
- Adopted UTC timestamped IDs for new specs while keeping legacy IDs usable and preserving one temporary worktree and branch per spec, with no pull requests.
- Persisted per-spec UI design briefs and required reviewed visual references or explicit prose-only approval.
- Tightened design-system evidence and contrast rules, and made reference-product PRD framing conditional.

## In Progress

- None yet.

## Next Up

- None yet.

## Open Questions

- None.

## Architecture Decisions

- Structural decisions (architecture, process, tooling, convention) are recorded automatically in `.context/adr/decisions/` - see `.context/adr/README.md`. This section only needs a one-line pointer to the relevant decision file, not the full rationale.
- [Review verified specs on the local target branch](.context/adr/decisions/2026-09-27%20-%20Review%20verified%20specs%20on%20the%20local%20target%20branch.md) (accepted; supersedes the proposed timestamped-spec workflow decision).
- [Conditional reference-product framing](.context/adr/decisions/2026-09-27%20-%20Make%20reference%20product%20framing%20conditional.md) (proposed).
- [Keep domain behavior with its owning objects](.context/adr/decisions/2026-09-27%20-%20Keep%20domain%20behavior%20with%20its%20owning%20objects.md).
- [Separate generic project initialization from architecture decisions](.context/adr/decisions/2026-09-27%20-%20Separate%20generic%20project%20initialization%20from%20architecture%20decisions.md).
- [Require complete framing before feature specs](.context/adr/decisions/2026-09-27%20-%20Require%20complete%20framing%20before%20feature%20specs.md) (proposed).

## Session Notes

- UI design tools (for example, OpenDesign) are separate from the local coding agent, which may be Codex, Claude Code, OpenCode, or another tool.
