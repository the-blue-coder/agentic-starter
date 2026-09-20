# Twig

- **Void elements**: always self-close with ` />` - `<link ... />`, `<img ... />`, `<input ... />`, `<meta ... />`, `<hr />`, `<br />`. Never leave them unclosed (`<link ...>`, `<img ...>`).
- Use `getParam('appName')` to display the app name - never hardcode "OAI Armarium" in templates.
- Theme class is set on `<body>`: `{{ themeClass|default('theme-blue') }}`.
- **Variable names**: always use the full, explicit name - no abbreviations. `{% set setCouleur = ... %}` not `{% set sc = ... %}`. A reader should understand the variable without context.
- **Sections**: every conceptual section inside a `<main>` must use a `<section>` element, not a `<div>`.

## Indentation

Indent the body of every nested tag (`{% if %}`, `{% else %}`, `{% for %}`, `{% block %}`, ...) one level deeper than the tag itself, exactly like nested HTML. Never leave nested content flush left against the tag.

```twig
{% if results is empty %}
    No non-archived clients to process.
{% else %}
    {% for result in results %}
        {{ result.clientName }}: {{ result.status }}{% if result.invoiceNumber %} ({{ result.invoiceNumber }}){% endif %}{% if result.reason %} - {{ result.reason }}{% endif %}
    {% endfor %}
{% endif %}
```

Not:

```twig
{% if results is empty %}
No non-archived clients to process.
{% else %}
{% for result in results %}
{{ result.clientName }}: {{ result.status }}{% if result.invoiceNumber %} ({{ result.invoiceNumber }}){% endif %}{% if result.reason %} - {{ result.reason }}{% endif %}
{% endfor %}
{% endif %}
```

## Partials

Shared partials live in `templates/partials/`, grouped into sub-folders **by component type** rather than as a flat list. Folder names are the plural type, e.g. `badges/`, `buttons/`, `cards/`, `content/`, `feedback/`, `fonts/`, `headings/`, `images/`, `navigation/`, `sections/`. Add a new type folder when none fits.

- Include with the full path: `{% include 'partials/buttons/button.html.twig' %}`.
- **Never prefix a partial's filename with `_`** (`_button.html.twig`) - the `partials/` directory location is what signals "this is a partial, not a directly-rendered page," so the filename itself stays plain (`button.html.twig`).
- **Include formatting**: when passing parameters, always use multi-line layout — never inline:
  ```twig
  {% include 'partials/buttons/button.html.twig' with {
      label: 'Click me',
      classes: 'bg-theme text-white'
  } %}
  ```
- A partial never owns its `<section>` wrapper - the caller provides it.
- **Partial docblock**: use a `{# ... #}` comment at the top listing params. Do not align param names/types with extra spaces — one space between each column only.
- Parameterise visual variants through **complete class strings** (`bg_color`, `border_color`, `classes`, ...) with sensible `|default(...)` values - never assemble class names by concatenation, so Tailwind can detect every utility. `partials/buttons/button.html.twig` and `partials/badges/badge.html.twig` are the canonical examples.

## Font bootstrap

Font loading lives in a single block inside `base.html.twig`, delimited by `{# Font bootstrap #}` / `{# End of font bootstrap #}` comments: one `<link rel="preload" />` per font file, one inline `<style>` block with all `@font-face` declarations, then the visibility-trigger `<script>` - in that exact order. See `/add-new-font` for the full structure and the procedure for adding or replacing a font pair.

`@font-face` declarations stay inline in that block, not in `app.css`. Reason: `app.css` is loaded via importmap (JS) and is parsed after the DOM, so the browser doesn't know about the fonts until too late - inline `<style>` is parsed immediately.

Every declared font file also gets a `<link rel="preload" />` so the browser fetches all font files at maximum priority from the very start of `<head>` parsing. AssetMapper fingerprints the URLs via `asset()`, so they are cached aggressively (`Cache-Control: immutable`) on repeat visits.

The visibility script prevents fallback-font flash by hiding the page until `document.fonts.ready` resolves. `requestAnimationFrame` defers the check until after the first layout pass, by which point the browser knows exactly which font weights are needed for the current page; `setTimeout(3000)` is a safety fallback in case a font file fails to load.

Do not reorder the three parts, and do not split them out of `base.html.twig` into separate partials - see `/add-new-font` and the comment block in `base.html.twig` itself for why.
