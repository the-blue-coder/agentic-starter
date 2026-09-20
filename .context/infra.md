# Infrastructure & Deployment

> **Project not initialized yet?** If this file still contains `[bracketed]` placeholders, stop and run `/init-project`. The chosen stack recipe under `.context/stacks/` fills this file in.

## Overview

- **Hosting**: [e.g. VPS, Vercel, Fly.io]
- **Deploy path / target**: [where the app runs in production]
- **Domains**: [production domain(s)]

## Runtime / Containers

[Describe how the app runs - Docker Compose services, serverless functions, a single process, etc. List the compose files or config files involved and what each one is for.]

## Env Variables

- [Describe the env file convention: which files are committed vs gitignored, and where new vars must also be declared (e.g. a prod compose file's `environment:` section).]

## Web Server / Routing

- [Describe how requests reach the app - nginx configs, a platform's own routing, etc.]

## Deploy Scripts

- [Describe the deploy mechanism - CI/CD pipeline, deploy script, manual steps - and what happens on each push.]

## GitHub Actions

- **Secrets**: [list required repo secrets]

## Known Gotchas

[Add project-specific infra pitfalls here as they're discovered.]

## Test Commands (reference only - do not run automatically)

[Add the commands used to run the test suite(s) once known.]
