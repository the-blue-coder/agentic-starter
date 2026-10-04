---
type: decision
status: accepted
date: 2026-10-04
tags: [seo, html, reviews, agent-workflows]
affects: [[Implementation workflows]]
---

## Context

Nothing in the workflow covered how search engines see a project. Agents readily ship pages without canonical URLs, with duplicate titles, client-only content, soft 404s, or links that are not links. Many products are not meant to be indexed at all (internal tools), and many are mixed: a public site next to an authenticated dashboard. A single "always check SEO" rule would be noise for the first and wrong for the second.

## Decision

Every project settles an SEO value in `.context/project-settings.md`: `yes` (the whole user-facing product), `no`, or `hybrid` (a public part, listed in `SEO public scope:`, plus a non-SEO remainder such as a dashboard). `/init-project` decides it for new projects and `/update-workflow` decides it for older ones, recommending a value from the project and asking the user. `/spec` and `/status` treat it as a required setting.

Two convention files back it. `html.md` holds HTML best practice for all markup, SEO or not, and is read wherever a UI layer is reviewed. `seo.md` holds the SEO rules (rendering, URLs, metadata, crawl control, structured data, per-stack implementation) and applies only when `SEO:` is `yes` or `hybrid`, and only to the public scope.

`/review-seo`, backed by an `seo-reviewer` subagent, runs right after `/review-performance` and before `/review-security`, which stays last and owns the handoff. It is flagged work: the project's `SEO:` setting and a per-spec `seo: true|false` frontmatter flag (set by `/spec` like `ui:`, true only when the feature touches the SEO-relevant part) decide whether any caller launches it. With `SEO: no` or `seo: false` it is never launched and never mentioned, in reports, handoff messages, or status suggestions. When launched it returns "Not applicable" silently if no in-scope file in the diff contains a page, route, template, head metadata, public markup, a URL or status change, a rendering change, sitemap/robots/i18n, or media loading. It never invents titles, descriptions, or copy: content decisions are flagged to the user. It runs in `/implement`, `/implement-queue`, `/implement-swarm`, the individual feature path, and the quick path.

## Why not something else

- **Two values, SEO or not**: rejected because a hybrid product would either be reviewed against SEO rules on its dashboard or skipped entirely on its public pages.
- **Fold SEO into `/review-performance` or `/review-changes`**: rejected because it cannot then be skipped for non-SEO projects, and it dilutes those reviews.
- **One combined `seo.md` with the HTML rules**: rejected because HTML best practice (accessibility, semantics) applies to every project, not only SEO-friendly ones.
- **Let the agent decide per diff whether SEO matters**: rejected because the review gate exists precisely so the agent does not judge; the setting, the spec flag, and a closed applicability list keep it mechanical.
- **Always launch it and let it say "Not applicable"**: rejected because the review and its mentions would clutter every pipeline report on projects and specs where SEO is irrelevant.
- **Have the reviewer write titles and descriptions**: rejected because that is copywriting, a product decision.

## Consequences

- Positive: SEO defects are caught at diff time on projects that care, at no cost on projects that do not; hybrid projects get the right scope.
- Negative / risk: one more review per iteration on SEO projects; the review cannot see real rendering or ranking, so it complements a crawler check rather than replacing it; `hybrid` depends on an accurate public scope.
- Generates: `html.md`, `seo.md`, `/review-seo` and `seo-reviewer` for Claude Code and OpenCode, new `SEO:` and `SEO public scope:` settings, and updates to `/init-project`, `/update-workflow`, the implement workflows, the entrypoint gates, and the README.
