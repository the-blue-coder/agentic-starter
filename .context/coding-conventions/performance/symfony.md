# Performance - Symfony

Applies on top of `php.md` in this folder.

## Doctrine

- **N+1**: a relation read inside a loop or a Twig/serializer iteration triggers one query per item. Fetch with a `JOIN ... addSelect` (or a dedicated repository method) so the collection loads once. Only join-fetch what the use case reads.
- **Indexes**: add `#[ORM\Index]` (and a migration) for every new column used in `WHERE`, `ORDER BY`, or join conditions on a growing table. Foreign keys are indexed; confirm composite filters have a matching composite index.
- **Projections**: read-only lists, exports, and dashboards select the columns they need (`SELECT NEW`, scalar/array hydration), not full entities.
- **Large sets**: use `toIterable()` or paginated batches, and call `clear()` between batches in long loops; never `findAll()` on a table that grows.
- **Batch writes**: one `flush()` after the loop, not one per entity; for bulk updates and deletes use a DQL/SQL statement instead of loading each entity.
- **Counting and existence**: `COUNT(*)`/an `EXISTS` query, never loading entities to call `count()` on the result.
- Keep queries in repositories (see `symfony.md`); fix a slow query in the repository method once, not per caller.

## API Platform

- Paginate every collection operation and cap the maximum items per page.
- Restrict serialization groups to fields consumers need; avoid embedding large relations by default.
- Filters on large tables must hit an index.

## Request path

- Slow work (email, PDF, third-party calls, imports) goes through Symfony Messenger, not inline in a controller or listener.
- Cache stable, expensive reads with the Cache component (explicit key and TTL); do not cache per-user data under a shared key.
- Avoid heavy work in event listeners that run on every request (`kernel.request`/`kernel.response`).
