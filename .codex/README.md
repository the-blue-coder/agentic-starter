# Codex project configuration

Codex-specific agent definitions live in `.codex/agents/` as TOML files. Reusable workflows live in `.codex/skills/` as Agent Skills; each delegates to its single source in `.context/commands/`.

When adding or changing a command, update `.context/commands/` first and keep its Codex skill in `.codex/skills/` in sync.
