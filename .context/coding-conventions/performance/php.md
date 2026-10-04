# Performance - PHP

- Never run a query or HTTP call inside a loop; collect ids, fetch once, then index the result by id.
- Do not load a whole table or large result into an array; iterate with a cursor/`iterable`, `yield`, or batches (`array_chunk`, query limits) and free what you are done with.
- Look up by key (`isset($map[$id])`), never `in_array`/`array_search` inside a loop over another array.
- Avoid building strings with repeated concatenation in large loops; collect parts and `implode` once.
- Hoist invariant computation (`count()`, regexes, config reads) out of loops.
- Open files and streams only as long as needed and close them; read large files line by line rather than `file_get_contents`.
- Slow work (mail, PDF/report generation, third-party calls) does not run inline in a request when the project has an async mechanism; see `symfony.md` for that stack's option.
