# Symfony

### Repositories, domain objects, and services

Keep each responsibility with the object that owns it:

- **Repositories** own Doctrine reads and queries. They return entities or projections; they do not decide domain state transitions.
- **Entities and value objects** enforce invariants over their own state. Give them intention-revealing methods such as `withdraw()` or `publish()` rather than making callers inspect values, branch on them, and update them through setters.
- **Application services** coordinate a use case: load objects through repositories, invoke their domain methods, coordinate multiple objects or external systems, and manage transaction/persistence boundaries such as `persist()` and `flush()`. They are not a catch-all for rules an entity can enforce itself.
- A **domain service** is appropriate for a domain rule that genuinely spans multiple objects and has no natural owner. Keep it focused; do not create one just to move a conditional out of a controller.
- Never put `createQueryBuilder`, `findBy`, raw SQL, or `getRepository` inside a service. **Always inject repositories via the constructor** - never `$this->em->getRepository(Foo::class)`.
- Do not make entities query repositories, flush, or call external systems. When concurrent updates could violate an invariant, protect the use case with the appropriate transaction and locking strategy as well; an entity method alone does not prevent a database race.

```php
// ❌ wrong - the caller owns the account's rule and transition
if ($account->getBalanceCents() >= $amountCents) {
    $account->setBalanceCents($account->getBalanceCents() - $amountCents);
}

// ✅ correct - the account protects and changes its own state
$account->withdraw($amountCents);
```

```php
final class Account
{
    public function __construct(private int $balanceCents) {}

    public function withdraw(int $amountCents): void
    {
        if ($amountCents <= 0) {
            throw new \InvalidArgumentException('Amount must be greater than zero.');
        }

        if ($this->balanceCents < $amountCents) {
            throw new \DomainException('Insufficient funds.');
        }

        $this->balanceCents -= $amountCents;
    }
}
```

The application service still coordinates loading and persistence; it delegates the decision to the account:

```php
$account = $this->accountRepository->get($accountId);
$account->withdraw($amountCents);
$this->entityManager->flush();
```

```php
// ❌ wrong - query in the service
class OrderService
{
    public function getPendingOrders(): array
    {
        return $this->em->createQueryBuilder()
            ->select('o')
            ->from(Order::class, 'o')
            ->where('o.status = :status')
            ->setParameter('status', 'pending')
            ->getQuery()
            ->getResult()
        ;
    }
}

// ✅ correct - query in the repository
class OrderRepository extends ServiceEntityRepository
{
    public function findPending(): array
    {
        return $this->createQueryBuilder('o')
            ->where('o.status = :status')
            ->setParameter('status', 'pending')
            ->getQuery()
            ->getResult()
        ;
    }
}
```

### Controllers - thin, no business logic

Controllers are HTTP adapters: they map the request to a use case and map its result to an HTTP response. They must not implement domain rules or decide whether an entity may change state.

Keep the extraction aligned with responsibility: domain behavior goes on the object that owns the state; repositories handle queries; application services coordinate the use case; DTOs and normalizers shape the response. Do not move every branch or transformation into a generic service merely to keep the controller short.

### Controllers - never use `private` methods

**Controller classes must never declare `private` methods.** A controller action must stay a single public method that only calls into injectable classes (service, repository, normalizer, ...). If an action needs a helper step, that step is logic that belongs in a dedicated, injectable class - not a private method on the controller.

- ❌ No `private function` (or `protected function`, for the same reason) anywhere in a controller class.
- ✅ Extract the logic to whichever class owns that responsibility - an entity/value object for its invariant, an **application service** for use-case coordination, a **repository** for queries, or a **normalizer**/DTO for response shaping - and inject it into the action.

```php
// ❌ wrong - private helper method in the controller
class OrderController extends AbstractController
{
    #[Route('/orders/{id}/summary', methods: ['GET'])]
    public function summary(Order $order): Response
    {
        return $this->json($this->buildSummary($order));
    }

    private function buildSummary(Order $order): array
    {
        // ... transformation logic ...
    }
}

// ✅ correct - helper logic moved to a dedicated injectable class
class OrderController extends AbstractController
{
    #[Route('/orders/{id}/summary', methods: ['GET'])]
    public function summary(Order $order, OrderService $orderService): Response
    {
        return $this->json($orderService->buildSummary($order));
    }
}
```

### DTOs and value types - colocate with their owner, never a reverse dependency

