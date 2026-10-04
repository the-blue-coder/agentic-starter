# Performance - Next.js

Applies on top of `react.md` and `typescript.md` in this folder.

- **Default to Server Components.** Every `"use client"` boundary ships JavaScript; push it to the smallest leaf that needs interactivity instead of marking a whole page or layout.
- **No request waterfalls**: in Server Components fetch independent data with `Promise.all`, or stream slow parts behind `<Suspense>`. Do not await one fetch before starting the next when they are independent.
- **TanStack Query (client pages)**: reuse one query key per resource so results are shared and deduplicated; set `staleTime` deliberately for data that does not change per second; use `select` to avoid re-rendering on unrelated fields; invalidate the narrowest key that is stale (see `nextjs.md` "Cache invalidation").
- Native `fetch` in Server Components: state caching intent explicitly (`cache`/`next.revalidate`) rather than relying on defaults for data that is stable or per-user.
- Use `next/image` (dimensions, `priority` only for the above-the-fold image, `sizes` for responsive) and `next/font`; never raw `<img>` or a `<link>` to a font CDN.
- Use `next/dynamic` for heavy client-only components (charts, editors, maps); keep them out of the initial bundle.
- Import narrowly from large libraries; never import a server-only or heavy module into a client component.
- Pagination or cursor limits on every list route and query hook; never return an unbounded collection to the client.
- Zustand: select the slice you need (`useStore((s) => s.x)`), never the whole store, to avoid re-rendering on unrelated changes.
