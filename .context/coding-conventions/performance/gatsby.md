# Performance - Gatsby

Applies on top of `react.md` and `typescript.md` in this folder.

- **Query only the fields you render.** A page or static query that selects whole nodes bloats page data; list the fields. Limit and paginate list queries (`limit`/`skip`) instead of loading every node.
- Images go through `gatsby-plugin-image` (`GatsbyImage`/`StaticImage`) with `loading="lazy"` below the fold and `loading="eager"` only for the above-the-fold hero; never raw `<img>` for CMS or local images.
- Prefer `StaticQuery`/`useStaticQuery` for small shared data and page queries for per-page data; do not duplicate the same query across components - share one hook in `src/queries/`.
- Heavy client-only widgets (maps, embeds, editors): load with `React.lazy` or on interaction, and guard browser APIs so they never run during SSR/build.
- Build-time work belongs in `gatsby-node` (page creation, data shaping); do not repeat it in components at runtime.
- Do not add a client-side data fetch for content that is available at build time through GraphQL.
- Fonts: self-host and preload the critical font; avoid render-blocking third-party stylesheets and scripts (load third-party scripts deferred or via `Script`).
