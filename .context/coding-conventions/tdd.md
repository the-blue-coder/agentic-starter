# Test-Driven Development

Non-negotiable for every agent that writes code here, whatever the stack. The stack's test tools come from the `## Testing` section of `.context/architecture.md`; stack-specific patterns live in the matching `coding-conventions/*.md`.

TDD is a **loop**, not "tests before code". Writing every test of the feature up front (test-first) invites the agent to anticipate, over-specify, and build more than the current step needs. The loop below works one acceptance criterion at a time, which keeps the code minimal without paying for one test run per assertion.

## Scope

Strict TDD applies to **business logic**: code whose breakage would be a functional, security, or data-integrity bug.

| Code | Rule |
| --- | --- |
| Backend: services, domain rules, state processors/providers, security filters/voters/listeners, validators with business rules | Strict TDD loop |
| Frontend logic: hooks, schemas and validators carrying business rules, stores, non-trivial state and calculations | Strict TDD loop |
| Bug fixes (any layer) | Strict TDD loop: the failing test reproduces the bug first |
| UI components and pages | Component tests only when they carry behavior (conditions, interaction, state), written after the logic they use; e2e tests for the user journeys the spec marks as critical |
| Simple CRUD, getters/setters, serialization groups, trivial utilities and glue code, config, generated files, pure markup/styling, migrations | No TDD; verify by running them |

If a unit of work is in the strict scope, the loop is not optional and not "quick to skip". If you are unsure whether something is business logic, ask: "would a regression here be a bug the user or the data would suffer from?" If yes, it is in scope. Non-trivial logic outside the scope still leaves behind one runnable check that fails if the logic breaks.

## The loop

Work one acceptance criterion at a time:

1. **Red** - write the tests that pin the criterion (usually one to three: the invalid or empty input, the happy path, the edge cases that matter). Run only those tests, once. Confirm they fail, and fail for the right reason (the behavior is missing - not a typo, import error, or bad setup).
2. **Green** - write the minimum code that makes them pass. Hardcoding is acceptable at this step; generalize only when a test forces it. Run the same tests.
3. **Refactor** - with everything green, clean up duplication and naming in both code and tests. Run the tests again.
4. Repeat with the next criterion.

Hard rules:

- One criterion at a time. Never write tests for a later criterion, or any production code, ahead of the current red run.
- Never write code "for later", "just in case", or for a case no test demands yet. If you think of one, it is a test of the next cycle.
- Never edit a test to make it pass. A test changes only when the requirement it states changes.
- Within a criterion, order the cases from the simplest to the richest (empty/invalid input, then the happy path, then edge cases).
- A test asserts observable behavior, not implementation details. Do not mock the code under test, and keep mocks to real boundaries (network, clock, third parties).

## Run scope per step

Test runs are the slowest part of the loop, so each step runs the narrowest scope that proves it:

| Step | Run |
| --- | --- |
| Red / Green / Refactor | The test file of the criterion being worked on (filter by name when it helps) |
| After the last cycle of a criterion | The test files of that criterion's unit |
| Final check (`dev.md` Step 10) | The full suite and the typecheck, once |

Never run the full suite or the typecheck inside a cycle. The `Command` column of `## Testing` in `.context/architecture.md` must therefore show how to run a single test file or test name, not only the whole suite.

## Acceptance criteria drive the cycles

Each acceptance criterion in the spec is covered in one of two ways, and the spec's test map says which:

- **Tested** - at least one test (unit, integration, component, or e2e) asserts it. Required for every criterion that touches strict-scope logic.
- **Verified manually** - for a criterion that is pure UI, markup, styling, copy, or configuration, no test is required. The test map states how it was verified (for example "checked in the browser at 375px and 1280px" or "ran the migration") instead of naming a test.

A criterion that is neither tested nor verified is a ❌. A criterion that touches strict-scope logic but that no test can assert is a spec defect: record it in the report as a decision instead of skipping it.

## Test levels

Pick the cheapest level that proves the behavior; the stack's levels and tools are in `.context/architecture.md` -> `## Testing`.

- **Unit** - pure logic with no I/O: domain rules, services with fakes, hooks, utilities.
- **Integration / functional** - the code with its real boundary: repository with the test database, API endpoint through the HTTP layer.
- **Component** - a UI component's behavior through its public interface, as a user would use it.
- **End-to-end** - a complete user journey in a real browser, with Playwright. Write them only for the journeys the spec marks as critical; keep them few and stable.

## Visual and browser verification (agent-side, not committed tests)

After UI work, verify the result in a real browser before reporting it done. Use Claude in Chrome when running in Claude Code, and Playwright when running in OpenCode or another agent. This is inspection (does it render and behave as the spec and design references say). It never replaces committed tests, and its findings that deserve a regression guard become e2e or component tests through the normal loop.

## Test map

Put a short map of the work at the end of the spec, in a `## Test map` section. One row per acceptance criterion:

| Criterion | Coverage |
| --- | --- |
| 1 | `file::name`, `file::name` (tested) |
| 2 | Checked in the browser at 375px and 1280px (verified manually) |

No red-failure narration and no per-cycle log: the map is the evidence that every criterion is covered, and reviewers check it against the diff.

## Reviewing

The reviewer sees only the result, so it checks what is checkable: every strict-scope unit has a test, every acceptance criterion is either mapped to a test or marked verified manually with a credible method, tests assert behavior and not the implementation, the test map exists and matches the diff, and, only where a criterion guards security or data integrity or a test looks suspect, a neutralization check (temporarily break the logic, confirm its test goes red, restore) as defined in `/review-spec-implementation`.
