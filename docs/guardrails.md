# Guardrails that run automatically

| Guardrail | Effect |
| --- | --- |
| `.claude/hooks/check-request-scope.sh` (prompt hook) | Suggests `/spec` first when a request looks like substantial feature work |
| `.claude/hooks/enforce-spec-pipeline.sh` (pre-write hook) | Refuses writes to application code while a spec is in progress with unchecked criteria |
| `.githooks/pre-commit` | Refuses a commit on `feature/<spec-id>` unless that spec exists and `/dev` has picked it up |
| Spec framing gate | `/spec` stops until `/init-project`, the product framing in `project-overview.md`, architecture (with `## Testing`), and the design system are complete |
| Commit and push gate | Nothing commits or pushes unless you directly invoke `/commit-and-push` |
| Mandatory review gate | Every direct code edit is followed by the reviews before the work counts as done |
