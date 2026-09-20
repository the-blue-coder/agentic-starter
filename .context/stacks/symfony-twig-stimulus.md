# Stack recipe: Symfony + Twig + Stimulus (server-rendered monolith)

> **Last validated: 2026-09-20.** This recipe pins specific versions and exact snippets (Symfony 6.4, Tailwind v4 via `symfonycasts/tailwind-bundle`, etc.) as of that date - treat them as a strong starting point to verify, not gospel. See "Freshness check" below.
>
> Pairs with these coding-conventions files: `php.md`, `symfony.md`, `twig.md`, `stimulus.md`, `javascript.md`, `tailwind.md`.
> Used by `INIT.md` §2 when the user picks this recipe. All "§1.N" references below mean "the answer to question N collected in `INIT.md` §1".

One paragraph description (shown when `INIT.md` lists available recipes): **Server-rendered Symfony monolith - Twig templates, Stimulus/Turbo for JS interactivity (no Node.js, AssetMapper-managed), Tailwind CSS v4 compiled via a Symfony bundle, EasyAdminBundle back-office, Doctrine/MySQL persistence.** No separate frontend app or build step - contrast with the decoupled `symfony-nextjs-contabo` recipe.

## Freshness check (do this before following Part 3 or Part 4)

Tools drift faster than this file gets updated. Before scaffolding or auditing anything:

1. Check the current stable versions of the pinned tools (Symfony, EasyAdminBundle, `symfonycasts/tailwind-bundle`, VichUploaderBundle, Stimulus/Turbo, AssetMapper) - a quick web check is enough, no need for exhaustive research.
2. If a version or pattern here is stale (a new major version, a deprecated API, a changed recommended pattern), don't silently follow the old instructions and don't silently switch to the new one either:
   - Tell the user what changed and what you're switching to.
   - **Update this file in place** (version numbers, snippets, gotchas) so the next project init starts from the corrected version instead of drifting back into the same staleness.
   - Bump the "Last validated" date above.
3. If everything checks out, bump the date anyway - it tells the next run this was actually re-verified, not just copy-pasted forward.

This makes the recipe a living document, the same way `.context/coding-conventions/*.md` already are - it should improve every time it's used, not just the first time it was written.

---

## Part 1 - Reference architecture

Paste this into `.context/architecture.md` verbatim (adjust the domain model and security roles once known):

### Stack

