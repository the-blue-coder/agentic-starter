---
type: decision
status: superseded
date: 2026-10-04
tags: [testing, tdd, agent-workflows]
affects: [[Implementation workflows]]
---

## Context

The workflow required "test first" only for critical business logic and bug fixes; everything else was test-after, and no test tool was ever chosen explicitly. With coding agents, writing tests in a batch before the code (test-first) lets the agent anticipate and over-build; the short red-green-refactor loop keeps it to the minimum the current test needs. The owner wants real TDD on the starter, backend and frontend, with test technologies chosen per stack at architecture time.

## Decision

Apply the strict TDD loop (one failing test, minimum code, refactor) to backend code, frontend logic, and bug fixes; component and e2e tests cover UI behavior and user journeys. `/architecture` records the test technologies in a mandatory `## Testing` section of `.context/architecture.md`, `/spec` blocks until it is complete, and `.context/coding-conventions/tdd.md` defines the loop, scope, acceptance-criteria mapping, and the TDD journal that workers keep in the verification record. Reviewers check results (coverage of every criterion, behavior-focused tests, journal consistency) and may run the existing neutralization check; they cannot prove ordering, so discipline rests with the implementing worker. E2E tests use Playwright; agent-side visual verification uses Claude in Chrome under Claude Code and Playwright elsewhere.

## Why not something else

- **Strict TDD on everything, UI included**: rejected because TDD on markup and styling is slow and brittle for little protection; component and e2e tests cover UI behavior instead.
- **Keep test-first for critical logic only**: rejected because it keeps the batch-writing failure mode and leaves most code untested.
- **Choose test tools globally in the starter**: rejected because tools depend on the stack, so the choice belongs to `/architecture`.
- **Reviewer enforcement of test-then-code order**: rejected because a reviewer only sees the final diff; the worker's journal and the neutralization check are the achievable controls.

## Consequences

- Positive: smaller, test-justified code from agents; explicit test tooling per project; every acceptance criterion traceable to a test.
- Negative / risk: slower implementation per spec; the journal adds reporting overhead; ordering compliance still depends on the worker following instructions.
- Generates: new `## Testing` section in the architecture template and gate; updates to dev, worker prompts, reviews, and stack conventions.
