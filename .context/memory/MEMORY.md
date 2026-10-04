# Memory Index

<!-- One line per entry: - [Title](file.md) - one-line hook. See README.md for the read/write protocol. -->

- [Step numbering](feedback_step-numbering.md) - never use "Step 0"/"Step N.5", always renumber sequentially
- [Quick-path reviews](feedback_quick-path-reviews.md) - run all three reviews (changes, performance, security last) after every direct edit, including post-spec fixes
- [Commit and push gate](feedback_commit_push_gate.md) - commit and push only when the user directly invokes the command
- [Local main review](feedback_local_main_review.md) - no PRs; transfer verified spec changes to the local target branch for review
- [Tool-agnostic design handoff](feedback_design_tool_agnostic_handoff.md) - any design tool or local reference; no provider lock-in
- [Direct starter edits](feedback_direct_starter_edits.md) - edit starter workflow files directly when asked; do not create a spec unless requested
- [Initialization and architecture](feedback_initialization_architecture_split.md) - keep shared init separate from stack decisions and architecture docs
- [Cross-agent spec selectors](feedback_cross_agent_spec_selectors.md) - dropped spec files must work across local coding agents
- [Minimal AGENTS.md](feedback_agents_md_minimal.md) - AGENTS.md holds only the mandatory-read pointer, rules live in .context/
- [Batch autonomy and TDD](feedback_batch_autonomy_and_tdd.md) - autonomous multi-spec runs never commit; strict TDD loop; Codex dropped
- [Convention reference projects](project_convention_reference_projects.md) - which real project models each stack's conventions and layout
