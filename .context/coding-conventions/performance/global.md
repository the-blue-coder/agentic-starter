# Performance - global

> Read by `/review-performance` on every run, then the matching stack files in this folder. The Absolute Directive in `../global.md` still governs: simplicity first, surgical changes. Performance review targets **real, demonstrable costs introduced by the diff** - never speculative micro-optimization.

## What counts as a violation

A finding needs a concrete cost the diff introduces and a bounded fix. "Could be faster" is not a finding.

- **N+1 access**: a query or network call inside a loop, or a lazy-loaded relation touched per item. Batch, join, or eager-load instead.
- **Unbounded results**: a list endpoint, query, or render with no pagination or limit on data that grows with usage.
- **Missing index**: a new filter, sort, join, or unique lookup on a column no index covers.
- **Redundant work**: the same computation, query, or request repeated per iteration or per render when it can be hoisted or shared. Fix at the shared function, not per caller.
- **Sequential independent I/O**: awaiting calls one after another that do not depend on each other. Run them concurrently.
- **Quadratic scans**: a nested loop or repeated `find`/`includes` over collections that grow. Index by key first.
- **Whole-payload loading**: reading a full file, table, or response into memory when streaming, batching, or a projection (selecting only needed columns/fields) works.
- **Unreleased resources**: listeners, timers, subscriptions, connections, or handles opened and never closed.
- **Heavy dependency**: a new dependency pulled in for something the platform or an installed dependency already does, or imported whole when a narrow import exists. Adding a dependency stays a separate decision per `../global.md`.
- **Blocking the hot path**: slow work (email, report, file processing, third-party call) done inline in a request when the project already has an async mechanism for it.

## What is not a violation

- A `shortcut:` comment naming a ceiling and an upgrade path - an accepted, documented trade-off (see the Absolute Directive). Leave it.
- Code on a cold path (one-off scripts, admin tasks, bounded small collections) where the cost cannot grow.
- Caching, memoization, or indexing "just in case" with no measured or evident cost. Adding these without need is itself over-engineering.

## Fixing

- Apply the smallest change that removes the cost. Do not restructure layers: repository/service/hook boundaries from the stack conventions stay intact.
- A fix must preserve behavior. If a test covers the code, run it; if the fix changes a query or contract, add or adjust a test per `tdd.md`.
- When the right fix needs a product decision (pagination size, cache TTL, async queue choice), flag it with the options instead of choosing silently.
