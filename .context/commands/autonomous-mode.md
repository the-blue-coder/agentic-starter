# Autonomous Mode

Shared rules for `/implement-queue` and `/implement-swarm`. These commands run unattended from start to finish: the user starts them, walks away, and reads one final report.

## Never commit or push

Autonomy never extends to Git history. No agent in these workflows runs `git commit` or `git push`, creates a remote branch, or invokes `/commit-and-push`. Verified changes end up uncommitted and unstaged on the target branch; only the user's later direct `/commit-and-push` invocation authorizes those actions.

## Decide instead of asking

- Never stop to ask the user a question, request a confirmation, or wait for a menu pick once the run has started. This replaces the "Ready to start?" gates and the "fix now or log it?" prompts of `/dev` and `/implement`.
- When a spec is ambiguous, silent, or contradicts the code, choose the simplest interpretation that satisfies the acceptance criteria and respects `.context/coding-conventions/` and `.context/adr/decisions/`. Never contradict a `status: accepted` decision; pick the compliant option instead.
- When a review leaves a gap, fix it within the five-round cap; never defer it to the user mid-run.
- Never invent behavior the spec does not describe to fill a gap. Choose the minimal reading and record it as a decision.
- Hard stops remain: unsafe or ambiguous Git state, a missing or inconsistent manifest, an unexpected destination hash, or a destructive action outside the workflow. These preserve all data and appear in the final report instead of being decided.

## Record every decision

Workers and reviewers report each non-trivial decision to the orchestrator as: spec ID, the question, the choice made, the reason, and the alternative rejected. The orchestrator keeps them in the batch's reports (`decisions.md` under `.worktrees/.parallel-batches/<batch-id>/reports/`, registered as an artifact like any other report) and does not drop any.

## Failed specs are set aside

A spec whose worker fails, or that still has findings after five review rounds, is marked `excluded` in the manifest and set aside; the run continues with the remaining specs. An excluded spec keeps its worktree, its `feature/<spec-id>` branch, and `status: in-progress`, so a later `/dev <spec-id>` can resume it. Only passed specs are integrated and transferred. If no spec passes, nothing is transferred and the report says so.

## Final report

When the run ends, show the user one report in English:

1. **Result** - specs transferred to the target branch (uncommitted), specs excluded, and the exact next step (`git diff HEAD`, then `/commit-and-push`).
2. **Decisions made on your behalf** - every recorded decision, grouped by spec, with its reason and the rejected alternative. Flag the ones most worth a second look.
3. **Excluded specs** - for each, the failing criteria or findings, the worktree path to resume from, and a suggested fix.
4. **Checks** - test/typecheck results and the review outcomes per spec and for the combined result.
5. **Spec deviations and open questions** - anything the spec did not anticipate.
