# UI / UX

### Primitives - shadcn/ui

- Always use **shadcn/ui** for UI primitives (Button, Input, Dialog, Select, etc.) - never build them from scratch.
- Add via CLI: `pnpm dlx shadcn@latest add <component>`.
- shadcn/ui components live in `src/components/ui/` - committed to the repo, edit freely to match the design.
- After `pnpm dlx shadcn@latest add <component>`, reformat the generated file to the project's conventions: convert 2-space indentation to tabs, and convert every `function ComponentName(...) {...}` declaration to `const ComponentName: React.FC<React.ComponentProps<"div">> = ({ className, ...props }) => {...};` (`React.FC` is mandatory, like for any other component; adapt the props type to the primitive it wraps). Keep the file's named multi-export structure as-is (`export { Foo, Bar, ... }`) - never force a single `export default` or split the file, since shadcn intentionally bundles several related sub-components per file.

### Icons - lucide-react

- Always use **lucide-react** - never inline SVGs or other icon libraries.
- Import individually: `import { Home, Settings } from "lucide-react"`.
- When lucide has no icon for the need (or its drawing does not fit, e.g. a check inside a cloud), build **our own lucide icon** with `createLucideIcon(name, iconNode)` from `lucide-react`, one file per icon in `lib/icons/` (for example `CloudSavedIcon.ts`). It then takes `size`, `className`, color and stroke like any lucide icon. Never inline an `<svg>` in a component, never put an icon drawing in `public/` or behind a CSS mask.
- Size/color via props or Tailwind (e.g. `size={16}`, `className="text-primary"`) - never inline `style={{...}}`.

### Animations - framer-motion

- Use **framer-motion** for all animations (page transitions, list item enter/exit, modals, micro-interactions).
- Prefer `motion.*` components over CSS transitions for anything interactive or sequenced.
- Keep animations subtle - avoid decorative motion that slows the UI.

### Global CSS defaults

```css
* {
    user-select: none;
}

input, textarea {
    user-select: text;
}
```

---

## UI Patterns

### Delete confirmation modals

- Always reuse generic `<DeleteModal>` - never one-off inline modals.
- Props: `isOpen`, `onClose`, `onConfirm`, `isDeleting`, `title`, optional `entityName`, `error`.

### Pending state on list/grid rows

- Any row with an in-progress API call: `pointer-events-none opacity-40`.
- Track with `Set<string>` state (`pendingIds`) - add before call, remove in `finally`.
- For add actions: boolean `isAdding`, disable the trigger button.

### Submit button loading state - never a spinner

Form submit buttons must **never render a spinner** while submitting. Disabled state via reduced opacity - label stays unchanged.

```tsx
// ❌ wrong
<Button type="submit" disabled={isSubmitting}>
    {isSubmitting ? <Loader2 className="animate-spin" /> : "Save"}
</Button>

// ✅ correct
<Button type="submit" disabled={isSubmitting || isNavigating}>
    Save
</Button>
```

`isNavigating` is true while a post-submit redirect is in flight (e.g. `router.push` called after a successful submit). Include it in the disabled condition only for forms that navigate on success; omit it otherwise.

### Loading state on non-form interactive elements

Any non-`<button>` clickable (span, div, anchor) triggering an async action needs both:
- `pointer-events-none opacity-40` Tailwind classes
- `onClick={!isLoading ? handleX : undefined}`

```tsx
// ❌ wrong
<span onClick={handleNoThanks} className="cursor-pointer underline">No, thanks</span>

// ✅ correct
<span
    onClick={!isSubmitting ? handleNoThanks : undefined}
    className={`underline ${isSubmitting ? "pointer-events-none opacity-40" : "cursor-pointer"}`}
>
    No, thanks
</span>
```

### Sidebar active state

Use `isNavActive(href)` from `useDashboardLayout` - highlights on exact match AND any sub-path. Exception: `/dashboard` uses exact match only.

### Account navigation - account menu in the app, session-aware public header

Any project with accounts treats the session the same way in both headers:

