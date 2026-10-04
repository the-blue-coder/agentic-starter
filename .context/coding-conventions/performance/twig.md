# Performance - Twig

- Never trigger a query by reading a relation inside a `for` loop (lazy-loaded association per item = N+1). Make the controller or repository load what the template iterates, then iterate.
- Do not call a service or repository from a template (`render(controller(...))` per row is a sub-request per item). Pass prepared data in, or fetch once outside the loop.
- Use `{% include %}` of a partial inside a large loop sparingly; for many repeats prefer `{% embed %}`-free partials with only the variables they need (`with { ... } only`) to keep the context small.
- Cache expensive, stable fragments at the controller or response level (HTTP cache, `cache` tag) with an explicit key and TTL; never cache per-user content under a shared key.
- Load scripts with `defer`, and styles/images with explicit dimensions and `loading="lazy"` below the fold; keep assets going through the project's asset pipeline so they are versioned and compressible.
