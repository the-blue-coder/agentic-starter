# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Forked the agentic tooling layer (`.claude/`, `.context/`, `.opencode/`, `infra/`, root docs) out of `symfony-nextjs-starter` into a standalone, stack-agnostic starter. `INIT.md`, `architecture.md`, and `infra.md` are now stack-neutral orchestrators/templates; the previous Symfony+Next.js+Contabo content was preserved as the first entry under `.context/stacks/` (`symfony-nextjs-contabo.md`) rather than deleted.
