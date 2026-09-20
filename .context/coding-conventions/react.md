# React

> Scope: `assets/react-islands/` - plain React mounted as isolated "islands" into Twig pages via the `react--island` Stimulus controller (see `architecture.md` and `.context/feature-specs/001-dashboard-tp-shell.md`). No Next.js, no App Router, no server/client component split - everything here is a regular client-rendered React component. Pairs with `.context/coding-conventions/typescript.md` for language-level rules. `portfolio-template/` is a separate Next.js project with its own toolchain and is not covered by this file.

### ⚠️ Hook/Component Split - THE MOST CRITICAL RULE

**Every component with logic/state MUST call `use[ComponentName]`.** No exceptions for complex components.

- **Hook** (`use[ComponentName]`) contains **ALL** of:
  - `useState`, `useRef`, `useCallback`, `useMemo`
  - All handlers (`handleX`, `onX`)
  - All derived `const` values (e.g. `const isEmpty = conversations.length === 0`)
  - All local constants and computed values
- **Component** contains **ONLY**:
  - `useEffect` calls (stay in the component, NOT the hook)
  - The JSX `return`
- **Every `useEffect` MUST have a `//` comment on the line above** explaining its intent. A bare `useEffect` with no comment is a convention violation.
- **Exception**: simple wrapper components (no state, no handlers, no derived values) can return JSX directly.

**Checklist - before writing/reviewing any component:**

- [ ] Component has state, handlers, or derived values? → Must call `use[ComponentName]`.
- [ ] Component just wraps JSX with props? → OK to skip hook.
- [ ] If hook exists: ZERO `const`, `let`, handler definitions in the component body.
- [ ] Only `useEffect` calls between the hook call and `return`.
- [ ] Every `useEffect` has a `//` comment above it.

```tsx
// ❌ WRONG - consts and logic in the component body
const ConversationList: React.FC<TConversationListProps> = ({ conversations }) => {
    const isEmpty = conversations.length === 0;
    const handleSelect = (id: number) => onSelect(id);
    return <ul>{isEmpty ? <EmptyState /> : conversations.map(...)}</ul>;
};

// ✅ CORRECT - everything in the hook
const ConversationList: React.FC<TConversationListProps> = (props) => {
    const { conversations, isEmpty, handleSelect } = useConversationList(props);
    return <ul>{isEmpty ? <EmptyState /> : conversations.map(...)}</ul>;
};
```

### Derived values belong in the hook, not the component

Any value derived from hook state (filtered lists, counts, booleans, formatted strings) must be computed inside the hook and returned - never derived inline in JSX or repeated across the component.

```ts
// ❌ wrong - derived inline in JSX, computed twice
{conversations.filter(c => c.unread).length > 0 && (
    <span>{conversations.filter(c => c.unread).length}</span>
)}

// ✅ correct - computed once in the hook, returned as a named value
const unreadCount = conversations.filter(c => c.unread).length;
return { ..., unreadCount };

// component just reads it
{unreadCount > 0 && <span>{unreadCount}</span>}
```

### Pure helper functions

Pure functions with no state or hook dependencies do NOT belong in a hook or a component file. Put them in `assets/react-islands/src/lib/utils.ts`.

- **Reusable across islands** → `src/lib/utils.ts` (exported).
- **Used only in one feature folder** → still `src/lib/utils.ts` if it has no dependencies; moving it inline adds noise.
- **Never** define a stateless pure helper inside a hook body or at the bottom of a component file.

```ts
// ❌ wrong - pure helper inside a component file
const ConversationThread: React.FC<...> = (...) => { ... };
const groupBySender = (messages: TMessage[]) => { ... }; // no state, no deps

// ✅ correct - in src/lib/utils.ts
export const groupBySender = (messages: TMessage[]) => { ... };
```

### State management

No client-side state library is adopted (no Redux/Zustand/TanStack Query) - each island's state lives in local `useState`/hook state, seeded from the props Twig passes in (see `architecture.md`'s React-islands section). Data fetching uses plain `fetch()` against the Symfony endpoints the island's props point to (e.g. `MessagingIsland`'s `endpoints` prop).

- **Never** fetch data the island's own props already provided on mount - seed state from props first, refresh via `fetch()`/polling afterwards, so the first render never flashes empty before the initial data arrives.
- If a future island's complexity genuinely warrants a state or data-fetching library, propose it and get explicit validation first - per `.context/coding-conventions/global.md`'s "never add a new library on your own initiative" rule. Don't reach for one preemptively.

### React component rules

- All clickable elements must have `cursor-pointer` (either via a CSS class or an inline style, consistent with the project's plain-CSS convention - see `bulma.md`).
- **Never put logic directly in JSX event attributes** - extract to a named handler: `onClick={handleClick}`, never `onClick={() => doX()}`.
- **Configuration values** (API endpoints, feature flags, current-user data): never hardcode or read them from a global - they arrive as island props from Twig (`data-react--island-props-value`), per the bridge documented in spec 001. If a value isn't already a prop, add it to the mounting template's props object rather than inventing a client-side default.

### File and folder structure

- One feature folder per island under `assets/react-islands/src/components/` (e.g. `Messaging/`), containing the top-level island component, its sub-components, and a colocated `types.ts` for types shared only within that feature.
- **A component's props type and a hook's return type are defined and exported from that component's/hook's own file - never centralized in the feature's `types.ts`.** A `TFooProps`/`TUseFooReturn` type belongs next to the thing it describes; a hook's return type is `export type TFoo = ReturnType<typeof useFoo>` at the bottom of `useFoo.ts`, not re-derived in `types.ts` by importing the hook there. Importing implementation files (hooks, components) into a `types.ts` inverts the dependency direction - `types.ts` is meant to be a leaf other files import, not something that itself depends on hooks/components. The feature's `types.ts` is reserved for types with no single owning file (e.g. a shared union/enum used across several sibling components).
- Pure helpers shared across islands: `assets/react-islands/src/lib/utils.ts` - no `utils/` subfolder.
- Every island exported from the bundle is registered in the single shared `registry` in `assets/react-islands/src/index.tsx` (see spec 001's Constraints section - one shared React runtime, one dynamic import).

### Testing

No JS/TS test runner is currently wired into `assets/react-islands/` (no Jest/Vitest in `package.json`). Per `.context/coding-conventions/global.md`, tests are only warranted for critical business logic/complex hooks - if a future hook's logic is genuinely critical enough to need one, propose adding a test runner (get explicit validation, per the library-usage rule) rather than assuming one is already available.

---

## Quick Reference

| You're about to... | Instead |
|---|---|
| Put `const`/handler in component body | Move to `use[ComponentName]` |
| `onClick={() => doX()}` inline | Named handler in hook → `onClick={handleClick}` |
| Fetch data an island prop already provided | Seed state from the prop, `fetch()` only for refresh/polling |
| Add Redux/Zustand/TanStack Query "just in case" | Plain `useState` + `fetch()` until complexity genuinely warrants a library - then propose it |
| Hardcode an API endpoint or feature flag in a component | Pass it as an island prop from Twig |
| Pure helper at the bottom of a hook/component file | `assets/react-islands/src/lib/utils.ts` |
| A clickable `<div>`/`<span>` with no pointer cursor | Add `cursor-pointer` |
