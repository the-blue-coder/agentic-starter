---
description: "Once per UI project - confirm design tokens and audit color-pair contrast (light/dark), so per-spec design passes never re-measure it"
---

You are a UI engineer documenting the project's actual design system and auditing contrast once, so future feature work can reuse it. This runs once per UI project, after `/architecture` and after the selected UI stack and its tokens exist.

---

## Phase 1 - Check there is a UI layer

Read `.context/architecture.md`. If its `Frontend` row is blank or unresolved, stop and ask the user to complete `/architecture` first. If the row explicitly says `None` or `-`, tell the user this command doesn't apply and stop. Don't infer a backend-only project from missing documentation or invent UI concerns for one that has none.

---

## Phase 2 - Load current context (silent)

Read:
- `.context/ui-context.md`
- Relevant `.context/coding-conventions/*.md` files for the stack (e.g. `tailwind.md`, `ui.md`, `react.md`) if present.

Then, using Read/Glob/Grep, find the actual design tokens in the codebase: theme/CSS variable definitions (e.g. `globals.css`, `tailwind.config`, a design-tokens file), and how they're used in real components.

Determine whether the project supports light mode, dark mode, or both - check `.context/ui-context.md`'s Theme section and how theming is actually implemented in code.

---

## Phase 3 - Confirm and enrich `.context/ui-context.md`

If the codebase contains no actual design tokens or established UI system and the user has provided no visual direction or source references, stop and ask for those inputs; do not create a generic visual identity. If the user provides visual direction but no implementation tokens exist yet, document the direction and mark missing token values as unresolved. Present any suggested token values for explicit user approval before treating them as project tokens.

Compare what's documented against the code. Fill `[bracketed]` placeholders only from actual code or user-approved direction. Update sections (Theme, Typography, Border Radius, Component Library, Layout Patterns, Icons) where the code has real answers the doc is missing or has wrong. Don't invent tokens that don't exist in the code or silently turn proposals into decisions.

---

## Phase 4 - Contrast audit

For every text/surface color pair the token set can actually produce (body text on background, muted text on surface, button text on button background, etc.), calculate the WCAG contrast ratio from exact color values. If a token cannot be resolved to an exact color, mark the ratio `unverified`; do not estimate a value or claim it passes.

If the project supports both light and dark mode, audit both. If only one mode, audit that one.

Flag any pair under:
- **4.5:1** for body/normal text
- **3:1** for large text (≥18pt/24px, or ≥14pt/19px bold) and UI components (borders, icon-only controls)

Write one `## Contrast Audit` section in `.context/ui-context.md`; append it if absent and replace the existing section if present so reruns never create duplicates:

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

Omit the mode table that doesn't apply. For every failure, identify where the pair is used and ask the user to approve a system-level token correction or an explicit, scoped exception. Wait for that decision. If a correction is approved, update the source token and its documentation, then recalculate the affected pairs. Record an exception only after the user approves it, with the exact scope and approval date in the row's status or note (for example, `APPROVED EXCEPTION - icon-only control; user approved 2026-09-27`). Do not defer failures to individual feature specs or silently accept them as large-text/UI-only usage. Mark unresolved failures or unknown color values clearly; the contrast audit is complete only when each pair passes or has an explicit user-approved exception.

---

## Phase 5 - Report

Tell the user the file was updated, list any failing pairs found, and note that future `/spec` design passes can reference these validated tokens instead of re-measuring contrast.
If failures or unknown values remain because a user decision is pending, say the audit is incomplete and `/spec` remains blocked; do not report the token set as validated.
