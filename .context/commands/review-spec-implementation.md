---
description: "Verify that the implemented code matches its feature spec - checks every acceptance criterion, data model, and API contract"
argument-hint: "<spec number or name fragment>"
---

Verify that the implementation matches its feature spec. Every acceptance criterion must be traceable to real code.

Spec to verify: `$ARGS`

---

## Step 1 - Find the spec

List files in `.context/feature-specs/`.

- If `$ARGS` is provided, match by numeric prefix or name fragment (case-insensitive).
- If omitted, show specs with `status: in-progress` or `status: done` and ask the user to pick one.
- If none found: "No implemented specs to verify. Run `/dev` first."

Read the full spec file.

---

## Step 1.5 - Delegate verification to a specialized subagent

If you were spawned by another command to execute only a subset of these steps, skip the sub-delegation below and go straight to Step 2 - but the worktree resolution at the top of Step 2 still runs unconditionally, whoever invokes it.

Otherwise, before delegating, check `.context/docs/verif/<id>.md` (in `.worktrees/<id>/` - see Step 2's worktree resolution). If it exists, run `git add -A && git write-tree` (in the worktree) and compare against the recorded tree hash. If they match and every recorded command exited 0, tell the `spec-verifier` subagent it can skip re-running the test/typecheck commands and trust the record (still verify the actual code against the spec, that part never gets skipped). If the record is missing, stale (hash mismatch), or shows a non-zero exit code, tell the subagent to run `Test command:`/`Typecheck command:` from `.context/project-settings.md` itself as part of its review.

Launch a subagent specialized for spec verification (agent type: `spec-verifier`, if your tool supports named subagent types - otherwise a general coding subagent) to execute Steps 2 through 6 below against the spec file. Wait for its structured report, then continue to Step 7.

---

## Step 2 - Load context (silent)

**Worktree resolution - first thing this step does, no matter who invoked it:** the spec was implemented in `.worktrees/<id>/` on branch `feature/<id>` (see `.context/commands/dev.md`), not necessarily in this session's own working directory. If `.worktrees/<id>/` doesn't exist or isn't on that branch, stop and tell the user - `/dev` hasn't set it up (or something removed it). Every git command from here on, in this command and in anything it delegates to, runs against that worktree (`git -C .worktrees/<id>/ <command>`, or `cd` there first).

Read:
- `.context/architecture.md`
- `.context/coding-conventions/global.md`
- `.context/coding-conventions/security.md`
- Determine the project's actual layer folders and stack from `.context/architecture.md`, then read the matching `.context/coding-conventions/*.md` files for whichever layer(s) the spec touches

---

## Step 3 - Verify each acceptance criterion

For each `- [x] criterion` (checked) and `- [ ] criterion` (unchecked) in the spec, find the code that satisfies it.

**How to verify each criterion:**

- Search for the relevant entity, route, component, hook, or service that implements it.
- Read the actual implementation - don't assume it exists because the box is checked.
- Confirm the behavior matches the criterion exactly (field names, HTTP method, response shape, access rules, edge case handling).

Assign one of three verdicts per criterion:

| Verdict | Meaning |
| --- | --- |
| ✅ PASS | Code found and behavior matches the criterion |
| ⚠️ PARTIAL | Code exists but behavior is incomplete or differs from the spec |
| ❌ FAIL | No implementation found, or behavior contradicts the criterion |

---

## Step 3.5 - Neutralization check (critical logic only)

For acceptance criteria that cover critical business logic (services, complex hooks - the same scope `.context/ai-workflow-rules.md`'s TDD mandate already limits to; skip simple CRUD/UI/config), pick the test file(s) that should catch a regression in that logic. Temporarily break the invariant (comment out or invert the guarding condition), run ONLY those narrowly-scoped test file(s), and confirm they go red. Then IMMEDIATELY revert the change (`git checkout -- <file>` or manual undo) before writing anything to the report - this mutation must never survive past this single check. If the tests do NOT go red, that's a ❌ finding: "criterion N has no test that actually catches its own regression," even if the criterion otherwise looks implemented. This is the one deliberate exception to read-only verification, and it must always end with the code restored.

---

## Step 4 - Verify the data model

For each entity and field listed in the spec's **Data Model** table:

- Find the entity/model definition on the server side (location per `.context/architecture.md`).
- Check that each field exists with the correct type, constraints (nullable, length, etc.), and lifecycle hooks.
- Check that the corresponding client-side type (if the stack has one) matches.

Verdict: ✅ / ⚠️ / ❌ per entity.

---

## Step 5 - Verify the API contract

For each route in the spec's **API Contract** table:

- Find the corresponding route/controller/resource handler on the server side.
- Confirm: method, route path, request body shape, response shape, auth requirement.
- If the stack uses a declarative API framework (e.g. API Platform), also check its resource/operation attributes, serialization groups, and security rules.

Verdict: ✅ / ⚠️ / ❌ per route.

---

## Step 6 - Report

Output a structured report:

### Verification report - NNN Feature Name

**Acceptance Criteria**

| # | Criterion | Verdict | Evidence |
| --- | --- | --- | --- |
| 1 | criterion text | ✅ PASS | `path/to/file.ext:line` |
| 2 | criterion text | ⚠️ PARTIAL | found in X but missing Y |
| 3 | criterion text | ❌ FAIL | no implementation found |

**Data Model**

| Entity | Verdict | Notes |
| --- | --- | --- |
| Foo | ✅ | - |

**API Contract**

| Route | Verdict | Notes |
| --- | --- | --- |
| POST /api/foos | ⚠️ | missing auth check |

**Summary**

- X / Y criteria passing
- Overall: ✅ COMPLETE / ⚠️ INCOMPLETE / ❌ FAILING

---

## Step 7 - Convention review

Run `/review-changes` on the files changed by this feature (scope = `frontend`, `backend`, or `all` depending on what the spec touched). This checks coding conventions - hook/component split, braces, prop type naming, repo injection, etc.

Fix all violations before proceeding to Step 8.

---

## Step 8 - Fix or flag

**If all spec verdicts are ✅ and conventions are clean:**
- Update any unchecked `- [ ]` criteria in the spec to `- [x]`.
- Update `status` to `done` and update `.context/progress-tracker.md` accordingly.
- Tell the user: "Spec fully verified and conventions clean - marking as done."

**If any spec verdict is ⚠️ or ❌:**
- Do NOT mark the spec as done.
- For each gap, ask the user: "Do you want me to fix this now, or log it as an open question in the spec?"
  - Fix now → implement the missing piece inline, then re-verify that criterion.
  - Log it → add to the spec's **Open Questions** section: `- [ ] [criterion text] - not yet implemented`.

---

## Step 9 - Commit and push

Once the spec is marked `done`, tell the user:
> Before pushing, do a quick manual scan of the diff (`git diff HEAD`) to catch anything automated review may have missed - dead code, stray debug logs, TODO comments, or anything that looks off. Once satisfied, run `/commit-and-push` to commit and push these changes.
