# Performance - Stimulus

Applies on top of `javascript.md` in this folder.

- Anything a controller attaches in `connect()` is removed in `disconnect()`: listeners (`addEventListener`), timers, observers (`IntersectionObserver`, `ResizeObserver`, `MutationObserver`), and in-flight `fetch` (abort it). Controllers are connected and disconnected as Turbo swaps the DOM, so a leak compounds with each navigation.
- Prefer Stimulus `data-action` over manual listeners; it is cleaned up for you and delegates efficiently.
- Debounce or throttle actions bound to `input`, `scroll`, and `resize`.
- Query targets through Stimulus `targets`, not repeated `document.querySelector` calls; cache what you read in `connect()`.
- Keep `connect()` cheap: defer heavy setup until first interaction, or load heavy libraries with a dynamic `import()` so pages that do not use the controller do not pay for it.
- `valueChanged` callbacks run on every change - keep them idempotent and free of DOM thrashing; batch DOM reads and writes.
