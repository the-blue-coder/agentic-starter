# Performance - Symfony

Applies on top of `php.md` in this folder.

## Doctrine

- **N+1**: a relation read inside a loop or a Twig/serializer iteration triggers one query per item. Fetch with a `JOIN ... addSelect` (or a dedicated repository method) so the collection loads once. Only join-fetch what the use case reads.
- **Indexes**: add `#[ORM\Index]` (and a migration) for every new column used in `WHERE`, `ORDER BY`, or join conditions on a growing table. Foreign keys are indexed; confirm composite filters have a matching composite index.
- **A paginated list sorts on plain columns its index covers**: never a `CASE`, `COALESCE` or other expression in `ORDER BY` (for example "rows without a date last"), which no index serves, so every page sorts the whole set. Store the order in a never-null column instead (for example `sort_at`, set to the epoch while there is no date), with a composite index on the filter and the sort columns (`owner_id, sort_at, id`), and check with `EXPLAIN` that the plan walks the index (no `Sort` node).

```php
// ❌ wrong - the expression forces a sort of every matching row
->addSelect('CASE WHEN item.lastActivityAt IS NULL THEN 1 ELSE 0 END AS HIDDEN withoutActivity')
->orderBy('withoutActivity', 'ASC')->addOrderBy('item.lastActivityAt', 'DESC')

// ✅ correct - a never-null column, indexed with the filter: #[ORM\Index(columns: ['owner_id', 'sort_at', 'id'])]
->orderBy('item.sortAt', 'DESC')->addOrderBy('item.id', 'DESC')
```
- **Projections**: read-only lists, exports, and dashboards select the columns they need (`SELECT NEW`, scalar/array hydration), not full entities.
- **Large sets**: use `toIterable()` or paginated batches, and call `clear()` between batches in long loops; never `findAll()` on a table that grows.
- **Batch writes**: one `flush()` after the loop, not one per entity; for bulk updates and deletes use a DQL/SQL statement instead of loading each entity.
- **Counting and existence**: `COUNT(*)`/an `EXISTS` query, never loading entities to call `count()` on the result.
- Keep queries in repositories (see `symfony.md`); fix a slow query in the repository method once, not per caller.

## API Platform

- Paginate every collection operation and cap the maximum items per page.
- Restrict serialization groups to fields consumers need; avoid embedding large relations by default.
- Filters on large tables must hit an index.

## FrankenPHP

- If worker mode is enabled, the application stays in memory between requests: never keep per-request state in static properties, globals, or singletons that are not reset between requests, and release large objects and open handles when a request ends. A leak grows until the worker restarts.
- Keep OPcache and `apcu` enabled in production images, and compile the prod container (`cache:warmup`) at build time rather than on first request.
- Compression (`encode zstd br gzip`) and HTTP/2 or HTTP/3 are handled by the Caddy layer; do not re-implement them in PHP.

## Request path

- Slow work (email, PDF, third-party calls, imports) goes through Symfony Messenger, not inline in a controller or listener.
- **A job that can wait long on an outside service (an AI or LLM call, an export) runs on its own transport and its own worker**, never in the worker that consumes the fast queues (inbound events, sends): one slow message would hold every message behind it. Each worker lists only its transports in its `messenger:consume` command, and the deploy restarts every worker.
- Cache stable, expensive reads with the Cache component (explicit key and TTL); do not cache per-user data under a shared key.
- Avoid heavy work in event listeners that run on every request (`kernel.request`/`kernel.response`).
