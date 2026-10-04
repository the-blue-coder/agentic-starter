# SEO

> Applies only where the project is SEO-friendly. Read `SEO:` and `SEO public scope:` in `.context/project-settings.md` first: `yes` means every user-facing page follows these rules, `hybrid` means only the declared public scope does (the rest, typically an authenticated dashboard, is explicitly kept out of search engines), and `no` means this file does not apply. `html.md` is the markup foundation; `performance/` covers speed, which is also a ranking factor. Keep it simple: these rules ask for correct, crawlable pages, not tricks.

## Scope and exclusion

- **Public scope** is every page a visitor can reach without signing in that the product wants found. In `hybrid`, the scope is the list recorded in `SEO public scope:`; everything else is private.
- **Private areas** (dashboards, account, checkout steps, admin, search-result and filter pages with no standalone value, preview and staging deployments) must send `noindex`, stay out of `sitemap.xml`, and sit behind authentication. Never rely on `robots.txt` to hide a page: a disallowed URL can still be indexed from links, and a crawler that cannot fetch the page never sees its `noindex`.
- A route that does not exist returns a real `404` (or `410` when removed for good), never a `200` page saying "not found" (a soft 404). A moved page returns a `301` to its new URL.

## Rendering

- Public content is in the HTML the server sends: server-rendered or statically generated. Never build a public page's primary content only in the browser after load, and never behind a click.
- Navigation between public pages uses real links with real URLs (see `html.md`), including pagination. Infinite scroll needs paginated links as a fallback.
- Public pages are indexable by default and fast (see `performance/`): mobile-first responsive layout, HTTPS, compression, and good Core Web Vitals.

## URLs

- Stable, lowercase, hyphen-separated, readable slugs; no session ids or tracking parameters in indexable URLs. Content is addressed by path, not by a query string alone.
- One canonical URL per page: pick a trailing-slash and host (`www` or not) convention and redirect the others. Every public page declares `<link rel="canonical">` pointing to itself (or to the preferred duplicate).
- Changing a URL means a `301` from the old one. Never leave two URLs serving the same content without a canonical.

## Per-page metadata

Every public page, rendered on the server:

- A unique `<title>` of about 50-60 characters, leading with the page's subject, with the brand last. Never repeat one title across pages.
- A unique `<meta name="description">` of about 120-155 characters that summarizes the page for a person.
- `<link rel="canonical">`, and `<meta name="robots" content="noindex">` only on pages that must not be indexed.
- Open Graph and Twitter Card tags: `og:title`, `og:description`, `og:url`, `og:type`, `og:image` (about 1200x630, absolute URL), `og:locale`, and `twitter:card`.
- Multilingual sites: `<html lang>` per page and `hreflang` alternates (including `x-default`) that reference each other, with canonical URLs per language.
- Metadata values come from the page's data, never hard-coded duplicates. Writing the actual title and description text is a content decision: flag it rather than inventing marketing copy.

## Crawl control files

- `robots.txt` allows the public scope, points to the sitemap, and blocks only non-content paths (API, internal assets that are not needed to render). Never block CSS or JavaScript that pages need to render.
- `sitemap.xml` lists only indexable, canonical, `200` public URLs with `lastmod` taken from real modification dates. It is generated from data, not maintained by hand, and referenced from `robots.txt`.

## Structured data

- Add JSON-LD (`<script type="application/ld+json">`) that matches the visible content: `Organization` and `WebSite` on the home page, `BreadcrumbList` on nested pages, and the type that fits the page (`Article`, `Product`, `LocalBusiness`, `Person`, `Service`, `FAQPage`, ...).
- Never mark up content the page does not show. Build the object from the same data the page renders, serialize it safely (no unescaped user input), and keep it valid.

## Internal linking and content structure

- Every public page is reachable from the navigation or another page within a few clicks; no orphan pages.
- Use breadcrumbs on nested pages. Anchor text describes the destination.
- One topic per page, one `<h1>`, meaningful headings, and body content in text rather than inside images (see `html.md`).

## Images and fonts

- `alt`, dimensions, lazy loading, and modern formats as in `html.md`.
- Self-host and preload the critical font, use `font-display: swap` (or `optional`), and reserve space to avoid layout shift.

## Implementation by stack

### Next.js

- Public pages are Server Components. Set metadata with the Metadata API (`metadata` or `generateMetadata`) including `alternates.canonical`, `openGraph`, and `robots`; do not set titles in client components.
- Generate `app/sitemap.ts` and `app/robots.ts` from data. Use `notFound()` for missing resources so the response is a real `404`, and `redirect`/`permanentRedirect` for moves.
- Use `next/image` and `next/font`. Render JSON-LD in the page with `<script type="application/ld+json">`.
- Private layouts (dashboard, account) export `robots: { index: false, follow: false }` and are protected by the authentication guard.

### Gatsby

- Set page metadata with the Head API (`export const Head`), including canonical and Open Graph tags. Use `gatsby-plugin-sitemap`, and generate `robots.txt` at build time.
- Content comes from the GraphQL layer at build time, so it is in the static HTML. Use `gatsby-plugin-image` for images.

### Symfony and Twig

- The base layout exposes overridable blocks for `title`, `meta_description`, `canonical`, `robots`, and Open Graph tags, and each page template fills them from its data. Templates follow `html.md`.
- Throw `NotFoundHttpException` for a missing resource so the status is `404`. Redirect moved routes with a permanent redirect response.
- Generate the sitemap from the repository data (a controller or a bundle). Send `X-Robots-Tag: noindex` on non-production environments and on private routes.

## What not to do

- No keyword stuffing, hidden text, cloaking, doorway pages, or duplicated titles and descriptions.
- No `noindex` on a page that is also in `sitemap.xml`; no canonical pointing at a different page than the one a visitor should land on.
- No public content behind a login, a cookie wall, or a JavaScript-only interaction.
- No SEO change that breaks the Absolute Directive: do not add a library or abstraction for a single tag.
