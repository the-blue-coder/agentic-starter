---
type: decision
status: accepted
date: 2026-10-04
tags: [performance, reviews, agent-workflows]
affects: [[Implementation workflows]]
---

## Context

The workflow reviewed conventions, spec conformance, and security, but nothing checked whether the code an agent introduces is slow: N+1 queries, unbounded lists, request waterfalls, leaked listeners, heavy imports. Agents produce these readily and no existing review owns them.

## Decision

Add `/review-performance`, a review of the diff's introduced code only, backed by a `performance-reviewer` subagent and per-stack rules in `.context/coding-conventions/performance/` (`global.md` plus one file per stack, loaded like the other stack conventions). It runs in `/implement`, `/implement-queue`, `/implement-swarm`, the individual feature path, and the quick path, always before `/review-security`, which stays last and keeps the target-branch handoff. A finding requires a concrete cost and a bounded fix; `shortcut:`-marked code and cold paths are left alone. On the quick path the review is mandatory when the diff contains a query or network call, a loop or collection processing, UI rendering, a dependency change, or file handling; otherwise the review reports "Not applicable" itself, so the agent never decides to skip it.

## Why not something else

- **Fold performance into `/review-changes`**: rejected because it dilutes that review's convention focus and cannot be skipped independently when not applicable.
- **Run it after security**: rejected because security must judge the final code, and both reviews may edit files.
- **A single `performance.md`**: rejected because stacks differ widely and reviewers should load only the files matching the diff.
- **Agent judges when to run it on the quick path**: rejected because the existing review gate exists precisely so the agent does not judge; a closed applicability list keeps it mechanical.

## Consequences

- Positive: performance regressions caught before handoff; small non-applicable diffs cost one cheap "Not applicable" run.
- Negative / risk: one more review per iteration; static review cannot measure real load, so findings are heuristic.
- Generates: new command, subagent (Claude Code and OpenCode), and `performance/` convention folder; updates to the entrypoint gates, implement workflows, README, and quick-path memory.
