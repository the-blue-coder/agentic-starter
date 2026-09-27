---
type: decision
status: accepted
date: 2026-09-27
tags: [symfony, domain-modeling, conventions]
---

# Keep domain behavior with its owning objects

## Context

The Symfony conventions described services as the place for business logic. That wording can encourage procedural code which reads an entity's state, makes a decision outside it, and changes it through setters. It also obscures the separate roles of domain objects, application services, repositories, and HTTP adapters.

## Decision

An entity or value object owns invariants and state transitions over its own data; application services orchestrate use cases, transactions, cross-object coordination, and external effects.

## Why not something else

- **Put every business rule in a service**: rejected because rules about one object's state can become duplicated across callers and leave the object unable to protect its own invariants.
- **Put every workflow in an entity**: rejected because coordination across objects, transactions, persistence, and external systems does not belong in one entity.
- **Treat Tell Don't Ask as a ban on getters or services**: rejected because callers still need read access, and focused application or domain services remain useful where responsibilities span objects or systems.

## Consequences

- Positive: each object's state transitions have one clear owner and are reusable across entry points.
- Positive: services have a narrower, visible role in coordinating use cases instead of collecting unrelated rules.
- Negative / risk: domain objects may gain methods as their responsibilities become explicit; keep them cohesive and move cross-object or I/O work to services.
- Negative / risk: concurrent writes still require appropriate transaction and locking strategies outside the in-memory domain method.
