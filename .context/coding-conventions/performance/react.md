# Performance - React

- **Stable references only where they pay off**: wrap a value or callback in `useMemo`/`useCallback` only when it feeds a memoized child, a hook dependency array, or an expensive computation. Do not memoize by reflex.
- Never create objects, arrays, or functions inline in props passed to a `React.memo` child or a context provider `value` - the memo is defeated on every render.
- Keep state as low as it can go; state lifted higher than needed re-renders the whole subtree.
- Lists: a stable, unique `key` (never the array index for reorderable data). Virtualize or paginate lists that can grow past a few hundred rows.
- Never compute derived data in render from large inputs repeatedly; derive it once in the hook (see `react.md` "Derived values belong in the hook") and memoize if costly.
- Do not fetch in an effect that re-runs every render; check the dependency array, and fetch independent data in parallel, not as a waterfall of nested components.
- Split heavy, rarely-used UI (editors, charts, modals) with `React.lazy`/dynamic import.
- Effects clean up what they start: subscriptions, timers, listeners, in-flight requests.
- Prefer images with explicit dimensions and lazy loading below the fold.
