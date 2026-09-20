---
description: "Once per UI project - confirm design tokens and audit color-pair contrast (light/dark), so per-spec design passes never re-measure it"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

You are a UI engineer locking down design tokens and contrast for a project, once, so future feature work never has to re-derive it. This runs once per project (after `/architect`), UI projects only.

---

## Phase 0 - Check there is a UI layer

Read `.context/architecture.md`. If the project has no frontend/UI layer (pure API/backend), tell the user this command doesn't apply here and stop. Don't invent UI concerns for a project that doesn't have any.

---

## Phase 1 - Load current context (silent)

Read:
- `.context/ui-context.md`
- Relevant `.context/coding-conventions/*.md` files for the stack (e.g. `tailwind.md`, `ui.md`, `react.md`) if present.

Then, using Read/Glob/Grep, find the actual design tokens in the codebase: theme/CSS variable definitions (e.g. `globals.css`, `tailwind.config`, a design-tokens file), and how they're used in real components.

Determine whether the project supports light mode, dark mode, or both - check `.context/ui-context.md`'s Theme section and how theming is actually implemented in code.

---

## Phase 2 - Confirm and enrich `.context/ui-context.md`

Compare what's documented against what's in the code. Fill any `[bracketed]` placeholders from what you found. Update sections (Theme, Typography, Border Radius, Component Library, Layout Patterns, Icons) where the code has real answers the doc is missing or has wrong. Don't invent tokens that don't exist in the code.

---

## Phase 3 - Contrast audit

For every text/surface color pair the token set can actually produce (body text on background, muted text on surface, button text on button background, etc.), compute or estimate the WCAG contrast ratio.

If the project supports both light and dark mode, audit both. If only one mode, audit that one.

Flag any pair under:
- **4.5:1** for body/normal text
- **3:1** for large text (≥18pt/24px, or ≥14pt/19px bold) and UI components (borders, icon-only controls)

Append a new section to `.context/ui-context.md`:

```markdown
## Contrast Audit

### Light mode

| Text | Surface | Ratio | Status |
| --- | --- | --- | --- |
| `--text-primary` | `--bg-base` | 12.6:1 | OK |
| `--text-muted` | `--bg-surface` | 3.8:1 | FAIL (body text needs 4.5:1) |

### Dark mode

| Text | Surface | Ratio | Status |
| --- | --- | --- | --- |
| ... | ... | ... | ... |
```

Omit the mode table that doesn't apply. If a pair fails, note in the row (or just below the table) what it's used for, so the user can decide whether to adjust the token or accept it as large-text/UI-only usage.

---

## Phase 4 - Report

Tell the user the file was updated, list any failing pairs found, and note that future `/spec` design passes can reference these validated tokens instead of re-measuring contrast.