A DTO/normalizer output type describing what one service or one class returns is defined in that service's/class's own file (or a file named after it), not centralized in a shared `Dto`/`Type`-style file that then has to `use` the service/class it describes to shape itself. That inverts the dependency: the shared file is meant to be a leaf other classes depend on, not something that itself depends on the service it types. A shared DTO folder is fine for types genuinely used by several unrelated services (e.g. a generic paginated-list wrapper) - not for a type that only ever describes one service's output.

### Commands - thin, same responsibility boundaries as controllers

Console commands are CLI adapters. Keep option/argument parsing, `SymfonyStyle` output formatting, and exit-code selection in the command. Put an invariant or state transition on the domain object that owns it; use an application service to coordinate a reusable use case. Unlike controllers, a command may have private methods for CLI-only work. Do not create a service merely to move code out of a command.

```php
// ❌ wrong - parsing, batching, and persistence all live in the command
class ImportProductsCommand extends Command
{
    protected function execute(InputInterface $input, OutputInterface $output): int
    {
        $rows = array_map('str_getcsv', file((string) $input->getArgument('csv-path')));
        foreach ($rows as $row) {
            $product = new Product();
            // ... mapping, validation, persist ...
        }
        $this->em->flush();
    }
}

// ✅ correct - command maps CLI input to a use case and renders progress;
// domain objects still enforce their own invariants during the import
class ImportProductsCommand extends Command
{
    public function __construct(private readonly ProductImportService $productImportService)
    {
        parent::__construct();
    }

    protected function execute(InputInterface $input, OutputInterface $output): int
    {
        $io = new SymfonyStyle($input, $output);
        $stats = $this->productImportService->importFromCsv((string) $input->getArgument('csv-path'));
        $io->success(sprintf('%d imported, %d errors', $stats['imported'], $stats['errors']));
        return $stats['errors'] > 0 ? Command::FAILURE : Command::SUCCESS;
    }
}
```

### Service naming

Use `src/Service/` for focused application services, domain services, and established integration services such as `EmailService`; name those classes and files `*Service`. Do not put an entity rule, query, parser, or external client there just to satisfy the suffix convention. Place other responsibilities in the appropriate location defined by `.context/architecture.md`.

### Email sending - always via EmailService

All emails must be sent through `EmailService`, never directly via `MailerInterface`, `SesClient`, or any other transport. This service is an external integration boundary, not a general home for unrelated domain rules. Add a dedicated method for each new email type, with its own Twig template in `templates/emails/`.

```php
// ❌ wrong
$this->mailer->send($email);

// ✅ correct
$this->emailService->sendBackupError($subject, $detail);
```

### Entity conventions

- **Money**: all money values stored as **integers (cents)**.
- **Timestamps**: `createdAt` / `updatedAt` on all entities - set via `#[ORM\PrePersist]` and `#[ORM\PreUpdate]`; the entity class **must** carry `#[ORM\HasLifecycleCallbacks]`.
- Entities expose intention-revealing methods for state transitions and enforce invariants over their own state. Getters remain appropriate for reading; avoid caller-side getter/check/setter sequences that duplicate a rule outside its owner.

### Migrations

After generating a migration with `doctrine:migrations:diff`, always remove the auto-generated comments before committing:
- The `/** Auto-generated Migration: Please modify to your needs! */` docblock on the class
- The `// this up() migration is auto-generated, please modify it to your needs` inline comments in `up()` and `down()`

### API Platform - routes MUST use kebab-case, never underscores

**Every API route/URI segment MUST use kebab-case (`-`). Underscores in a URI path are a hard error, no exceptions.** This applies to `uriTemplate`, custom operation paths, and any `#[Route]` used for an API endpoint.

- ✅ `/order-items`, `/payment-methods`, `/api/webhook-backup`
- ❌ `/order_items`, `/payment_methods`, `/api/webhook_backup`

This is independent from PHP/property naming (`snake_case` properties are fine per the Entity conventions above) - only the **URI itself** is affected. Property/field names in the request or response body follow the project's serialization convention, not this rule.

```php
// ❌ wrong - underscore in the URI
#[ApiResource(
    operations: [
        new GetCollection(uriTemplate: '/order_items'),
    ],
)]
class OrderItem {}

// ✅ correct - kebab-case URI
#[ApiResource(
    operations: [
        new GetCollection(uriTemplate: '/order-items'),
    ],
)]
class OrderItem {}
```

**Before adding or editing any `#[ApiResource]` operation or `#[Route]` on an API controller, check the URI for underscores.** A reviewer must reject the route on sight if one is found - this is not a style nitpick, it's a project-wide contract with the frontend and any external consumer of the API.

### Idempotent endpoints - payment and order mutations

Any endpoint that triggers a **non-repeatable side effect** (charging a card, creating an order, sending a payment to a PSP) **MUST be idempotent**. A retried request (double-click, network timeout, client auto-retry) must produce the same result as the first request - never a second charge, a second order, a second email.

