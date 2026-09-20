# AI Workflow Rules

> Context loading order and file index: `.context/ai-workflow-entrypoint.md`.

## Approach

Build incrementally against the specs defined in `.context/`. Never infer or invent behavior not described there. When in doubt, resolve ambiguity in the relevant context file before writing code.

---

## Scoping Rules

- Work on one feature unit at a time.
- Small, verifiable increments over large speculative changes.
- Never combine unrelated system boundaries in a single step.

**Split a step if it touches:**

- UI changes AND background/async logic simultaneously
- Multiple unrelated API routes
- Behavior not defined in the context files

If a change cannot be verified end-to-end quickly, the scope is too broad - split it.

---

## Testing Approach

> ## ⛔ TDD IS MANDATORY FOR CRITICAL BUSINESS LOGIC AND BUG FIXES - NO EXCEPTIONS
>
> Write the **failing test FIRST**, before a single line of implementation or fix code. This is non-negotiable for services, domain logic, and regressions - skipping the red step is a process violation, not a shortcut.

- Everything else (simple CRUD, UI components, config) keeps the existing test-after convention - see the `coding-conventions/*.md` files matching this project's stack (per `.context/architecture.md`).

---

## Handling Missing Requirements

- Do not invent product behavior.
- If ambiguous, resolve it in the relevant `.context/` file first.
- If missing, add it as an open question in `progress-tracker.md` before continuing.

---

## Protected Files

Do not modify unless explicitly instructed. The exact paths depend on the chosen stack recipe (see `.context/architecture.md`) - typically:

- UI primitive/design-system components (edit only to match the design system)
- The auth guard / middleware
- The shared API client / fetch wrapper

---

## Keeping Docs in Sync

Update the relevant `.context/` file whenever implementation changes:

- System architecture, structure, or invariants → `architecture.md`
- Infrastructure, env vars, deploy config → `infra.md`
- Feature scope or status → `progress-tracker.md`
- Design tokens, layout, UI decisions → `ui-context.md`
- A structural decision with rejected alternatives (architecture, process, tooling, convention) → `.context/adr/decisions/`, not inline prose in another file
- A behavioral correction/confirmation from the user, or a non-obvious project fact/reference → `.context/memory/` (see below) - not inline prose, and not the same thing as an ADR (that's structural, this is behavioral/factual)

---

## Recording Decisions (ADR)

This is automatic, not a command - see `.context/adr/README.md` for the full read/write protocol.

- As soon as a structural choice is settled - and especially when alternatives were considered and rejected - write it down yourself in `.context/adr/decisions/` as `proposed`. Only the user can move it to `accepted`.
- Before proposing an approach in a domain, check `.context/adr/decisions/` and `.context/adr/context/` first - do not re-propose something already rejected in an `accepted` decision.
- Never edit an `accepted` decision file. If it changes, supersede it - see the write protocol.

---

## Recording Feedback (Memory)

This is automatic, not a command - see `.context/memory/README.md` for the full read/write protocol. Do it in the moment, not "later" - a correction not written down within the same unit of work is one you'll fail to apply next session.

Write an entry the instant one of these happens, even if the user didn't ask you to remember it:

- **The user corrects how you're working** ("no, don't do X", "stop doing Y") → `.context/memory/feedback_<slug>.md`.
- **The user confirms a non-obvious approach worked** (accepts an unusual choice without pushback, "yes exactly, keep doing that") → same file, type `feedback`. This is the half people forget - don't only record failures, or the memory drifts toward excess caution over time.
- **You learn an ongoing project fact not derivable from code/git** (a deadline, a stakeholder ask, why something is scoped a certain way) → `.context/memory/project_<slug>.md`.
- **You learn where something lives externally** (tracker, dashboard, vault) → `.context/memory/reference_<slug>.md`.

Before starting a unit of work, `.context/memory/MEMORY.md` is already covered by the mandatory read order in `ai-workflow-entrypoint.md` - open an individual entry when its one-line hook looks relevant to what you're about to do, same as you would an ADR.

---

## Before Moving to the Next Unit

1. The current unit works end-to-end within its defined scope.
2. No invariant defined in `architecture.md` was violated.
3. `progress-tracker.md` reflects the completed work.
4. This stack's build/typecheck and test commands pass (see `.context/infra.md` for the actual commands).
5. `.env.example` is up to date if any env var was added.
6. `CHANGELOG.md` is updated.
7. Any correction or validated approach the user gave during this unit is written to `.context/memory/` (see Recording Feedback above) - don't let it live only in chat history.