- **App header (signed in):** the user's account is one round avatar button at the top right showing the initial of their email (or name), like GitHub. It opens a dropdown menu (shadcn `DropdownMenu`) with the email as a non-interactive first line, then Settings, then Sign out. Never lay the email, a Settings link and a Sign out button side by side in the bar. The avatar button carries an `aria-label` (for example "Account"), and sign-out is a menu item calling the sign-out action.
- **Public header (marketing pages, homepage):** read the session in the public layout (server side) and pass `isSignedIn` down. Signed out shows "Sign in" and the waitlist or sign-up call to action; signed in replaces both with a single "Dashboard" link to the app home. A visitor who is already connected is never offered to sign in or join again.

### Links - never inert after a click

A click on an internal link must give feedback at once: the app never feels frozen while the next page loads.

- Use the shared `Link` primitive (`components/ui/link.tsx`, wrapping `next/link`) for every internal navigation link (back links, logo, navbar, call to action, auth pages, not-found). On a plain click it navigates in a transition (`usePendingNavigation(href)`, a `useTransition` plus `router.push`) and, while the page opens, dims (`opacity-50`), ignores clicks (`pointer-events-none`) and sets `aria-disabled`. A click with a modifier key keeps the browser behavior (new tab).
- Never import `next/link` directly for an internal link. Exceptions: a link opening a new tab (`target="_blank"`), and a component that already owns a pending state with `usePendingNavigation` (for example a card that dims as a whole).
- A menu trigger (avatar, dropdown) is a button, not a link: it opens its menu at once and gets no pending state. A navigation item inside the menu is pending: keep the menu open (`closeOnClick={false}`) until the page changes so the dimmed item is visible, then close it.
- In Jest, `next/navigation` has no router context: mock `useRouter` and `usePathname` once in `tests/setup.ts`.

### Numeric inputs - always use `<NumberInput>`

Never use a raw `<Input type="number">`. Always use `<NumberInput>` from `src/components/ui/NumberInput.tsx`.
- Formats in French locale with non-breaking space separators (`12 345`) live during typing.
- Wire via `Controller` from react-hook-form.
- Integers only. If decimals are needed, extend the component.

### Date inputs - always use `<DatePickerInput>`

Never use `<Input type="date">` or any raw date input. Always use `<DatePickerInput>` from `src/components/ui/DatePickerInput.tsx`.

- `value`: `YYYY-MM-DD` string (or empty string)
- `onChange(value: string)`: called with `YYYY-MM-DD` on selection, closes the popover automatically
- `todayLabel`: translated label for the "Today" shortcut button (shown at the bottom of the calendar popover)
- `placeholder`, `disabled`, `className`: optional
- Trigger displays the date as `DD MMM YYYY`; shows `text-muted-foreground` when empty
- Internally uses `moment` for parsing and formatting

```tsx
<DatePickerInput
    value={values.date ?? ""}
    onChange={handleDateChange}
    todayLabel={t("today")}
/>
```

### Select - full-width dropdown

When a `<Select>` sits inside a table cell or a fixed-width container and the dropdown must fill exactly the same width as the trigger, pass `position="popper"` to `<SelectContent>`. Radix then exposes `--radix-select-trigger-width` and the component applies `w-(--radix-select-trigger-width)` automatically.

```tsx
// ✅ dropdown matches trigger width
<SelectContent position="popper">…</SelectContent>

// default - dropdown sizes to its content
<SelectContent>…</SelectContent>
```

`SelectItem` uses symmetric horizontal padding (`px-2`) and `justify-center` by default. The check icon is absolutely positioned so it never shifts the text.

### Select - native `<select>`: always draw the chevron yourself

The default dropdown is the shadcn `Select` (Radix): its trigger holds its own chevron, so the spacing is the same everywhere and nothing more is needed. A project may instead choose a **native** `<select>` (better keyboard and mobile behavior). The browser chevron of a native select sits at a different distance from the border in each browser and OS, so two dropdowns never line up. In that case, never write a raw `<select>`: every native select goes through one shared `Select` primitive, which:

- hides the browser chevron (`appearance-none`) and reserves room for it (right padding larger than the left one);
- draws a lucide `ChevronDown` (`size-4`, `pointer-events-none`, vertically centered) at a **fixed distance from the right border**, the same for every dropdown of the project;
- applies `className` (width, margin) to a `relative` wrapper and `selectClassName` to the `<select>` itself, and dims the icon with the select when it is disabled (`peer-disabled:`).

