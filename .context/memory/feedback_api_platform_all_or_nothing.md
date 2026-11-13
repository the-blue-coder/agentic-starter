---
name: feedback_api_platform_all_or_nothing
description: with Symfony, API Platform is brainstormed in /architecture and is all or nothing, never mixed with classic controllers
metadata:
  type: feedback
---

When Symfony is the backend, `/architecture` must brainstorm API Platform with the user. If it is chosen, every endpoint is an API Platform operation with no classic controller; otherwise API Platform is not installed at all.

**Why:** the user strongly dislikes a mixed backend ("pas de controlleur classique, sinon j'aime pas du tout") and wants the choice made deliberately at architecture time, not defaulted. See [[feedback_stacks_not_kept_in_project]].

**How to apply:** never add a `Controller/` or `#[Route]` action in an API Platform project; model health checks, webhooks and tracking as API Platform resources with providers and processors.
