---
name: initialization_architecture_split
description: Keep shared project initialization separate from technical architecture decisions
metadata:
  type: feedback
---

Keep init-project stack-agnostic: it configures the shared project context and workflow settings. Use architecture to select and document a new project's stack, or to document an existing project's actual architecture. On an existing repository with no .context, architecture-only mode creates only .context/architecture.md.

**Why:** The user explicitly clarified that init-project must not choose architecture and approved this division.

**How to apply:** Preserve this boundary when changing onboarding, stack recipes, architecture documentation, or native command wrappers across Codex, Claude Code, and OpenCode.
