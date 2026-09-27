**Mandatory read at the start of every session, before any code:**
`.context/ai-workflow-entrypoint.md`

**Commit and push gate:** Run `git commit` and `git push` only when the user directly invokes `$commit-and-push` (Codex) or `/commit-and-push` (other command environments). No other workflow may invoke that command or commit/push on its own. A direct user invocation of the command authorizes its canonical commit and push steps.
