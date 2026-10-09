---
type: decision
status: proposed
date: 2026-10-09
tags: [testing, tdd, agent-workflows]
supersedes: [[2026-10-04 - Apply the TDD loop across the workflow]]
affects: [[Implementation workflows]]
---

## Context

The strict loop (one test, one red run, one green run, one journal row) made implementation slow: the cost grows with the number of assertions rather than with the risk of the code. It also applied to simple CRUD, serialization groups, and trivial utilities, and forced a test for criteria that are pure UI or configuration.

## Decision

Keep TDD, but work one acceptance criterion at a time: write the tests that pin the criterion, run them once to confirm they fail for the right reason, write the minimum code, refactor, move on. Limit the strict scope to business logic (services, domain rules, state processors, security filters, hooks and schemas carrying business rules) and bug fixes. Replace the per-cycle TDD journal with a per-criterion `## Test map` in the verification record. Allow criteria that are pure UI, markup, styling, copy, or configuration to be marked "verified manually" with the method used. E2E tests cover only the journeys the spec marks as critical. The neutralization check is unchanged.

## Why not something else

- **Keep one test per cycle**: rejected because run count scales with assertions while the protection it adds over a per-criterion batch is small.
- **Drop mandatory TDD, test after**: rejected because tests written afterwards mirror the implementation and let the agent over-build.
- **Remove the traceability requirement**: rejected because an uncovered business-logic criterion is the failure the workflow exists to catch; "verified manually" only relaxes it for criteria no unit test can usefully assert.

## Consequences

- Positive: fewer test runs and less reporting per spec; the same coverage guarantee for business logic.
- Negative / risk: a per-criterion batch can anticipate slightly more than one test at a time; "verified manually" depends on the worker and reviewer judging it honestly.
- Generates: updates to `tdd.md`, dev, review-spec-implementation, review-changes, spec, the implementer agents, and the stack testing conventions.
