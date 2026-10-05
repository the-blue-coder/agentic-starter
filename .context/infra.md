# Infrastructure & Deployment

> New project: choose the architecture with /architecture first, then apply the selected stack-specific setup separately. Existing project: /architecture documents what is present. /init-project configures shared workflow settings and does not choose or apply infrastructure.

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

[Add the commands used to run the test suite(s) once known, including how to run a single test file or test name.]

**Speed (Docker projects):** TDD runs dozens of test commands per spec, so their overhead matters.
- Keep the app container running and run tests with `docker compose exec <service> <command>`. Never use `docker compose run` for tests: it creates a new container on every call.
- On Windows, keep the project in the WSL2 filesystem (`\\wsl$\...`) and run Docker from WSL2 rather than from a Windows drive mount. File I/O on a mounted drive is several times slower for PHP and Node.
- Use a dedicated test database that is already created and migrated, so a test run never rebuilds the schema.
