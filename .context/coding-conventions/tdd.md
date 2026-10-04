# Test-Driven Development

Non-negotiable for every agent that writes code here, whatever the stack. The stack's test tools come from the `## Testing` section of `.context/architecture.md`; stack-specific patterns live in the matching `coding-conventions/*.md`.

TDD is a **loop**, not "tests before code". Writing a batch of tests first (test-first) invites the agent to anticipate, over-specify, and build more than the current step needs. The loop below is what keeps the code minimal.

## Scope

| Code | Rule |
| --- | --- |
| Backend: entities, domain rules, services, repositories, API endpoints | Strict TDD loop |
| Frontend logic: hooks, utilities, schemas, validators, stores, non-trivial state | Strict TDD loop |
| Bug fixes (any layer) | Strict TDD loop: the failing test reproduces the bug first |
| UI components and pages | Component tests when they carry behavior (conditions, interaction, state), written after the logic they use; e2e tests for the user journeys in the spec |
| Config, generated files, pure markup/styling, migrations | No TDD; verify by running them |

If a unit of work is in the strict scope, the loop is not optional and not "quick to skip". If you are unsure, it is in scope.

## The loop

Work one test at a time:

1. **Red** - write exactly one test for the smallest next behavior. Run only that test. Confirm it fails, and fails for the right reason (the behavior is missing - not a typo, import error, or bad setup).
2. **Green** - write the minimum code that makes it pass. Hardcoding is acceptable at this step; generalize only when a later test forces it. Run the test and the ones already written.
3. **Refactor** - with everything green, clean up duplication and naming in both code and tests. Run the tests again.
4. Repeat with the next-smallest behavior.

Hard rules:

- One failing test at a time. Never write several tests, or any production code, ahead of the current red test.
- Never write code "for later", "just in case", or for a case no test demands yet. If you think of one, write its test as the next cycle.
- Never edit a test to make it pass. A test changes only when the requirement it states changes.
- Order cycles from the simplest case to the richest (empty/invalid input, then the happy path, then edge cases).
- A test asserts observable behavior, not implementation details. Do not mock the code under test, and keep mocks to real boundaries (network, clock, third parties).

## Acceptance criteria drive the cycles

Each acceptance criterion in the spec is split into one or more test cases, then worked one cycle at a time. Every criterion must end up covered by at least one test (unit, integration, component, or e2e). A criterion no test can assert is a spec defect: record it in the report as a decision instead of skipping it.

## Test levels

Pick the cheapest level that proves the behavior; the stack's levels and tools are in `.context/architecture.md` -> `## Testing`.

- **Unit** - pure logic with no I/O: domain rules, services with fakes, hooks, utilities.
- **Integration / functional** - the code with its real boundary: repository with the test database, API endpoint through the HTTP layer.
- **Component** - a UI component's behavior through its public interface, as a user would use it.
- **End-to-end** - a complete user journey in a real browser, with Playwright. Write them for the journeys named in the spec's acceptance criteria and for UI specs; keep them few and stable.

## Visual and browser verification (agent-side, not committed tests)

After UI work, verify the result in a real browser before reporting it done. Use Claude in Chrome when running in Claude Code, and Playwright when running in OpenCode or another agent. This is inspection (does it render and behave as the spec and design references say). It never replaces committed tests, and its findings that deserve a regression guard become e2e or component tests through the normal loop.

## TDD journal

Keep a short journal of the cycles and put it in the verification record (`.context/docs/verif/<spec-id>.md`) under `## TDD journal`. One row per cycle:

| # | Criterion | Test (file::name) | Red: command and failure reason | Green: minimal change |
| --- | --- | --- | --- | --- |

Parts of the work outside the strict scope (config, markup, migrations) are listed in one closing line with the reason. The journal is the evidence that the loop ran; reviewers check it against the diff.

## Reviewing

The reviewer sees only the result, so it checks what is checkable: every strict-scope unit has a test, every acceptance criterion maps to a test, tests assert behavior and not the implementation, the journal exists and matches the diff, and, where a journal looks suspect, a neutralization check (temporarily break the logic, confirm its test goes red, restore) as already defined in `/review-spec-implementation`.
