# Performance - JavaScript

- Run independent awaits together with `Promise.all`; do not `await` in a loop when iterations are independent.
- Look up by key (`Map`/`Set`), never `find`/`includes` inside a loop over another collection.
- Read layout (`offsetHeight`, `getBoundingClientRect`) and write styles in separate batches; never interleave them in a loop (layout thrashing).
- Debounce or throttle handlers on `scroll`, `resize`, `input`, and `mousemove`; mark scroll/touch listeners `{ passive: true }` when they do not call `preventDefault`.
- Prefer event delegation on a container over one listener per item in a list.
- Every listener, timer, observer, and subscription added must be removed on teardown.
- Hoist regular expressions and constants out of hot functions; avoid re-querying the same DOM node repeatedly - cache the reference.
