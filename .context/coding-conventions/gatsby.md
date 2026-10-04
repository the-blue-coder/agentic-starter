# Gatsby

> Scope: `src/` - plain client-rendered React mounted by Gatsby (no server/client component split, no App Router). Pairs with `typescript.md` for language-level rules, `tailwind.md` for styling, and `tdd.md` for tests. Modeled on a Gatsby 5 content site fed by a Markdown CMS.

### Hooks are for reuse and non-trivial logic, not mandatory per component

Unlike Next.js here, Gatsby code does **not** require a `use[ComponentName]` hook for every stateful component. Simple local state/effects (`useState`, `useRef`, `useEffect`) may live directly in the component.

Extract a dedicated hook (`useX`) when the logic is:

- Reused across more than one component (e.g. `useMenus`, `useContentSummary`).
- Non-trivial domain logic worth naming and testing in isolation (e.g. `usePostSchema`, `useFaqSchema` building structured data).
- Large enough that pulling it out keeps the component focused on JSX.

```tsx
// ✅ simple local state - stays in the component
const PageBackground: React.FC = () => {
    const [opacity, setOpacity] = useState<number>(0);

    useEffect(() => {
        // ...
    }, []);

    return <div style={{ opacity }} />;
};
```

```tsx
// ✅ reusable/non-trivial logic - extracted to a hook
const ContentSummary: React.FC<TContentSummaryProps> = ({ contentBody }) => {
    const { extractHnsFromContentBody } = useContentSummary();
    // ...
};
```

### Pure helper functions belong in `src/utils/`

Pure functions with no state or hook dependencies do not belong inside a component or hook file. Group them by concern: `contentUtils.ts`, `dateUtils.ts`, `schemaUtils.ts`.

```ts
// ❌ wrong - pure helper inside a component file
const ContentSummary: React.FC<...> = (...) => { ... };
const titleToAnchor = (title: string) => { ... }; // no state, no deps

// ✅ correct - in src/utils/contentUtils.ts
export const titleToAnchor = (title: string) => { ... };
```

### Data flow - GraphQL + CMS content, no client state library

No client-side state library by default (no Redux/Zustand/TanStack Query). Page-level data comes from Gatsby's GraphQL layer (`src/queries/`, a template's `pageQuery`), sourced from CMS content (Markdown under `content/`). Component-local UI state (toggle, hover, scroll position) uses plain `useState`.

- If a feature's complexity genuinely warrants a state or data-fetching library, propose it and get explicit validation first - per `global.md`'s "never add a new library on your own initiative" rule.

### React component rules

- **Never put logic directly in JSX event attributes** - extract to a named handler: `onClick={handleToggle}`, never `onClick={() => setOpenIndex(i)}`.
- CMS-authored raw HTML (`dangerouslySetInnerHTML`, `rehypeRaw` through a Markdown renderer) is a deliberate, reviewed pattern - see `security.md` before adding a new raw-HTML render path or wiring one to non-CMS input.
- Static assets are imported directly (`import img from "../images/x.jpg"`) - Gatsby's webpack pipeline handles them; never reference `src/images/` by string path.

### File and folder structure

- `src/components/` - reusable UI components.
- `src/common/` - shared layout-level components (`Header.tsx`, `Footer.tsx`).
- `src/layouts/` - page layout wrappers.
- `src/pages/` - file-based routes.
- `src/templates/` - Gatsby page templates, wired to routes in `gatsby-node.ts`.
- `src/hooks/` - custom hooks, one per file, named `use[Thing].ts`.
- `src/utils/` - pure helper functions, grouped by concern.
- `src/queries/` - shared GraphQL query fragments.
- `src/constants/` - app-wide constants (app details, metadata, schema defaults).
- `src/types/` - shared types; a component's own props type stays in its own file.
- `src/config/` - third-party configuration (cookie consent, analytics).
- Component styles: Tailwind utility classes by default; a co-located `Component.module.css`/`.module.scss` only for what Tailwind cannot express.

### Testing

TDD (`.context/coding-conventions/tdd.md`) applies to hooks and `src/utils/` helpers, with the test tool recorded in the `## Testing` section of `.context/architecture.md`. A Gatsby project has no test runner until `/architecture` records one; propose it there (explicit validation required) rather than assuming one is available. Pure presentational components, `gatsby-*.ts` configuration, and GraphQL fragments are verified by running the build.

---

## Quick Reference

| You're about to... | Instead |
|---|---|
| Extract every stateful component into a `use[Component]` hook | Only extract when the logic is reused or non-trivial - simple local state can stay in the component |
| `onClick={() => setOpenIndex(i)}` inline | Named handler: `onClick={handleToggle}` |
| Pure helper at the bottom of a component/hook file | `src/utils/<concern>.ts` |
| Add Redux/Zustand/TanStack Query "just in case" | Plain `useState` + Gatsby GraphQL until complexity genuinely warrants a library - then propose it |
| Reference `src/images/x.jpg` by string path | `import x from "../images/x.jpg"` |
| Add a new `dangerouslySetInnerHTML`/raw-HTML path | Check `security.md` first - confirm the source is CMS-authored, trusted content |
