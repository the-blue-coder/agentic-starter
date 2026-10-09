---
type: decision
status: proposed
date: 2026-10-09
tags: [testing, agent-workflows]
affects: [[Implementation workflows]]
---

## Context

`/dev` wrote `.context/docs/verif/<spec-id>.md` with a tree hash, the exit codes of the test and typecheck commands, and the test map. Its only job was to let `/review-spec-implementation` skip re-running the suite when the hash still matched. The suites run in seconds, the hash goes stale as soon as the record itself is added or a file is touched, and the record piled up one file per spec without ever being read again. Only its test map carried lasting value.

## Decision

Remove the verification record. `/dev` runs the test and typecheck commands itself and writes the `## Test map` at the end of the spec. `/review-spec-implementation` always runs the commands through its `spec-verifier` and reads the test map from the spec. `/status` no longer reports a record, `/update-workflow` deletes the obsolete `.context/docs/verif/` folder, and the handoff comparison of the spec copies ignores the `## Test map` section like it ignores `status:` and the checkboxes.

## Why not something else

- **Keep the record, drop only the hash**: rejected because the remaining content (command exit codes) is already in the review reports and the test map fits in the spec.
- **Keep a record folder as a log**: rejected because nothing reads it and git history already holds the evidence.

## Consequences

- Positive: one fewer file and folder per spec, a simpler `/dev` Step 10, no stale-hash logic, the evidence sits next to the criteria it covers.
- Negative / risk: the verifier always re-runs the suite (seconds on current stacks; a project with a very slow suite pays for it each review).
- Generates: updates to `dev`, `implement`, `implement-swarm`, `review-spec-implementation`, `status`, `update-workflow`, `tdd.md` and `ai-workflow-rules.md`; supersedes the record-related parts of [[2026-10-09 - Lighten the TDD loop per criterion]].
