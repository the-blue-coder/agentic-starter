---
description: "Autonomously implement several specs one after another in isolated worktrees, each building on the previous, and hand off uncommitted changes with a decision report"
argument-hint: "<spec ID or dropped spec file> <spec ID or dropped spec file> [more] | resume <batch-id>"
---

Implement two or more existing feature specs in series and autonomously, in the order given. Each spec is implemented and reviewed by its own subagent in its own worktree, on top of the verified result of the previous spec, so a later spec can depend on an earlier one. The primary agent is the queue orchestrator; at the end it hands the complete reviewed result to the configured local target branch.

**This command is autonomous.** Follow `.context/commands/autonomous-mode.md` for the whole run: never ask the user anything after it starts, decide ambiguities yourself, record every decision, set failed specs aside, and finish with its final report. It never commits or pushes. For independent specs that can be built simultaneously, use `/implement-swarm`.

This command reuses the batch machinery of `.context/commands/implement-swarm.md` - manifest, per-spec worktrees, review loop, transfer, cleanup, resume - and only differs where stated below. Read both files; when this file is silent, `implement-swarm.md` applies, with "batch" meaning "queue".

Arguments:

- `/implement-queue <spec-id-or-file> <spec-id-or-file> [...]` starts a queue. Require at least two distinct exact spec IDs or validated local spec files/`file:` URIs, resolved per `.context/commands/spec-selector-resolution.md`. **The given order is the execution order** (put a spec after the specs it depends on). If no selectors are supplied, select every eligible `todo` spec in ID order (at least two required) and list them in the final report.
- `/implement-queue resume <batch-id>` resumes the recorded queue, following the resume rules of `implement-swarm.md`.

Read `.context/commands/autonomous-mode.md`, `.context/commands/implement-swarm.md`, and the files listed there before proceeding.

## Differences from `/implement-swarm`

- **Preflight:** same checks (framing, target branch at `<base-sha>`, no other active spec or worktree, no incomplete manifest, allowed `preflight_paths`), except the runtime does not need concurrent subagents. The manifest lives in the same `.worktrees/.parallel-batches/<batch-id>/` directory with an extra `"mode": "queue"` field and the specs listed in execution order, so `/status`, `/commit-and-push`, and every "incomplete batch" guard treat a queue like any other batch.
- **No upfront worktrees:** create each spec's worktree only when its turn comes, never earlier.
- **Per-spec loop**, in the given order, skipping specs already `passed` or `excluded` on resume:

  1. **Create its worktree** `.worktrees/<spec-id>/` on `feature/<spec-id>` at `<base-sha>`, synchronize its spec and design handoff, and record it in the manifest, exactly as in swarm Phase 2.
  2. **Seed it with the previous result.** If an earlier spec passed, take the staged binary patch of the most recent passed spec's worktree against `<base-sha>` (it already contains every earlier passed spec), register it as an artifact under `patches/seed-<spec-id>.patch`, apply it to this worktree with Git's three-way application, run `git add -A`, and record the resulting tree (`git write-tree`) in the manifest as this spec's `review_base`. For the first spec, `review_base` is `<base-sha>`'s tree. This is not a commit.
  3. **Implement.** Launch one `implementer` subagent with the batch ID, spec ID, spec path, worktree path, branch, base SHA, and `review_base`, following swarm Phase 3 (batch-worker mode of `.context/commands/dev.md`, Steps 6 through 10, following the TDD loop and TDD journal of `.context/coding-conventions/tdd.md`, leaving the tracker and changelog to the orchestrator, no commits). It sees the earlier specs' code as existing code and implements only its own spec.
  4. **Review.** Run the swarm Phase 4 review loop (spec-verifier, convention-reviewer, performance-reviewer, seo-reviewer (only for a spec with `seo: true`), security-reviewer, targeted fixes, five-round cap) for this spec only. Reviewers diff against `review_base` instead of `<base-sha>` so they judge only this spec's changes. On success mark the worktree copy of the spec `done`, run `git add -A`, and set the spec `passed`.
  5. **Failure.** A worker that fails twice, or a spec that still has findings after five rounds, is `excluded` (see autonomous mode). Keep its worktree and branch as they are, then continue the queue from the last passed spec's state. If a later spec depends on the excluded one it will most likely be excluded too; record that as its reason.

  Only one worker or reviewer runs at a time. Update the manifest before and after every step.
- **Final integration:** the last passed spec's worktree already holds the complete cumulative result, so no patch integration is needed. Treat it as the integration worktree: reconcile shared metadata once (remove every passed spec's entry from the tracker's `Next Up`/`In Progress`, combine the proposed changelog bullets, record valid memory notes), run `Test command:` and `Typecheck command:` once, then run the convention, performance, and security reviews on the complete diff, plus the SEO review only when at least one spec has `seo: true` against `<base-sha>` (role `integration`, all passed spec IDs). Keep the five-iteration cap. If nothing passed, stop without changing the target checkout.
- **Transfer and cleanup:** identical to swarm Phases 6 and 7, transferring from that final worktree. Remove every passed spec's worktree and branch after the verified transfer; never touch excluded specs' worktrees or branches.
- **Report:** deliver the final report of `.context/commands/autonomous-mode.md`, listing specs in the order they ran.

## Rules

- Never commit, push, create a remote branch, or invoke `/commit-and-push`. Only the user's later direct invocation of `/commit-and-push` authorizes those actions.
- Never run a spec before every earlier spec in the queue is `passed` or `excluded`.
- Never edit the primary target checkout before the final transfer.
