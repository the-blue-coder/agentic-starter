---
description: "Analyze the actual codebase once (or re-check for drift later) and reconcile architecture.md / conventions with reality"
---

You are a senior engineer reconciling documented architecture with the actual codebase. This command runs once at project start (after `/prd`), and can be re-run any time later to catch drift as the codebase evolves.

---

## Phase 1 - Load current docs (silent)

Read:
- `.context/architecture.md`
- `.context/coding-conventions/` (list the files, read each one)
- `.context/framing/prd.md` if it exists, for context on what's being built

---

## Phase 2 - Analyze the actual codebase (silent)

Using Read/Glob/Grep, inspect what's actually there:
- Real top-level folder structure.
- Real stack: languages, frameworks, package manifests (`package.json`, `composer.json`, etc.) - don't trust the recipe, read the lockfiles/manifests.
- Real patterns: how entities/services/routes/components are actually organized, naming conventions in use.
- Real invariants: things consistently true across the code (e.g. all routes defined server-side, all API calls go through one client, ID format actually used).
- Real system boundaries: what each layer actually owns.
- Real auth/access model as implemented, not just as described.

Keep this proportionate - skim representative files per area, don't read the entire repo file-by-file.

---

## Phase 3 - Reconcile

Two cases:

**Case A - `.context/architecture.md` still has `[bracketed]` placeholders** (project was never run through `/init-project`, e.g. an existing codebase wired in by hand):
Fill every placeholder from what you found in the codebase. Only ask the user for things you genuinely can't infer from code - business-level facts (why a boundary exists, product intent), not structural ones (folder layout, stack, patterns - infer those yourself).

**Case B - `.context/architecture.md` is already filled in:**
Compare what it claims against what you found. Update `.context/architecture.md` itself where the actual code has evolved in ways that are just... how the project grew (new folders, new patterns that supersede old ones, stack additions) - this file is meant to track reality.

For `.context/coding-conventions/*.md`: these are the starter's own opinionated rules, not to be casually overwritten. **Do not edit them.** Instead, report any drift you find - places where the actual code contradicts a stated convention - to the user, and let them decide whether the code or the convention should change.

---

## Phase 4 - Report

Summarize for the user:
- What was confirmed as accurate.
- What was updated in `architecture.md` and why.
- Any drift flagged against `coding-conventions/*.md` (convention says X, code does Y, in file(s) Z) - and ask whether to fix the code or update the convention.

Then check `.context/architecture.md` for whether this project has a frontend/UI layer:
- If yes, tell the user: "Next: run `/design-system` to lock design tokens and audit contrast."
- If the project is pure API/backend with no UI layer, skip that suggestion.
