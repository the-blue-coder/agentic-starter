# HTML

> Applies to every markup this project outputs: Twig templates, JSX/TSX, and static HTML. These are good practices in their own right and the foundation of `seo.md`: search engines read the HTML the server sends, so correct markup is the cheapest SEO there is. Accessibility follows from the same rules.

## Document

- Start with `<!doctype html>` and set `<html lang="...">` to the page's real language. Use `<meta charset="utf-8">` and `<meta name="viewport" content="width=device-width, initial-scale=1">` (never disable zoom).
- Exactly one `<title>` per page, in `<head>`, unique and descriptive (rules in `seo.md`).
- Page regions use landmarks, once each where applicable: `<header>`, `<nav>`, `<main>` (exactly one), `<aside>`, `<footer>`. Several `<nav>` elements get an `aria-label`.

## Headings

- Exactly one `<h1>` per page, describing it. Levels descend without skipping (`h1` → `h2` → `h3`); never choose a level for its size - style it with CSS.
- Headings form the page outline: someone reading only the headings should understand the page.

## Semantic elements over generic ones

Use the element that means what the content is; `<div>` and `<span>` are the last resort.

| Content | Element |
| --- | --- |
| Standalone piece (post, card, product) | `<article>` |
| Thematic group with a heading | `<section>` |
| Image with a caption | `<figure>` + `<figcaption>` |
| Date or time | `<time datetime="...">` |
| Navigation links | `<nav>` with a `<ul>` of `<a>` |
| Lists | `<ul>`, `<ol>`, `<dl>` - never lines separated by `<br>` |
| Tabular data | `<table>` with `<caption>`, `<th scope>` - never for layout |
| Actions that do something on the page | `<button type="button">` |
| Emphasis, importance | `<em>`, `<strong>` - never for styling only |
| Quotes | `<blockquote>`, `<q>`, with `<cite>` when sourced |

## Links

- Navigation is a real `<a href="...">` with a crawlable URL. Never a `<div>` or `<button>` with a click handler, `href="#"`, or `javascript:` for something that goes to another page.
- Anchor text describes the destination ("Read the pricing guide"), never "click here" or "read more" alone.
- External links opened in a new tab carry `rel="noopener"`. Mark user-generated and paid links `rel="ugc"` / `rel="sponsored"`, and links you do not vouch for `rel="nofollow"`.
- Links that look identical go to the same URL; a link that downloads a file says so in its text.

## Images and media

- Every `<img>` has an `alt`: a short description of its meaning, or `alt=""` when purely decorative. Never put keywords in `alt` that do not describe the image.
- Give every `<img>` explicit `width` and `height` (or an aspect ratio) so layout does not shift.
- Below the fold: `loading="lazy"` and `decoding="async"`. The single most important above-the-fold image (the likely LCP element): no lazy loading, and `fetchpriority="high"`.
- Serve responsive images with `srcset` and `sizes` (or `<picture>` for formats), in a modern format, with descriptive file names.
- `<iframe>` has a `title` and `loading="lazy"` unless it is above the fold. Video and audio have captions or a transcript.

## Forms

- Every control has a visible `<label for="...">` (or wraps its control). Placeholders are hints, never labels.
- Use the right `type` (`email`, `tel`, `number`, `date`), a meaningful `name`, and `autocomplete` values. Buttons declare `type` (`submit` or `button`).
- Group related controls with `<fieldset>` and `<legend>`. Errors are text associated with their field, not only a color.

## Content in the HTML

- Content users and crawlers need is in the HTML the server sends. Do not inject primary content only through JavaScript after load, and do not hide it behind interactions that never run for a crawler (tabs, accordions that fetch on click).
- Do not hide text from users to show it to crawlers, and do not stuff keywords.
- Critical content has a `<noscript>` fallback when it truly cannot be rendered on the server.

## Scripts, styles, and structure

- Scripts use `defer` (or `async` for independent ones) and never block rendering in `<head>`. Load styles in `<head>`; do not use `@import` chains.
- No inline `style` attributes or inline event handlers (`onclick`); see `javascript.md` and `stimulus.md` for behavior.
- `id` values are unique. Use classes for styling, not ids.
- Prefer native elements and attributes over ARIA; add ARIA only when no native element expresses the role, and never contradict native semantics (`<button role="link">`).
- No deprecated or presentational elements (`<center>`, `<font>`, `<b>` for layout, `<marquee>`); no empty elements used for spacing.
- Markup is valid and well-formed: elements properly nested and closed, attributes quoted. Indentation follows `twig.md` for Twig templates.
