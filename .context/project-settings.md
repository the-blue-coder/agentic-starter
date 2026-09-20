# Project Settings

This file holds project-specific settings that vary between projects using this starter - as opposed to `.context/coding-conventions/`, which holds fixed rules that don't change per project. `Merge mode: pr` means `/commit-and-push` pushes the spec's branch and opens a PR for review; `local` means it squash-merges locally into `Target branch` without going through a remote PR. `Ship confirmation: human` means the workflow asks before merging or opening a PR; `automatic` means it proceeds without asking. `Test command:` and `Typecheck command:` are read by `/dev`, `/commit-and-push`, and `/review-spec-implementation` - keep those two keys named exactly as below.

Merge mode: [pr or local]
Target branch: [e.g. main]
Ship confirmation: [human or automatic]
Test command: [e.g. pnpm test, or - if none]
Typecheck command: [e.g. pnpm typecheck, or - if none]
