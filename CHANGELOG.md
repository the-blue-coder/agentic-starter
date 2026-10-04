# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- Remove Codex support (`.codex/` and `$`-prefixed skill syntax); commands are mirrored to Claude Code and OpenCode only.
- Replace per-spec pull requests with verified local target-branch handoffs for user review before the explicitly authorized commit and push.
- Add parallel spec implementation with an integrated local handoff and resumable worktree cleanup.
- Allow `/dev`, `/implement`, and `/parallel-implement` to resolve dropped local spec files consistently across coding agents.

- Block feature specification until shared initialization, product framing, architecture, and the UI design system when applicable are complete.
- Separate generic shared project initialization from architecture decisions; rename the architect command to architecture and remove the standalone INIT.md guide.
- Make the per-spec UI design handoff provider-agnostic, with any design tool or local references supported.
- Use UTC timestamped IDs for new specs while keeping legacy numeric specs readable across worktrees, branches, verification records, and status reports.
- Persist UI design briefs with each spec, require reviewed visual references or explicit prose-only approval, and keep supplied active content unexecuted.
- Require evidence or user-provided direction before documenting a design system, use exact WCAG contrast values, and resolve failures at the system level or through explicit user-approved exceptions.
- Add conditional reference-product framing to the PRD for replacement, competitor, and benchmark projects.
- Clarify Symfony domain entity, repository, and application-service responsibilities.
- Keep the starter stack-agnostic; retain the previous Symfony + Next.js + Contabo setup only as a reference recipe under `.context/stacks/`.
