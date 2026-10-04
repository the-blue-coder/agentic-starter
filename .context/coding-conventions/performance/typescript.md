# Performance - TypeScript

- Run independent awaits together with `Promise.all`; never `await` them in sequence or inside a `for` loop when they do not depend on each other.
- Build a `Map`/`Set`/record keyed by id once, then look up - never `find`/`includes`/`indexOf` inside a loop over another collection.
- Chain `filter`/`map`/`reduce` only on small collections; for large ones, make one pass.
- Import narrowly (`import { fn } from "lib/fn"`), never a whole library for one function, and never a barrel that drags the module graph into a client bundle.
- Hoist constants, regular expressions, and formatters (`Intl.*`) out of functions that run repeatedly.
- Release what you open: remove event listeners, clear timers and intervals, abort in-flight `fetch` with `AbortController` on teardown.
- Stream or batch large payloads; select only the fields you need from API responses and database rows.