| Layer | Technology | Role |
| --- | --- | --- |
| Framework | Symfony 6.4 | HTTP kernel, DI, routing, Twig |
| Database | MySQL + Doctrine ORM | Persistence |
| Admin UI | EasyAdminBundle | CRUD back-office |
| Public UI | Twig + Tailwind CSS v4 + Stimulus | Server-rendered public portal |
| JS interactivity | Stimulus + Turbo (AssetMapper) | SPA-like navigation, controllers |
| CSS | Tailwind CSS v4 via `symfonycasts/tailwind-bundle` | Compiled to `public/styles/app.css` (not committed) |
| File uploads | VichUploaderBundle | Files in `public/uploads/` |
| Rich text | EditorJS (custom form type) | Editorial content fields, only if the project needs one |
| Email | SendGrid (or the project's mailer of choice) | Transactional emails |

### Repo Structure

```
/
├── assets/
│   ├── controllers/          # Stimulus controllers, grouped by concern into subfolders (subfolder = `--` namespace)
│   ├── utils/                 # Non-controller helper modules extracted from controllers, mirroring controllers/ subfolders
│   ├── early/                 # Classic (non-module) *.js, loaded via a plain <script src>, never through importmap.php
│   ├── styles/
│   │   ├── app.css           # Main Tailwind entry (public site)
│   │   └── admin.css         # Admin-specific styles
│   ├── app.js                # Public JS entry
│   └── admin.js              # Admin JS entry
├── config/                   # Symfony config (packages, routes, services)
├── migrations/               # Doctrine migrations
├── src/
│   ├── Controller/
│   │   ├── Admin/            # EasyAdmin CRUD controllers + custom fields
│   │   └── MainController.php
│   ├── Entity/               # Doctrine entities
│   │   └── Trait/            # Shared entity traits (TimestampableTrait)
│   ├── Repository/           # All Doctrine queries
│   ├── Security/             # AppAuthenticator
│   ├── Service/              # Business logic services
│   └── Twig/                 # Twig extensions
├── templates/
│   ├── admin/                # EasyAdmin custom templates
│   ├── common/                # Header + footer partials
│   ├── main/                  # Public page templates
│   ├── partials/              # Shared UI partials, grouped by component type (buttons/, badges/, cards/, ...)
│   └── base.html.twig         # Base layout
└── importmap.php              # JS/CSS dependency map (AssetMapper - no Node.js)
```

### JS / CSS - No Node.js

- **No npm/pnpm/Node.js** - JS dependencies managed via Symfony AssetMapper (`importmap.php`).
- Stimulus controllers in `assets/controllers/`, grouped into subfolders by concern; the subfolder path becomes a `--` namespace prefix on the identifier (e.g. `media/lightbox_controller.js` → `media--lightbox`). Custom event names stay stable strings, decoupled from identifiers.
- Turbo for SPA-like navigation.
- Tailwind v4 compiled to `public/styles/app.css` - **not committed**. Run `php bin/console tailwind:build --watch` during development.
- `assets/early/` - for the rare script that must run before first paint (e.g. scroll-to-anchor on a direct link, a dark-mode class on `<html>` to avoid a flash of the wrong theme). Controllers registered via `importmap.php` load as deferred ES modules, so they always run after the page has already rendered - too late for this. Reference the file with a classic `<script src="{{ asset('early/<file>.js') }}"></script>` in the template that needs it instead, which blocks and executes in place during HTML parsing. Everything else stays a Stimulus controller in `assets/controllers/`.
  **Placement matters as much as the script being blocking** - browsers paint progressively, so a blocking `<script>` still lets everything above it render first. Put the tag immediately after the element(s) it depends on, never at the bottom of the page; a script with no DOM dependency (e.g. the dark-mode one, which only touches `<html>`/`localStorage`) belongs as early as possible in `<head>`.

### File Uploads

- VichUploaderBundle - config: `config/packages/vich_uploader.yaml`.
- Files stored in `public/uploads/`.
- Upload paths defined as Symfony parameters in `config/services.yaml`.

### Published Status & 404 Enforcement

Any entity with a published/`actif` boolean field must return HTTP 404 for unpublished records on public-facing routes. Two valid patterns:

- **Repository-level filter** (preferred): add `andWhere('e.actif = true')` in a named repository method (e.g. `findOneActiveByAlias`), then do a simple null check in the controller. Fail-safe and reusable.
- **Controller check** (fallback when using a param converter): explicitly check `if (!$entity->isActif()) throw $this->createNotFoundException()`.

Never return a 200 for an unpublished record on a public route.

### Key Invariants

- All Doctrine queries in repositories - never in services.
- `persist()` and `flush()` stay in services (transaction orchestration).
- All classes in `src/Service/` are named `*Service`.
- Inject repositories via constructor - never `$em->getRepository(Foo::class)`.
- Never use FQN inline - always `use` statements at the top of the file.
- The `--color-theme` CSS variable drives the theme system - never use `--theme-color` (or whichever token name the project actually settles on - keep this row's spirit, not necessarily the literal name).

### System Boundaries

- `src/` - all data, business rules, HTTP responses.
- `templates/` - all HTML output.
- `assets/` - CSS and client-side JS behavior.
- `public/uploads/` - managed by VichUploaderBundle (not committed).
- `public/styles/app.css` - compiled Tailwind output (not committed).

### Auth and Access Model

- Form login at `/login`.
- Roles: `ROLE_ADMIN`, `ROLE_SUPERADMIN` (adjust per project).
- All `/admin` routes require at least `ROLE_ADMIN`.

---

## Part 2 - Infra reference

Unlike `symfony-nextjs-contabo`, this recipe has **no single validated hosting topology** across projects built from it - client projects on this stack have shipped with different hosts and even different local dev setups. Paste into `.context/infra.md` and fill in the specifics for *this* project rather than assuming the below is universal:

### Local dev (typical pattern seen across projects - verify per project)

A single PHP+Apache container plus a database container is the common shape:

```yaml
services:
  php:
    build:
      context: .
      dockerfile: Dockerfile
    volumes:
      - .:/var/www/symfony
    environment:
      - APACHE_RUN_USER=#1000
      - APACHE_RUN_GROUP=#1000
    ports:
      - "8080:80"
    depends_on:
      mysql:
        condition: service_healthy

  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: symfony_db
      MYSQL_USER: symfony_user
      MYSQL_PASSWORD: symfony_pass
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  mysql_data:
```

Add other services (e.g. Elasticsearch, Redis) only if the specific project actually needs them - don't carry them over by default.

### Production hosting

Not standardized - ask the user what's available (shared hosting/cPanel, a VPS, a PaaS) and fill in `.context/infra.md` accordingly. If it's a Contabo VPS with Docker + nginx like `symfony-nextjs-contabo`, that recipe's Part 2 (Docker/nginx/deploy-script shape) is a reasonable template to adapt - just remember there's no separate frontend service here, only `php` (+ MySQL, + whatever else the project needs).

### AssetMapper build step

No `npm run build` / `pnpm build` equivalent - `php bin/console tailwind:build` (prod: without `--watch`, and typically with `--minify`) is the only build step needed before deploying, alongside the usual `composer install --no-dev` and `doctrine:migrations:migrate`.

---

## Part 3 - Fresh project init

### 3.0 Additional info to collect (on top of `INIT.md` §1)

1. **Database**: MySQL (default for this recipe) or another engine the user prefers.
2. **Admin back-office**: EasyAdminBundle (default) - ask which entities need CRUD screens, and what the two admin roles (`ROLE_ADMIN` / `ROLE_SUPERADMIN`, or the project's actual naming) should be able to do differently.
3. **File uploads**: does the project need them? (VichUploaderBundle if yes)
4. **Rich text editing**: does any entity need a WYSIWYG/rich-text field? (EditorJS via a custom form type if yes)
5. **Transactional email provider**: SendGrid (seen most often on this recipe) or another Symfony Mailer-supported provider.
6. **Hosting target**: see Part 2 - there's no default here, ask.

### 3.1 Scaffold

```bash
symfony new <project> --version=6.4 --webapp
cd <project>
composer require symfony/asset-mapper symfony/stimulus-bundle symfony/ux-turbo
composer require symfonycasts/tailwind-bundle --dev
php bin/console tailwind:init
composer require easycorp/easyadmin-bundle
composer require vich/uploader-bundle          # only if file uploads are needed
composer require symfony/mailer
```

Wire up `docker-compose.yml` from Part 2's local-dev pattern, adjusted to the project's actual DB choice and any extra services.

### 3.2 Replace placeholders and fill `.context/` files

- `.context/project-overview.md`, `.context/ui-context.md` - same as any recipe, from `INIT.md` §1's answers.
- `.context/architecture.md` - Part 1 above, with the Domain Model section filled in once entities are known.
- `.context/infra.md` - Part 2 above, with the actual hosting target filled in per §3.0.6.
- Security roles in `config/packages/security.yaml` and `.context/architecture.md`'s Auth section, per §3.0.2.

### 3.3 Verify locally

`docker compose up`, confirm `/` and `/admin` both load, `php bin/console tailwind:build --watch` runs without error.

---

## Part 4 - Existing project

### 4.1 Explore the existing codebase (silent)

Read `src/`, `templates/`, `assets/`, `config/packages/security.yaml`, `composer.json`, `importmap.php`, and any `docker-compose.yml`/deploy scripts present.

### 4.2 Collect missing info

Same list as Part 3 §3.0, but only ask for what the codebase doesn't already reveal (check `composer.json` for EasyAdmin/Vich/mailer packages, `config/packages/security.yaml` for roles, `docker-compose.yml` for the DB engine and any extra services).

### 4.3 Wire up `.context/` files

Same as any recipe's Path B: fill `project-overview.md`, `architecture.md` (Part 1, adapted to what's actually there), `infra.md` (Part 2, filled from the actual deploy setup found), `ui-context.md`, `progress-tracker.md` - only where missing or still placeholder.

### 4.4 Audit and complete infrastructure

Check `.env`/`.env.local` for missing values (DB credentials, mailer DSN, any upload/storage config), and whatever CI/CD is already in place (or note that none exists yet, and ask the user whether to set one up).
