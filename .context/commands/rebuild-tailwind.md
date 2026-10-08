---
description: "Rebuild the project's Tailwind CSS output using the build command of its stack"
---

Rebuild Tailwind CSS so the compiled stylesheet reflects the current sources and design tokens.

## Step 1 - Find the build command

Read `.context/architecture.md` (stack, folder layout, how commands run - directly or through Docker) and pick the first match:

1. **Symfony with `symfonycasts/tailwind-bundle`** (Twig stack): `php bin/console tailwind:build` (add `--minify` only if the project's infra notes say production builds minify).
2. **A dedicated Tailwind script** in `package.json` (for example `build:css`, `tailwind:build`, `css`): run it with the project's package manager (pnpm by default).
3. **Next.js or Gatsby**: Tailwind is compiled by the framework build. Run the project's `build` script with the package manager.

If none matches, stop and tell the user which command is missing instead of guessing one.

Run the command from the directory that owns the Tailwind entry (for example `frontend/` in a decoupled stack). When `.context/architecture.md` says commands run in a container, run it there.

## Step 2 - Run it and report

- Run the command once, without `--watch`.
- On success, report the command that ran and the output file it refreshed when the build prints it.
- On failure, show the relevant error output and stop. Do not retry blindly or edit files to work around it.

Never commit, push, or edit source files as part of this command.