```tsx
// ❌ wrong: raw select, the chevron position depends on the browser
<select className="w-full px-4 py-3 border">…</select>

// ✅ correct: shared primitive, chevron at a fixed distance from the border
<Select className="max-w-sm" selectClassName="font-serif">…</Select>
```

### External links - always show the external icon

A link that opens another site or the user's public page in a new tab (`target="_blank"`) shows a lucide `ExternalLink` icon (`aria-hidden`, `size-3.5`) right after its label, with `rel="noopener noreferrer"`. Put the icon in the shared link component, always on, so every such link (header, prose, buttons) gets it without a per-call prop.

### Time inputs - always use `<TimePickerInput>`

Never use `<Input type="time">` or any raw time input. Always use `<TimePickerInput>` from `src/components/ui/TimePickerInput.tsx`.

- `value`: `HH:MM` string (or empty string)
- `onChange(value: string)`: called with `HH:MM`; selecting a minute auto-closes the popover
- `nowLabel`: translated label for the "Now" shortcut button (shown at the top of the popover)
- `placeholder`, `disabled`, `className`: optional
- Popover fills the trigger width (`w-(--radix-popover-trigger-width)`); hour/minute columns each take `flex-1`
- Reopening scrolls to the current selection; trigger shows `text-muted-foreground` when empty

```tsx
<TimePickerInput
    value={values.startTime ?? ""}
    onChange={handleStartTimeChange}
    nowLabel={t("now")}
/>
```

### Typography - never use `font-mono` for display values

Never apply `font-mono` to dates, times, durations, amounts, or any user-facing numeric/temporal value. `font-mono` is reserved for actual code snippets or technical tokens (e.g. UUIDs, code blocks).

---

### Secret inputs - a stored value shows `**********` as placeholder

A field for a write-only secret the server keeps (API key, access token, webhook secret) never shows the stored value, but it must show that one IS stored: while a value is set, the field's `placeholder` is `**********` (one shared constant, for example `SECRET_PLACEHOLDER` in the shared constants); while none is set, it has no such placeholder. The field value itself stays empty (never prefilled, not even masked), `type="password"`, `autoComplete="off"`; typing a new value replaces the stored one, and saving clears the field again. A status label ("Set" / "Not set", or the last four characters) can sit next to it, but never replaces the placeholder. The component test asserts the placeholder in both states.

```tsx
// ❌ wrong - an empty field reads as "nothing saved" although a key is stored
<Input type="password" {...register("key")} />

// ✅ correct
<Input autoComplete="off" placeholder={isSet ? SECRET_PLACEHOLDER : undefined} type="password" {...register("key")} />
```

## Quick Reference

| You're about to... | Instead |
|---|---|
| Build a Button / Dialog / Select from scratch | `pnpm dlx shadcn@latest add <component>` |
| Inline SVG icon | `import { X } from "lucide-react"`, or `createLucideIcon` in `lib/icons/` when lucide has no fitting icon |
| Non-button clickable with async action | `pointer-events-none opacity-40` + `onClick={!isLoading ? handleX : undefined}` |
| `<Input type="date">` | `<DatePickerInput>` |
| `<Input type="time">` | `<TimePickerInput>` |
| SelectContent dropdown width ≠ trigger | Add `position="popper"` to `<SelectContent>` |
| Raw native `<select>` (project that chose native selects) | Shared `Select` primitive: chevron drawn at a fixed distance from the right border |
| Email + Settings + Sign out laid out in the app header | One avatar button (initial) opening a dropdown: email, Settings, Sign out |
| "Sign in" / "Join the waitlist" shown to a signed-in visitor on a public page | Read the session in the public layout and show a single "Dashboard" link |
| `<Link>` from `next/link` for an internal navigation | `Link` from `components/ui/link.tsx` (dims and disables itself while the page opens) |
| Link opening a new tab | `target="_blank"` + `rel="noopener noreferrer"` + `ExternalLink` icon after the label |
| Empty secret field (API key, token) while a value is stored | `placeholder="**********"` (shared `SECRET_PLACEHOLDER`), field value still empty |
