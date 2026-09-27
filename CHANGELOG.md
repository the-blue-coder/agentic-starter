# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Block feature specification until shared initialization, product framing, architecture, and the UI design system when applicable are complete.
- Separate generic shared project initialization from architecture decisions; rename the architect command to architecture and remove the standalone INIT.md guide.
- Make the per-spec UI design handoff provider-agnostic, with any design tool or local references supported.
- Clarify Symfony domain entity, repository, and application-service responsibilities.
- Configure initialization and feature workflows for one spec per branch and PR, with an OpenDesign export handoff that works across local coding agents.
- Keep the starter stack-agnostic; retain the previous Symfony + Next.js + Contabo setup only as a reference recipe under `.context/stacks/`.
