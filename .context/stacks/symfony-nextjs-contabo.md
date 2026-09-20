# Stack recipe: Symfony + Next.js + Contabo

> **Last validated: 2026-09-20.** This recipe pins specific versions and exact snippets (Symfony 8, Next.js 16, API Platform 4, etc.) as of that date - treat them as a strong starting point to verify, not gospel. See "Freshness check" below.
>
> Pairs with these coding-conventions files: `php.md`, `symfony.md`, `typescript.md`, `nextjs.md`, `tailwind.md`, `ui.md`.
> Used by `INIT.md` §2 when the user picks this recipe. All "§1.N" references below mean "the answer to question N collected in `INIT.md` §1".

## Freshness check (do this before following Part 3 or Part 4)

Tools drift faster than this file gets updated. Before scaffolding or auditing anything:

1. Check the current stable versions of the pinned tools (Symfony, Next.js, API Platform, Clerk SDKs, Tailwind, the others in the Stack table below) - a quick web check is enough, no need for exhaustive research.
2. If a version or pattern here is stale (a new major version, a deprecated API, a changed recommended pattern), don't silently follow the old instructions and don't silently switch to the new one either:
   - Tell the user what changed and what you're switching to.
   - **Update this file in place** (version numbers, snippets, gotchas) so the next project init starts from the corrected version instead of drifting back into the same staleness.
   - Bump the "Last validated" date above.
3. If everything checks out, bump the date anyway - it tells the next run this was actually re-verified, not just copy-pasted forward.

This makes the recipe a living document, the same way `.context/coding-conventions/*.md` already are - it should improve every time it's used, not just the first time it was written.

One paragraph description (shown when `INIT.md` lists available recipes): **Symfony 8 + API Platform backend, Next.js 16 (App Router) frontend, Clerk auth, Docker Compose, deployed to a Contabo VPS behind nginx + certbot, with GitHub Actions CI/CD.**

---

## Part 1 - Reference architecture

Paste this into `.context/architecture.md` verbatim (adjusting the stack table/ports once real values are known):

### Stack

| Layer          | Technology                        | Role                              |
| -------------- | --------------------------------- | --------------------------------- |
| Backend        | Symfony 8 + API Platform 4        | REST API (JSON-LD)                |
| Database       | PostgreSQL + Doctrine ORM         | Persistence                       |
| Cache          | Redis                              | Provisioned via Docker Compose, not yet wired into Symfony cache (see `backend/config/packages/cache.yaml`) |
| Async          | Symfony Messenger                 | Background jobs                   |
| Frontend       | Next.js 16 (App Router)           | UI - SSR + client                 |
| Styling        | Tailwind CSS v4 + shadcn/ui       | Design system                     |
| Server state   | TanStack Query v5                 | Fetch, cache, revalidate          |
| Client state   | Zustand                           | Global UI / auth state            |
| Forms          | React Hook Form + Zod             | Validation + submission           |
| Auth           | Clerk                             | Auth, JWT, webhooks               |
| i18n           | next-intl                         | Translations                      |

### Repo Structure

```
/
├── backend/                  - Symfony + API Platform
├── frontend/                 - Next.js 16 + pnpm
├── infra/                    - deploy scripts + nginx configs
├── docker-compose.yml        - shared service definitions (backend + frontend, both Docker)
├── docker-compose.override.yml - local overrides (ports, bind mounts, hot reload)
├── docker-compose.prod.yml   - prod overrides (env, restart policies, build targets)
└── CHANGELOG.md
```

### Frontend `src/` Tree (mandatory)

