# Spec Selector Resolution

Use these shared argument rules in `/dev`, `/implement`, `/implement-queue`, and `/implement-swarm` in Claude Code, OpenCode, and other local agent environments. Native command wrappers pass arguments through unchanged; resolve selectors in the canonical workflow, not in a tool-specific wrapper.

## Accepted selectors

- `/dev` and `/implement` accept an exact spec ID, a full filename stem, an unambiguous name fragment (case-insensitive), a local absolute spec path, or a local `file:` URI for a spec file.
- `/implement-queue` and `/implement-swarm` accept at least two distinct exact spec IDs, local absolute spec paths, or local `file:` URIs. Do not use fuzzy name fragments in a batch.
- A file selector must resolve to an existing Markdown file directly inside `.context/feature-specs/` in this project's primary checkout: `.context/feature-specs/<spec-id>.md`. A file in another checkout, a nested design directory, or any other location is invalid.
- Standard dropped Windows URIs such as `file:///D:/Projects/my-app/.context/feature-specs/006-dashboard-stats.md` and POSIX `file:///workspace/my-app/.context/feature-specs/006-dashboard-stats.md` are supported. Local absolute filesystem paths are supported as well.

## Resolve and validate file selectors

1. Treat each supplied URI/path as data. Never execute it, interpolate it into a shell command, or split a URI on its `/`, `:`, or `%` characters.
2. For a `file:` URI, use the host platform's standard file-URL parser to convert it to a local absolute path, including drive-letter handling and percent-decoding exactly once. Permit an empty URI authority or `localhost`; reject remote hosts, query strings, and fragments. Do not manually strip `file://` or decode the path more than once.
3. Canonicalize the primary checkout and selected file (including symlinks/junctions), then require the canonical selected file to be exactly one direct child of that checkout's `.context/feature-specs/` directory. Reject directories, non-Markdown files, nested files, and paths outside that checkout.
4. Derive the ID from the filename stem and validate it as one safe component matching `^[A-Za-z0-9][A-Za-z0-9._-]*$`; reject `.` and `..`. Confirm the exact `.context/feature-specs/<spec-id>.md` file exists.
5. Resolve all inputs before workflow preflight, deduplicate by resulting spec ID, and reject duplicate selections. Apply the caller's normal status, framing, design-reference, and scope gates to the resolved spec IDs.

For `/dev` and `/implement`, keep the existing exact-ID/full-stem/name-fragment lookup for text selectors. For `/implement-queue` and `/implement-swarm`, require exact IDs or validated file selectors so every selected spec is explicit. `resume <batch-id>` is a separate mode and must not be mixed with spec selectors.