- The client sends an **idempotency key** (UUID generated once per user action, e.g. on button click) in a header (`Idempotency-Key`).
- The server checks the key **before** processing: if it has already been seen, return the stored result of the original request instead of re-executing the side effect.
- Store the key alongside the operation's result (dedicated table or column), scoped to the resource/user, with a reasonable expiry.
- **Never rely on the frontend disabling the button as the only protection** - it helps UX, but the guarantee must live server-side, since a slow network, a retry, or a direct API call bypasses it.

```php
// ❌ wrong - no idempotency check, every call charges the card
#[Route('/payment', methods: ['POST'])]
public function pay(Request $request, PaymentService $paymentService): Response
{
    $result = $paymentService->charge($request->toArray());
    return $this->json($result);
}

// ✅ correct - idempotency key checked before the side effect
#[Route('/payment', methods: ['POST'])]
public function pay(Request $request, PaymentService $paymentService): Response
{
    $idempotencyKey = $request->headers->get('Idempotency-Key');
    if (!$idempotencyKey) {
        throw new BadRequestHttpException('Missing Idempotency-Key header.');
    }

    $result = $paymentService->chargeIdempotent($idempotencyKey, $request->toArray());
    return $this->json($result);
}
```

### Twig Templates

- **Indentation**: use tabs, not spaces.

---

## Testing

- **PHPUnit** (or the tool recorded in `## Testing` of `.context/architecture.md`) for unit and functional tests. Tests in `/backend/tests/`.
- Unit tests for **services**, entities, and **domain logic**; repository tests against the test database.
- Functional tests for **API endpoints**.
- ✅ Test (TDD): entities, services, domain logic, repositories, API endpoints, and bug fixes. ❌ Skip: config files, generated code, migrations (verify by running them).
- **The TDD loop is MANDATORY** for all of the above (`.context/coding-conventions/tdd.md`): one failing test, minimum code, refactor. Use `WebTestCase` for API/page functional tests, fakes for ports, and real objects for entities.

---

## Quick Reference

| You're about to... | Instead |
|---|---|
| Query the DB from a service | Put the query in the repository |
| Put an entity's invariant in a generic service | Add an intention-revealing method to the entity/value object that owns the state |
| Coordinate a use case across repositories, objects, or external systems | Use a focused application service; let domain objects enforce their own invariants |
| `$this->em->getRepository(Foo::class)` | Inject the repository via constructor |
| Put a non-service class in `src/Service/` to satisfy its naming rule | Place it according to its actual responsibility and the project architecture |
| Add a `private`/`protected` method to a controller | Extract it to the domain object, application service, repository, or normalizer that owns the work |
| Add a new user-owned resource without updating `CurrentUserExtension` | Add it to `OWNED_RESOURCES` and throw `AccessDeniedException` if no user |

---

### Data isolation - CurrentUserExtension

**Every user-owned resource MUST be listed in `CurrentUserExtension::OWNED_RESOURCES`.** This is a security invariant, not a convenience.

The extension ships at `src/ApiPlatform/CurrentUserExtension.php`, already wired in and unit-tested. Adding a user-owned entity means adding one class-string to that array - do not re-implement the class. The code below explains *why* it throws; it is not a template to copy.

The extension scopes all collection and item queries to the current user. When the resource is in the protected list and no authenticated user is found, **throw `AccessDeniedException` - never `return` silently.** A silent return means an unauthenticated request hitting a future public route returns every row for every user with no error.

```php
// ❌ wrong - silent pass-through exposes all rows on unauthenticated access
private function addFilter(QueryBuilder $qb, string $resourceClass): void
{
    if (!in_array($resourceClass, self::OWNED_RESOURCES, true)) {
        return;
    }

    $user = $this->security->getUser();
    if (!$user) {
        return; // ← no user = no filter = full table exposed
    }

    $qb->andWhere('o.user = :user')->setParameter('user', $user);
}

// ✅ correct - owned resource with no user → hard fail
private function addFilter(QueryBuilder $qb, string $resourceClass): void
{
    if (!in_array($resourceClass, self::OWNED_RESOURCES, true)) {
        return;
    }

    $user = $this->security->getUser();
    if (!$user) {
        throw new AccessDeniedException(); // ← defense-in-depth: firewall can be misconfigured
    }

    $qb->andWhere('o.user = :user')->setParameter('user', $user);
}
```

The `access_control` firewall is the primary guard, but it is configuration - it can be misconfigured or bypassed. The extension is the last line of defense at the data layer.
