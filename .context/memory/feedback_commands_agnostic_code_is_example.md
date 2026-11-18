---
name: feedback_commands_agnostic_code_is_example
description: workflow commands stay database- and language-agnostic; embedded code (PHP, pg_dump) is an example, never the contract
metadata:
  type: feedback
---

A command in `.context/commands/` must not hardcode an engine or a language in its description, wording or steps. Where it embeds code (for example the Symfony/PHP files of `/setup-backup`), that code is labelled as an example, and the command states the contract to reproduce on another stack.

**Why:** the user noticed `/setup-backup` said PostgreSQL in the README and then pointed out the PHP code read as the requirement ("le code php doit être un exemple"). Fix it everywhere (command, wrappers, README, conventions), not only where it was spotted. See [[feedback_direct_starter_edits]].

**How to apply:** when touching a command, grep every mirror and doc for the hardcoded engine or language name, isolate the engine-specific part in one place, and add a short contract plus an "example" label next to any embedded code.