Initialize with `src/` (answer **Yes** to `create-next-app`'s "Would you like to use `src/` directory?").

```
src/
├── app/
│   ├── (auth)/              # Public route group - no layout
│   │   └── [page]/
│   │       ├── components/
│   │       │   ├── hooks/
│   │       │   │   └── use[Component].ts
│   │       │   └── [Component].tsx
│   │       ├── hooks/
│   │       │   └── use[Page].ts
│   │       ├── services/
│   │       │   └── [page].ts
│   │       └── page.tsx
│   ├── (dashboard)/         # Protected route group - sidebar layout
│   │   ├── hooks/
│   │   │   └── use[Layout].ts
│   │   ├── layout.tsx
│   │   └── [section]/
│   │       ├── components/
│   │       │   ├── hooks/
│   │       │   │   └── use[Component].ts
│   │       │   └── [Component].tsx
│   │       ├── hooks/
│   │       │   └── use[Page].ts(x)
│   │       ├── services/
│   │       │   └── [section].ts
│   │       ├── page.tsx             # List
│   │       ├── new/page.tsx         # Create
│   │       └── [id]/page.tsx        # Detail
│   ├── layout.tsx
│   └── page.tsx
├── components/
│   ├── ui/                  # shadcn/ui primitives
│   └── [domain]/            # Domain-specific components
├── constants/
│   ├── app.ts               # App-level constants (APP_NAME, MERCURE_URL, etc.)
│   └── [domain].ts          # Domain-specific constants (e.g. operators.ts)
├── hooks/                   # Reusable hooks (client)
├── i18n/
│   ├── en.json              # English translations
│   └── fr.json              # French translations (add more locales here)
├── lib/
│   ├── api.ts               # Fetch wrapper - JWT injection, 401 redirect
│   ├── i18n.ts              # next-intl config: routing, navigation, getRequestConfig
│   └── utils.ts             # Pure helpers (cn, formatAmount…) - NO utils/ subfolder
├── schemas/                 # Zod schemas + inferred form types
├── services/                # Reusable services (server)
├── store/                   # Zustand stores (useUIStore…)
└── types/
    └── [domain].ts          # One file per domain (e.g. auth.ts, operator.ts, transaction.ts)
```

### Backend `src/` Layout

```
src/
├── Entity/       - Doctrine entities
├── Repository/   - All queries (never in services)
├── Service/      - Business logic (all classes named *Service)
└── ...
```

### Component & Hook Placement

**Hooks** are the logic layer for **Client Components**. **Services** are the equivalent for **Server Components** - they fetch and shape data server-side, never run in the browser.

| Scope                                       | Location                                              |
| ------------------------------------------- | ----------------------------------------------------- |
| Reusable component (multiple pages)         | `src/components/[domain]/[Component].tsx`             |
| Component specific to one page              | `src/app/.../components/[Component].tsx`              |
| Reusable hook (multiple pages)              | `src/hooks/use[Domain].ts`                            |
| Hook specific to one page                   | `src/app/.../hooks/use[PageName].ts`                  |
| Hook specific to a reusable component       | `src/components/[domain]/hooks/use[ComponentName].ts` |
| Hook specific to a colocated page component | `src/app/.../components/hooks/use[ComponentName].ts`  |
| Reusable service (multiple pages)           | `src/services/[domain].ts`                            |
| Service specific to one page               | `src/app/.../services/[section].ts`                   |

### Scripts That Must Run Before First Paint

For the rare case where something has to happen before the browser paints
(e.g. a dark-mode class on `<html>` to avoid a flash of the wrong theme, or
scrolling to an anchor on a direct link) - a regular Client Component's
`useEffect` is too late: it only runs after React hydrates, well after first
paint. Use `next/script` with `strategy="beforeInteractive"` in the root
`layout.tsx` instead - it injects and blocks like a classic `<script>`, ahead
of hydration. Reserve it for this specific problem; everything else that can
afford to run after first paint stays a normal Client Component/hook.

Where the script is *declared* in JSX doesn't affect when it runs - Next.js
always hoists `beforeInteractive` scripts into the initial response ahead of
`<body>`. What does matter: any DOM element the script touches (e.g. an id it
scrolls to) must already be in the server-rendered HTML the script ships
with, not something a Client Component renders in after hydration - the
script runs before that exists.

### Key Invariants

- The `<main>` landmark lives **only** in route group layouts - never in individual pages or client components.
- The backend defines all API routes - frontend never invents routes.
- All entity IDs are UUIDs (strings) - never cast to number.
- Auth guard lives in `src/proxy.ts` (Clerk) - never implement a custom auth guard.

### System Boundaries

- `backend/` - owns all data, business rules, and API responses.
- `frontend/` - owns all UI; consumes the API; never accesses the DB directly.
- `infra/` - owns deployment scripts and nginx config; no application logic.

### Storage Model

- **PostgreSQL**: all persistent data via Doctrine entities.
- **Money**: stored as integers (cents) - never floats.
- **Timestamps**: `createdAt` / `updatedAt` on all entities via lifecycle callbacks.

### Auth and Access Model

- **Clerk** handles auth, JWT, and OAuth - never implement custom auth flows.
- Auth guard in `src/proxy.ts` protects the `(dashboard)` route group via `clerkMiddleware`.
- **Every user-owned resource MUST be listed in `CurrentUserExtension::OWNED_RESOURCES` and MUST throw `AccessDeniedException` when no authenticated user is present - never `return` silently.** A silent return exposes all rows if a route is ever made public. See `.context/coding-conventions/symfony.md` → _Data isolation - CurrentUserExtension_.

---

## Part 2 - Infra reference

Paste this into `.context/infra.md` verbatim (fill in real domains/ports as they're assigned):

### Overview

> Two possible topologies - keep only the one this project uses, delete the other.

**Topology A - single instance per service (default):**

- **Server**: Contabo VPS, Ubuntu
- **Web server**: nginx + certbot (SSL)
- **Backend**: Docker (PHP-FPM + nginx) - `b.[project].domain.com` on port [XXXX]
- **Frontend**: Docker (Next.js standalone) - `[project].domain.com` on port [XXXX]
- **Deploy path**: `/home/www/[project-name]`

**Topology B - rolling zero-downtime deploy (2 instances per service):**

- **Server**: Contabo VPS, Ubuntu
- **Web server**: nginx + certbot (SSL)
- **Backend**: Docker (PHP-FPM + nginx) - `b.[project].domain.com`, 2 instances behind nginx: port [XXXX] (`backend_a`) and port [XXXX] (`backend_b`)
- **Frontend**: Docker (Next.js standalone) - `[project].domain.com`, 2 instances behind nginx: port [XXXX] (`frontend_a`) and port [XXXX] (`frontend_b`)
- **Deploy path**: `/home/www/[project-name]`
- nginx load-balances both instances of each service via a static `upstream` block with passive health checks; `infra/deploy.sh` updates one instance at a time with a health check (`GET /api/health`) before moving to the next, so a deploy never interrupts service. See §3 below (rolling deploy setup) for the full mechanics.

### Docker (backend + frontend)

**Topology A - single instance:**

- `docker-compose.yml` (root) - shared service definitions for postgres + redis + backend + frontend.
- `docker-compose.override.yml` (root) - **local only** - ports, bind mounts, hot reload.
- `docker-compose.prod.yml` (root) - **prod only** - production overrides (env, volumes, restart policies, build targets).
- Backend API exposed on **port 8000** locally (http://localhost:8000); frontend on **port 3000** (http://localhost:3000).
- `vendor/` **must** be in `backend/.dockerignore` - never copy Composer dependencies into the build context.
- `frontend/Dockerfile` is multi-stage (`dev` / `builder` / `runner`): local dev runs the `dev` target with the source bind-mounted (hot reload); prod builds the Next.js **standalone** output (`output: "standalone"` in `next.config.ts`) and runs it from the minimal `runner` stage.
- `NEXT_PUBLIC_*` vars are **build-time**: `next build` bakes them in from the committed `frontend/.env`. `frontend/.env.local` is excluded via `.dockerignore` so prod builds never bake in local dev values.

**Local dev (single command, from the project root):**

```bash
docker compose up    # postgres + redis + backend + frontend - API at http://localhost:8000, app at http://localhost:3000
```

**Topology B - rolling zero-downtime deploy:**

- `docker-compose.yml` (root) - postgres + redis + `backend_a`/`backend_b` + `frontend_a`/`frontend_b`, defined via `x-backend`/`x-frontend` YAML anchors. Only `backend_a`/`frontend_a` carry a `build:` block - `backend_b`/`frontend_b` just reference the resulting image tag. **Never add `build:` to both instances of a pair** - building the same image tag concurrently races (`failed to solve: image "...:latest": already exists`).
- `docker-compose.override.yml` (root) - **local only** - ports/bind mounts/hot reload for the `_a` instance only. Local dev doesn't need 2 instances, only prod does.
- `docker-compose.prod.yml` (root) - **prod only** - production overrides for both instances of both services, via anchors.
- Backend on ports **[XXXX]**/**[XXXX]** (`_a`/`_b`), frontend on **[XXXX]**/**[XXXX]** (`_a`/`_b`) in prod; locally just **8000**/**3000** (single instance).
- `vendor/` **must** be in `backend/.dockerignore` - never copy Composer dependencies into the build context.
- `frontend/Dockerfile` is multi-stage (`dev` / `builder` / `runner`), same as Topology A.
- `NEXT_PUBLIC_*` vars are **build-time**, same as Topology A.

**Local dev (from the project root) - only the `_a` instances run:**

```bash
docker compose up postgres redis backend_a frontend_a    # API at http://localhost:8000, app at http://localhost:3000
```

**Production** - `infra/deploy.sh` uses both compose files, plus `--env-file` since Compose does not read a service's `env_file` for `${VAR}` interpolation in the prod overrides:

```bash
docker compose --env-file ./backend/.env -f docker-compose.yml -f docker-compose.prod.yml
```

> nginx on the **host** (not dockerized) proxies each domain to the port published by its container (frontend / backend). Run `infra/first-deploy.sh` once before `infra/nginx/setup.sh` so the containers are up and listening on those ports first.

### Env Variables

- `.env` files are **committed** and hold production values.
- `.env.local` files are **gitignored** and override values for local dev.
- Backend env vars must be declared in **both** `backend/.env` AND `docker-compose.prod.yml`'s (root) `environment:` section (as `${VAR}`).
- After adding a new backend env var → recreate: `docker compose up -d --force-recreate backend`.
- `.env.example` must always be up to date.

### Nginx

- Configs named after the domain:
  - `infra/nginx/[project].domain.com` - frontend
  - `infra/nginx/b.[project].domain.com` - backend
- Setup script: `infra/nginx/setup.sh` - installs config + runs certbot.
- **Topology B only (rolling deploy)**: each config defines an `upstream` block listing both instances (`max_fails=1 fail_timeout=5s` per server, `proxy_next_upstream error timeout`, `proxy_connect_timeout 2s`), and `proxy_pass` targets the upstream name instead of `http://localhost:<port>`. Config is static and never reloaded by the deploy script - nginx's passive health checks route around whichever instance is currently down.

### Deploy Scripts

- `infra/deploy.sh` - triggered via GitHub Actions on push to `main`.
- `infra/first-deploy.sh` - run **once** on the server to set up the environment (clone repo if not already present, build and start backend + frontend containers); the git clone must be conditional: `[ ! -d ".git" ] && git clone ...`.
- **Topology A (single instance)** - deploys are **build-before-swap**: `infra/deploy.sh` builds new images while the old containers keep serving, then `up -d` only recreates the services whose image changed - minimal downtime, and a broken build (`set -e`) never touches the running site.
- **Topology B (rolling deploy)** - `infra/deploy.sh` builds once, then rolls `backend_a` → `backend_b` → `frontend_a` → `frontend_b` one at a time: `up -d --no-deps <instance>`, poll that instance's own `/api/health` directly (bypassing nginx) until 200 or `HEALTH_TIMEOUT` (60s), only then move to the next. If an instance never becomes healthy, the script aborts (`exit 1`) and leaves the other, still-serving instance untouched. No separate migration step - `docker/entrypoint.sh` already migrates on every backend container start, and the sequential roll order guarantees the schema is migrated before the second instance serves. `infra/first-deploy.sh` starts all 4 instances directly (`up -d --build --wait`) - nothing is live yet, so no rolling logic is needed.

### GitHub Actions

- **Secrets**: `CONTABO_HOST`, `CONTABO_USER`, `CONTABO_SSH_PRIVATE_KEY`.
- **Naming convention**: workflow name is `Deploy to Contabo` - never `Deploy on Contabo`. Applies to `name:` (top-level), `jobs.<job>.name:`, and `steps.- name:`.

### Known Gotchas

#### Docker nginx - DNS caching after backend container recreation

Applies only when nginx runs in its **own container** (separate from the PHP-FPM backend, with `fastcgi_pass backend:9000`). Nginx resolves the `backend` hostname at startup and caches the IP. When the backend container is recreated on deploy it gets a new Docker-assigned IP, and nginx keeps the stale one → 502 until nginx itself is restarted.

Fix: use Docker's internal resolver with a short TTL **and** a variable upstream (the variable is what forces re-resolution at request time - a literal hostname in `fastcgi_pass` ignores the resolver):

```nginx
resolver 127.0.0.11 valid=5s ipv6=off;

location ~ ^/index\.php(/|$) {
    set $upstream backend:9000;
    fastcgi_pass $upstream;
    ...
}
```

Does **not** apply to the single-container setup (`fastcgi_pass 127.0.0.1:9000`) used by this recipe's default architecture.

#### Nginx + Certbot - proxy headers stripped on renewal

The certbot renewal config uses `installer = nginx`, which rewrites the `location /` block on every `certbot renew` and strips all `proxy_set_header` directives.

Consequence: `X-Forwarded-For` missing → `$request->getClientIp()` returns the Docker bridge IP (e.g. `172.26.0.1`).

**Always do both on every project:**

1. The backend nginx `location /` block must contain:

   ```nginx
   proxy_http_version 1.1;
   proxy_set_header Host $host;
   proxy_set_header X-Real-IP $remote_addr;
   proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
   proxy_set_header X-Forwarded-Proto $scheme;
   client_max_body_size 20M;
   ```

2. Create `/etc/letsencrypt/renewal-hooks/deploy/restore-nginx-proxy-headers.sh` that re-applies these headers if missing, then reloads nginx.

### Test Commands (reference only - do not run automatically)

**Backend:**

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml \
  exec -T -e APP_ENV=test -e APP_SECRET=test-secret backend \
  php bin/phpunit tests/Unit --no-coverage
```

> Topology B (rolling deploy): replace `backend` with `backend_a`.

**Frontend** (from `frontend/`):

```bash
pnpm lint
pnpm test --ci --passWithNoTests
```

---

## Part 3 - Fresh project init (this recipe's steps, run after `INIT.md` §1)

> **Prerequisites**: Ask the user to make sure **Docker Desktop is running** before proceeding.

### 3.0 Additional info to collect (on top of `INIT.md` §1)

1. **Frontend domain** - e.g. `my-app.example.com`
2. **Backend domain** - e.g. `b.my-app.example.com`
3. **Ports**:
   - Local: frontend (default `3000`) & backend (default `8000`) - single instance, even if rolling deploy is enabled below.
   - **Rolling zero-downtime deploy** - should this project run 2 instances per service (frontend + backend) behind nginx, rolled one at a time with a health check before moving to the next? (default: **no** - only add this complexity if the project expects significant production traffic)
     - **No** (default) → Prod: 1 port for frontend, 1 port for backend.
     - **Yes** → Prod: 4 ports - frontend `_a` / frontend `_b` / backend `_a` / backend `_b`. Follow §3.3b in addition to the steps below.
   - **Before assigning prod ports** (either case): read the centralized port registry on the server to pick free ports that continue the existing numbering without gaps. **You (the agent) run this yourself via `ssh contabo`** (host alias already configured locally) - this is a read-only lookup, not a deploy action:
     ```bash
     ssh contabo "cat /home/www/app.ports.txt"
     ```
     E.g. if existing backend ports go up to `8007`, the next free one is `8008` - not an arbitrary jump like `8010`.
   - **After assigning prod ports**, append them to the registry (format: `<port>  <domain>`, one per line). **You run this yourself too**:
     ```bash
     ssh contabo "echo '<port>  <domain>' >> /home/www/app.ports.txt"
     ```
     - Single instance (default): one line per service, e.g. `3005  my-app.example.com` and `8004  b.my-app.example.com`.
     - Rolling deploy (if enabled): one line per instance, with the **second** instance's domain suffixed `(2nd)` - e.g. `3010  my-app.example.com (2nd)` and `8008  b.my-app.example.com (2nd)`.
4. **Mercure** - does this project need real-time push features? (default: **yes**)
5. **Authentication mode** - Clerk is the only option. Choose the registration mode:
   - **Clerk with registration** (default) - public sign-in + sign-up.
   - **Clerk without registration** - sign-in only, users created via the Clerk dashboard. Delete the register route (see §3.3).
6. **API Platform** - does this project need API Platform? (default: **yes**)
   - **Use it when**: public/partner-facing REST/GraphQL API, need automatic OpenAPI docs, or external clients consume the backend.
   - **Skip it when**: the backend only serves this one frontend, you prefer full control over controllers/serialization, or the project is simple enough that the overhead isn't worth it.
7. **Internationalization (i18n)** - does this project need multi-language support? (default: **yes** - next-intl)
8. **Google Analytics** - does this project need it? (default: **no**). If yes, get the Measurement ID from analytics.google.com.
9. **Microsoft Clarity** - heatmaps + session recordings? (default: **no**). If yes, get the Project ID from clarity.microsoft.com.
10. **Mailer sender address (`MAILER_FROM`)** - address transactional emails are sent from. Use `[project_slug]@madainsight.com`.
    > ⚠️ Before proceeding, set up the mailbox and DNS records:
    >
    > **Step 1 - cPanel (NTMada)**: log in to cPanel for `madainsight.com` → Email Accounts → create `[project_slug]@madainsight.com`.
    >
    > **Step 2 - DNS (NameSilo)** for `madainsight.com`:
    >
    > | Name | Type | Value | TTL |
    > |---|---|---|---|
    > | `mail.[project_slug]` | A | `<mail-server-ip>` (ask the user) | 3603 |
    > | `[project_slug]` | MX | `mail.[project_slug].madainsight.com` | 3603 |
    > | `[project_slug]` | TXT | `v=spf1 a mx ip4:<mail-server-ip> ~all` | 3603 |
    >
    > **Step 3 - AWS SES**: go to [SES Identities](https://us-east-2.console.aws.amazon.com/ses/home?region=us-east-2#/identities) → Create identity → Email address → `[project_slug]@madainsight.com` → confirm via the verification email.

### 3.1 Create the GitHub repository

Wire up the remote:

```bash
git remote set-url origin https://github.com/<owner>/<project-slug>.git
```

Then add secrets at **https://github.com/`<owner>`/[project-slug]/settings/secrets/actions/new**:

| Secret | Value |
|---|---|
| `CONTABO_HOST` | ask the user for their VPS IP |
| `CONTABO_USER` | ask the user for their SSH user |
| `CONTABO_SSH_PRIVATE_KEY` | see below |

**How to get `CONTABO_SSH_PRIVATE_KEY`:**

```bash
ssh contabo "cat ~/.ssh/id_rsa"
```

Copy the full output (including `-----BEGIN ... PRIVATE KEY-----` / `-----END ... PRIVATE KEY-----`) and paste it as the secret value. These must be in place before the first push to `main` so CI/CD can deploy immediately.

### 3.2 Scaffold the code

If `backend/` and `frontend/` don't exist yet, scaffold them:
- `backend/` - Symfony 8 skeleton + API Platform 4 (if enabled in §3.0.6).
- `frontend/` - `create-next-app` with `src/` directory (answer **Yes**), App Router, Tailwind v4.

### 3.3 Replace all placeholders

Use the answers from `INIT.md` §1 and §3.0 to replace every placeholder across the repo.

| Placeholder | Replace with |
|---|---|
| `[Project Name]` | Display name - in `.context/project-overview.md` (title + `App Name`), `frontend/src/app/layout.tsx`, `frontend/src/app/page.tsx`, `frontend/src/app/(dashboard)/layout.tsx` |
| `[project-name]` | Slug - in `.context/infra.md` (deploy path), `.github/workflows/deploy.yml`, `infra/deploy.sh`, `infra/first-deploy.sh`, `infra/nginx/setup.sh` |
| `[project_slug]` | Slug - in `.context/infra.md`, `docker-compose.yml`, `docker-compose.override.yml` and `docker-compose.prod.yml` (`name:` and container names) |

> **Docker network naming**: the internal network is always called `network` in compose files. Docker Compose automatically prefixes it with the project name (`name:` field), producing `[project_slug]_network`. Never name the network `[project_slug]_network` directly.

| `[project].domain.com` | Frontend domain - in `.context/infra.md`, `backend/.env`, `backend/.env.example`, `infra/nginx/setup.sh` |
| `b.[project].domain.com` | Backend domain - same files as above |
| `[FRONTEND_PORT]` | Prod frontend port - in `.context/infra.md`, `docker-compose.prod.yml`, `infra/nginx/setup.sh` |
| `[PROD_BACKEND_PORT]` | Prod backend port - in `.context/infra.md`, `docker-compose.prod.yml`, `infra/nginx/setup.sh`, AND in `infra/nginx/b.<domain>` (`proxy_pass http://localhost:<port>;`) |
| `[owner]/[repo]` | GitHub repo - in `infra/first-deploy.sh` |
| `[LETSENCRYPT_EMAIL]` | Let's Encrypt notification email (ask the user) - in `infra/nginx/setup.sh` |

> **If rolling zero-downtime deploy was enabled**: use `[FRONTEND_PORT_A]`/`[FRONTEND_PORT_B]` and `[BACKEND_PORT_A]`/`[BACKEND_PORT_B]` instead, per §3.3b. In `infra/nginx/setup.sh`, point the temporary HTTP-only bootstrap configs at the `_a` ports.

**Let's Encrypt email**: used for SSL renewal notifications, set as `LE_EMAIL` in `infra/nginx/setup.sh`. Each domain gets its own certificate - `setup.sh` makes two separate `certbot --nginx` calls. Do NOT combine into a single SAN cert.

**Fill in `.context/project-overview.md`**, `.context/ui-context.md`, `.context/coding-conventions/tailwind.md` (color tokens) as described in `INIT.md` §1.

**Set `APP_NAME` / `NEXT_PUBLIC_APP_NAME`:**
- `frontend/.env` + `frontend/.env.example` → `NEXT_PUBLIC_APP_NAME=<Project Name>`
- `backend/.env` + `backend/.env.example` → `APP_NAME=<Project Name>`

**Rename nginx config files:**
- `infra/nginx/[project].domain.com` → `infra/nginx/<frontend-domain>`
- `infra/nginx/b.[project].domain.com` → `infra/nginx/<backend-domain>`

Update their contents with the real domains and prod ports. Update `.context/infra.md` with the real domains, ports, and deploy path.

**Update `README.md`**: replace title and description with project name, slug, and objective.

**Set `CORS_ALLOW_ORIGIN`** in `backend/.env` and `backend/.env.example` - build the regex from the frontend domain:
```
^(https?://(localhost|127\.0\.0\.1)(:[0-9]+)?|https://<frontend-domain>)$
```
(dots in the domain must be escaped as `\.`)

**Authentication mode**:
- **Clerk with registration** → leave as-is; proceed to §3.4 for Clerk setup.
- **Clerk without registration** → proceed to §3.4, then delete `frontend/src/app/[locale]/(auth)/register/` and any link to it.

**API Platform**:
- **No** → `backend/composer.json` remove `api-platform/core` + `composer update`; delete `backend/config/packages/api_platform.yaml` and `backend/config/routes/api_platform.yaml` if present; remove `#[ApiResource]` + its `use` from all entities.

**i18n / next-intl**:
- **No** → remove `next-intl` from `frontend/package.json` + `pnpm install`; remove the `withNextIntl` wrapper from `next.config.ts`; remove i18n routing from `frontend/middleware.ts`; delete `frontend/src/i18n/`, `frontend/messages/`, `frontend/src/app/[locale]/(dashboard)/settings/`; remove the Settings nav entry from `DashboardLayoutClient.tsx`; remove `locale` params/`useTranslations`/`getTranslations`/`[locale]/` segments everywhere under `frontend/src/app/`.

**Google Analytics**:
- **No** → delete `frontend/src/components/tracking/GoogleAnalytics.tsx`, its import/usage in `layout.tsx`, `GA_MEASUREMENT_ID` from `constants/app.ts`, and `NEXT_PUBLIC_GA_MEASUREMENT_ID` from env files.
- **Yes** → fill `NEXT_PUBLIC_GA_MEASUREMENT_ID` in `frontend/.env`.

**Microsoft Clarity**: same pattern as GA, with `MicrosoftClarity.tsx` / `CLARITY_PROJECT_ID` / `NEXT_PUBLIC_CLARITY_PROJECT_ID`.

**SEO indexing**: `frontend/src/app/layout.tsx` → `robots` metadata; `frontend/public/robots.txt` → `Allow: /` or `Disallow: /`.

**App icon and PWA manifest**: generate `frontend/src/app/icon.svg` (512×512, accent color background) and fill `frontend/public/manifest.webmanifest`, `layout.tsx` metadata (`manifest`, `themeColor`), and the homepage nav icon - see the previous boilerplate's INIT.md history for the exact snippets if needed, or derive them fresh from the accent color and project name.

### 3.3b Rolling zero-downtime deploy (only if enabled in §3.0.3)

> Skip entirely if single-instance was chosen - the default files already work as-is.

Each service runs as 2 instances (`_a` / `_b`) behind nginx, updated one at a time with a health check before moving to the next.

**1. Rewrite `docker-compose.yml`** - split `backend`/`frontend` into `backend_a`/`backend_b` and `frontend_a`/`frontend_b` via YAML anchors. Only `_a` carries `build:` (concurrent builds of the same tag race):

```yaml
name: [project_slug]

x-backend: &backend
  image: [project_slug]_backend
  depends_on:
    postgres:
      condition: service_healthy
    redis:
      condition: service_healthy
  env_file:
    - ./backend/.env
  environment: &backend-environment
    DATABASE_URL: postgresql://${POSTGRES_USER:-app}:${POSTGRES_PASSWORD:-app}@postgres:5432/${POSTGRES_DB:-app}?serverVersion=16&charset=utf8
    MESSENGER_TRANSPORT_DSN: redis://redis:6379/messages
  networks:
    - network

x-frontend: &frontend
  image: [project_slug]_frontend
  networks:
    - network

services:
  postgres:
    # ... unchanged from the single-instance file

  redis:
    # ... unchanged from the single-instance file

  backend_a:
    <<: *backend
    container_name: [project_slug]_backend_a
    build:
      context: ./backend
      dockerfile: Dockerfile
      target: dev

  backend_b:
    <<: *backend
    container_name: [project_slug]_backend_b

  frontend_a:
    <<: *frontend
    container_name: [project_slug]_frontend_a
    build:
      context: ./frontend
      dockerfile: Dockerfile
      target: dev

  frontend_b:
    <<: *frontend
    container_name: [project_slug]_frontend_b

volumes:
  postgres_data:

networks:
  network:
    driver: bridge
```

**2. Rewrite `docker-compose.override.yml`** (local only) - only `_a` gets ports/volumes:

```yaml
name: [project_slug]

services:
  backend_a:
    ports:
      - "8000:80"
    env_file:
      - ./backend/.env.local
    volumes:
      - ./backend:/var/www/html
      - /var/www/html/vendor

  frontend_a:
    ports:
      - "3000:3000"
    environment:
      WATCHPACK_POLLING: "true"
    volumes:
      - ./frontend:/app
      - /app/node_modules
      - /app/.next
```

Document in `.context/infra.md` that local dev only starts the `_a` instances: `docker compose up postgres redis backend_a frontend_a`.

**3. Rewrite `docker-compose.prod.yml`** - prod overrides on both instances via anchors:

```yaml
name: [project_slug]

x-backend-prod: &backend-prod
  restart: unless-stopped

x-frontend-prod: &frontend-prod
  restart: unless-stopped
  env_file:
    - ./frontend/.env

services:
  postgres:
    container_name: [project_slug]_postgres
    restart: unless-stopped
    volumes:
      - /var/data/[project-slug]/postgres:/var/lib/postgresql/data

  redis:
    container_name: [project_slug]_redis
    restart: unless-stopped

  backend_a:
    <<: *backend-prod
    ports:
      - "[BACKEND_PORT_A]:80"
    build:
      target: prod
    environment:
      MERCURE_URL: http://mercure-mercure-1/.well-known/mercure
    networks:
      - default
      - mercure_default

  backend_b:
    <<: *backend-prod
    ports:
      - "[BACKEND_PORT_B]:80"
    environment:
      MERCURE_URL: http://mercure-mercure-1/.well-known/mercure
    networks:
      - default
      - mercure_default

  frontend_a:
    <<: *frontend-prod
    ports:
      - "[FRONTEND_PORT_A]:3000"
    build:
      target: runner

  frontend_b:
    <<: *frontend-prod
    ports:
      - "[FRONTEND_PORT_B]:3000"

networks:
  mercure_default:
    external: true
```

> Drop the `MERCURE_URL` override / `mercure_default` network from both backend services if Mercure was declined.

**4. Rewrite the nginx configs** - `infra/nginx/<frontend-domain>` and `infra/nginx/b.<backend-domain>` each get an `upstream` block with passive health checks:

```nginx
upstream [project_slug]_frontend {
    server 127.0.0.1:[FRONTEND_PORT_A] max_fails=1 fail_timeout=5s;
    server 127.0.0.1:[FRONTEND_PORT_B] max_fails=1 fail_timeout=5s;
}

server {
    listen 80;
    server_name [project].domain.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name [project].domain.com;

    ssl_certificate /etc/letsencrypt/live/[project].domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/[project].domain.com/privkey.pem;

    location / {
        proxy_pass http://[project_slug]_frontend;
        proxy_connect_timeout 2s;
        proxy_next_upstream error timeout;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}
```

```nginx
upstream [project_slug]_backend {
    server 127.0.0.1:[BACKEND_PORT_A] max_fails=1 fail_timeout=5s;
    server 127.0.0.1:[BACKEND_PORT_B] max_fails=1 fail_timeout=5s;
}

server {
    listen 80;
    server_name b.[project].domain.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name b.[project].domain.com;

    ssl_certificate /etc/letsencrypt/live/b.[project].domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/b.[project].domain.com/privkey.pem;

    client_max_body_size 20M;

    location / {
        proxy_pass http://[project_slug]_backend;
        proxy_connect_timeout 2s;
        proxy_next_upstream error timeout;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

**5. Rewrite `infra/deploy.sh` and `infra/first-deploy.sh`**:

```bash
#!/bin/bash
set -e

DEPLOY_PATH="/home/www/[project-name]"
COMPOSE="docker compose --env-file ./backend/.env -f docker-compose.yml -f docker-compose.prod.yml"
HEALTH_TIMEOUT=60
HEALTH_INTERVAL=2

wait_for_health() {
    local port="$1"
    local elapsed=0

    until curl -sf "http://localhost:$port/api/health" > /dev/null; do
        elapsed=$((elapsed + HEALTH_INTERVAL))
        if [ "$elapsed" -ge "$HEALTH_TIMEOUT" ]; then
            return 1
        fi
        sleep "$HEALTH_INTERVAL"
    done
}

roll_instance() {
    local service="$1"
    local port="$2"

    echo "==> Rolling $service (port $port)..."
    $COMPOSE up -d --no-deps "$service"

    if ! wait_for_health "$port"; then
        echo "==> ERROR: $service did not become healthy within ${HEALTH_TIMEOUT}s. Aborting - the other instance is untouched and still serving."
        exit 1
    fi

    echo "==> $service is healthy."
}

echo "==> Pulling latest code..."
cd "$DEPLOY_PATH"
git pull origin main

echo "==> Building new images (current instances keep serving - no downtime)..."
$COMPOSE build

# Migrations run automatically inside docker/entrypoint.sh on every backend
# container start (before supervisord launches) - no separate migration step
# needed here. Rolling backend_a before backend_b already serializes this:
# backend_a's entrypoint applies pending migrations and only then starts
# serving, so backend_b never starts against a not-yet-migrated schema.

roll_instance backend_a [BACKEND_PORT_A]
roll_instance backend_b [BACKEND_PORT_B]

roll_instance frontend_a [FRONTEND_PORT_A]
roll_instance frontend_b [FRONTEND_PORT_B]

echo "==> Done!"
```

> **Critical pitfall - do not add a separate migration step.** A one-off container like `docker compose run --rm backend_a php bin/console doctrine:migrations:migrate` does not do what it looks like: the prod image's `ENTRYPOINT` (`backend/docker/entrypoint.sh`) ignores the command passed to `run` and always ends with `exec supervisord`, which never returns - the container never exits, `--rm` never fires, and CI times out. Migrations already run automatically in `entrypoint.sh` on every backend container start; the sequential roll order is enough to guarantee they're applied before the second instance serves.

> **Retrofitting an already-deployed single-instance project**: add a one-time `docker rm -f [project_slug]_backend` / `[project_slug]_frontend` immediately before rolling `backend_a` / `frontend_a` respectively - removing the old container right before its replacement claims the port keeps the downtime window to just that one roll.

```bash
#!/bin/bash
# Run once on the server to bootstrap the environment before CI/CD takes over.
set -e

REPO_URL="https://github.com/[owner]/[repo].git"
DEPLOY_PATH="/home/www/[project-name]"
COMPOSE="docker compose --env-file ./backend/.env -f docker-compose.yml -f docker-compose.prod.yml"

echo "==> Setting up deployment directory..."
mkdir -p "$DEPLOY_PATH"
cd "$DEPLOY_PATH"

if [ ! -d ".git" ]; then
    git clone "$REPO_URL" .
fi

echo "==> Starting both instances of backend and frontend..."
# Nothing is live yet, so no rolling logic is needed - migrations run
# automatically inside docker/entrypoint.sh on each backend container start.
$COMPOSE up -d --build --wait

echo "==> First deploy complete! Run bash infra/nginx/setup.sh from the project root to configure nginx + SSL."
```

**6. Add health endpoints**:

- **Backend** - `GET /api/health`, no auth, `200 {"status":"ok"}` after a successful DB ping, `503 {"status":"error","message":...}` otherwise. Follow the "raw SQL never in services" convention (`.context/coding-conventions/symfony.md`) - the DB ping lives in a repository, not the service:

  `backend/src/Repository/HealthRepository.php`:
  ```php
  <?php

  declare(strict_types=1);

  namespace App\Repository;

  use Doctrine\DBAL\Connection;
  use Throwable;

  class HealthRepository
  {
      public function __construct(
          private Connection $connection,
      ) {
      }

      public function pingDatabase(): bool
      {
          try {
              $this->connection->executeQuery('SELECT 1');

              return true;
          } catch (Throwable) {
              return false;
          }
      }
  }
  ```

  `backend/src/Service/HealthService.php`:
  ```php
  <?php

  declare(strict_types=1);

  namespace App\Service;

  use App\Repository\HealthRepository;

  class HealthService
  {
      public function __construct(
          private HealthRepository $healthRepository,
      ) {
      }

      public function isDatabaseHealthy(): bool
      {
          return $this->healthRepository->pingDatabase();
      }
  }
  ```

  `backend/src/Controller/HealthController.php`:
  ```php
  <?php

  declare(strict_types=1);

  namespace App\Controller;

  use App\Service\HealthService;
  use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
  use Symfony\Component\HttpFoundation\JsonResponse;
  use Symfony\Component\HttpFoundation\Response;
  use Symfony\Component\Routing\Attribute\Route;

  #[Route('/api/health')]
  class HealthController extends AbstractController
  {
      public function __construct(
          private HealthService $healthService,
      ) {
      }

      #[Route('', methods: ['GET'])]
      public function check(): JsonResponse
      {
          if (!$this->healthService->isDatabaseHealthy()) {
              return $this->json([
                  'status' => 'error',
                  'message' => 'Database connection failed.',
              ], Response::HTTP_SERVICE_UNAVAILABLE);
          }

          return $this->json(['status' => 'ok']);
      }
  }
  ```

  If the project has a global request listener guarding a route prefix (e.g. an admin-secret check on `/api/admin/*`), verify it does **not** match `/api/health`.

- **Frontend** - `GET /api/health`, always `200 {"status":"ok"}` once the process is up:

  `frontend/src/app/api/health/route.ts`:
  ```ts
  import { NextResponse } from "next/server";

  export async function GET() {
    return NextResponse.json({ status: "ok" });
  }
  ```

**7. Update `.context/infra.md`** with the dual-instance topology, ports, and rolling deploy mechanics (delete the single-instance variant instead).

### 3.4 Generate secrets and Clerk setup

```bash
openssl rand -hex 32      # → APP_SECRET in backend/.env
```

Create `.env.local` files from their templates:

```bash
cp backend/.env.local.example backend/.env.local
cp frontend/.env.local.example frontend/.env.local
```

The user must:

1. Create a Clerk application at **https://dashboard.clerk.com** → "Add application".
2. **Switch to the Production instance** before copying any keys - using development keys (`pk_test_`) shows a "Development mode" badge.
3. Copy **production** keys into `frontend/.env`: `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` (`pk_live_`), `CLERK_SECRET_KEY` (`sk_live_`).
4. For **local development**, switch to the **Development** instance and copy dev keys (`pk_test_`/`sk_test_`) into `frontend/.env.local`.
5. Copy the JWKS URL into `backend/.env` as `CLERK_JWKS_URI` (API Keys → Advanced → JWKS endpoint). Also copy the **Development** JWKS URL into `backend/.env.local`.
6. Create a webhook for user sync: Clerk dashboard → Webhooks → Add endpoint → `https://<backend-domain>/api/webhook/clerk`, events `user.created`/`user.updated`/`user.deleted`. Copy the Signing Secret into `backend/.env` as `CLERK_WEBHOOK_SECRET` (and the Development one into `backend/.env.local`).

### 3.5 Install dependencies

```bash
# Backend + frontend (from the project root)
docker compose up -d
docker compose exec backend composer install
docker compose exec backend php bin/console doctrine:migrations:migrate --no-interaction

# Frontend - local node_modules for editor tooling (lint, type-check, IDE autocomplete)
cd frontend
pnpm install
```

### 3.6 Fill in remaining environment values

**AWS - IAM users (S3 + SES)** at **https://us-east-1.console.aws.amazon.com/iam/home?region=us-east-2#/users/create**:

1. **S3 backup user** (`s3__[project_slug]`) → add to group **s3_group** → create access key → fill `backend/.env`: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_S3_BACKUP_BUCKET` (ask for the full S3 URI, don't guess).
2. **SES mailer user** (`ses__[project_slug]`) → add to group **ses_group** → create access key → fill `backend/.env`: `MAILER_FROM`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` for SES.

**Mercure**: shared hub at `mercure.madainsight.com` (port 4000). JWT secret never hardcoded/committed - ask the user for `MERCURE_JWT_SECRET` and fill `backend/.env` + `frontend/.env`, or remove all `MERCURE_*` vars if declined.

### 3.7 First server deploy

```bash
git add -A
git commit -m "chore: initialize project"
git push origin main
```

> The deploy workflow will fail on this first push - the server isn't set up yet. Expected. Make sure the app works locally first.

```bash
ssh contabo
git clone https://github.com/<owner>/<project-slug>.git /home/www/<project-slug>
cd /home/www/<project-slug>
bash infra/first-deploy.sh
bash infra/nginx/setup.sh
```

Verify: frontend loads at its domain, backend `/api` returns the API Platform entrypoint (or `/` if API Platform was removed). From here, every push to `main` auto-deploys.

### 3.8 Configure automated backup

Generate a secret (LastPass extension, 32 chars) → `backend/.env` as `AWS_S3_BACKUP_WEBHOOK_SECRET` → commit + push.

Configure the backup workflow on n8n: duplicate the existing backup workflow, tag it with the app name, move to `Personal > [AppName]`, update the HTTP Request node (URL `https://<backend-domain>/api/webhook/backup`, header `X-Backup-Secret`), activate it.

---

## Part 4 - Existing project (bringing a Symfony+Next.js+Contabo project into this structure)

### 4.1 Explore the existing codebase (silent)

Read `backend/`, `frontend/`, `infra/`, `backend/.env`/`frontend/.env`, `CLAUDE.md`/`AGENTS.md`.

### 4.2 Collect missing info

Same list as Part 3 §3.0, but only ask for what the codebase doesn't already reveal (check env vars, `docker-compose.yml`, nginx configs, `composer.json`, `package.json`, presence of `frontend/messages/`, `GoogleAnalytics.tsx`, `MicrosoftClarity.tsx`, `register/` route, etc.).

### 4.3 Wire up `.context/` files

For each of `project-overview.md`, `architecture.md` (Part 1 above), `infra.md` (Part 2 above), `ui-context.md`, `coding-conventions/tailwind.md`, `progress-tracker.md`: if missing or still placeholder, fill it in from the codebase + answers. If it already has real content, leave it.

Ensure `CLAUDE.md`/`AGENTS.md` point at `.context/ai-workflow-entrypoint.md`.

### 4.4 Audit and complete infrastructure

- `git remote -v` → fix if wrong.
- GitHub Actions secrets (`CONTABO_HOST`, `CONTABO_USER`, `CONTABO_SSH_PRIVATE_KEY`) - verify present.
- Secrets in `.env` - generate any missing (`openssl rand -hex 32` for `APP_SECRET`).
- Ask for any blank remaining values: AWS S3/SES credentials, `MAILER_FROM`, `CORS_ALLOW_ORIGIN`.
- Verify `.env.example` matches `.env` (values redacted).

### 4.5 Deploy (if not already live)

Same flow as §3.7.

### 4.6 Configure automated backup

Same flow as §3.8.
