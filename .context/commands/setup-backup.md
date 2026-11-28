---
description: "Set up the database backup infrastructure (database dump → S3 + email alert) if not yet present"
---

> Assumes the `symfony-nextjs-contabo` stack (Symfony + Next.js + Docker + Contabo + nginx - see `.context/architecture.md` / `.context/infra.md`) - adapt or skip on a different stack, or when the project has no database.

Set up the complete backup feature on a project that does not have it yet. The feature adds a webhook-triggered database dump → S3 upload pipeline with email alert on failure. It is database-agnostic: only the dump command and its client tool depend on the engine (Step 1 detects it; Steps 3 and 8 use it).

**The PHP/Symfony code in this command is an example, not the contract.** It is the reference implementation for the default stack's backend. On another backend (language, framework), reproduce the same contract with that stack's idioms, conventions and test tools, and treat Steps 2 to 8 as a checklist of what to cover (dependencies, files, config, env vars, test, image):
- A `POST /api/webhook/backup` endpoint, authenticated only by an `X-Backup-Secret` header compared in constant time, fail-closed on an empty secret, and never returning internal error details.
- A service that dumps the database with the engine's native tool (credentials from `DATABASE_URL`, never on the command line), uploads the file to S3 under the configured bucket and prefix, deletes the temporary file, and prunes to `AWS_S3_BACKUP_KEEP_LAST` files named `backup_<UTC date>_<time>.sql`.
- An email alert on dump or upload failure that can never mask the original error.
- A functional test: 401 without or with a wrong secret, 200 with the right one and the service replaced by a test double. It is a step of the setup sequence, run after `/setup-stack` and the first deploy: `/init-project` → `/prd` → `/architecture` → `/setup-stack` → `/setup-backup` → `/design-system`. It does not gate `/spec`, but it is strongly recommended for any project with a database: `/spec` and `/status` remind you until the Stack table in `.context/architecture.md` has a `Backup` row (written by Step 9).

Follow `.context/coding-conventions/tdd.md` for the test in Step 7, and never commit or push: only a direct `/commit-and-push` does that. Ask the user before any outward-facing action (server writes, secrets in dashboards).

---

## Step 1 - Detect the backend mode and whether backup exists

Read `.context/architecture.md` (Key Invariants and Stack) and `.context/infra.md`.

- **Mode A - API Platform only** (the architecture forbids classic controllers: no `Controller/` folder, no `#[Route]` action): the webhook is an API Platform operation. Use the Mode A files in Step 3.
- **Mode B - plain controllers** (no API Platform): use the Mode B controller in Step 3.
- If the project has no database, stop and say this command does not apply. If the user declines the backup, install nothing and write the `Backup` row as `None - <reason>` (Step 9), which silences the reminders.

**Detect the database engine** from the `Database` row of `.context/architecture.md` and the scheme of `DATABASE_URL` in `backend/.env`. It selects the dump tool and the client package used in Steps 3 and 8:

| Engine | `DATABASE_URL` scheme | Dump tool | Debian package / Alpine package |
| --- | --- | --- | --- |
| PostgreSQL | `postgresql` | `pg_dump` | `postgresql-client` / `postgresql-client` |
| MySQL / MariaDB | `mysql` | `mysqldump` (`mariadb-dump` on a MariaDB-only client) | `default-mysql-client` / `mysql-client` (`mariadb-client`) |

For any other engine (SQL Server, MongoDB, SQLite, ...), the dump is the only engine-specific part: add its native dump tool as one more `match` arm in `BackupService::dumpCommand()` (Step 3) and its client package in Step 8, keeping everything else unchanged. Tell the user which engine you adapted and how you verified the dump.

Find the backend compose service name (`backend`, or `backend_a` under rolling deploy) and use it wherever a command below says `<backend-service>`.

Look for the webhook: `backend/src/ApiResource/BackupRun.php` (Mode A) or `backend/src/Controller/Webhook/BackupController.php` (Mode B). If it exists, stop and tell the user:
> Backup is already configured on this project. Nothing to do.

---

## Step 2 - Audit what is missing

Check each item below and build a list of what needs to be added (the items are the Symfony example; on another backend, list the equivalent dependencies, files and config):

**Composer packages** - read `backend/composer.json`:
- `aws/aws-sdk-php`
- `symfony/amazon-mailer`
- `symfony/process`
- Mode A only: `symfony/security-bundle` (the webhook is authenticated by a Symfony security authenticator)

**PHP files** - check if each exists (or its equivalent grouped by domain, such as `Service/Mail/` or `Service/Backup/`, following `symfony.md`):
- `backend/src/Service/EmailService.php`
- `backend/src/Service/BackupService.php`
- Mode A: `backend/src/ApiResource/BackupRun.php`, `backend/src/State/BackupRunProcessor.php`, `backend/src/Security/BackupSecretAuthenticator.php`
- Mode B: `backend/src/Controller/Webhook/BackupController.php`

**Symfony config** - check if exists:
- `backend/config/packages/mailer.yaml`
- `backend/config/packages/security.yaml` (Mode A: needs the `webhook` firewall, see Step 4)

**Env vars** - check `backend/.env` for each key:
- `AWS_SES_ACCESS_KEY_ID`
- `AWS_SES_SECRET_ACCESS_KEY`
- `MAILER_DSN`
- `MAILER_FROM`
- `AWS_DEFAULT_REGION`
- `AWS_S3_BACKUP_ACCESS_KEY_ID`
- `AWS_S3_BACKUP_SECRET_ACCESS_KEY`
- `AWS_S3_BACKUP_BUCKET`
- `AWS_S3_BACKUP_KEEP_LAST`
- `AWS_S3_BACKUP_WEBHOOK_SECRET`

Also check `backend/.env.example` for the same keys, and confirm the engine's dump tool is available in the backend image (Step 8).

---

## Step 3 - Create missing PHP files

Create each file that does not yet exist, using the Symfony example below as the model (adapt it to the project's backend if it is not Symfony, see the contract above). Indent with tabs.

### `backend/src/Service/EmailService.php`

```php
<?php

declare(strict_types=1);

namespace App\Service;

use Symfony\Component\DependencyInjection\Attribute\Autowire;
use Symfony\Component\Mailer\MailerInterface;
use Symfony\Component\Mime\Address;
use Symfony\Component\Mime\Email;
use Throwable;

class EmailService
{
	public function __construct(
		private readonly MailerInterface $mailer,
		#[Autowire(env: 'MAILER_FROM')]
		private readonly string $mailerFrom,
		#[Autowire('%app.name%')]
		private readonly string $appName,
	) {}

	public function sendBackupError(string $subject, string $detail): void
	{
		try {
			$email = (new Email())
				->from($this->sender($this->mailerFrom))
				->to($this->mailerFrom)
				->subject("[{$this->appName}] Backup error: {$subject}")
				->text($detail)
			;
			$this->mailer->send($email);
		} catch (Throwable) {
			// Email failure must never mask the original error
		}
	}

	/**
	 * Every email is sent under the app name (APP_NAME), never a bare address.
	 */
	private function sender(string $address): Address
	{
		return new Address($address, $this->appName);
	}
}
```

> Note: `%app.name%` must be defined in `config/services.yaml` as `app.name: '%env(APP_NAME)%'`. Verify it exists; add it if missing.

### `backend/src/Service/BackupService.php`

```php
<?php

declare(strict_types=1);

namespace App\Service;

use Aws\S3\S3Client;
use LogicException;
use Symfony\Component\DependencyInjection\Attribute\Autowire;
use Symfony\Component\Process\Exception\ProcessFailedException;
use Symfony\Component\Process\Process;
use Throwable;

class BackupService
{
	private readonly string $s3Bucket;
	private readonly string $s3Prefix;

	public function __construct(
		private readonly EmailService $emailService,
		#[Autowire(env: 'AWS_S3_BACKUP_ACCESS_KEY_ID')]
		private readonly string $awsKey,
		#[Autowire(env: 'AWS_S3_BACKUP_SECRET_ACCESS_KEY')]
		private readonly string $awsSecret,
		#[Autowire(env: 'AWS_DEFAULT_REGION')]
		private readonly string $awsRegion,
		#[Autowire(env: 'AWS_S3_BACKUP_BUCKET')]
		string $awsBucket,
		#[Autowire(env: 'int:AWS_S3_BACKUP_KEEP_LAST')]
		private readonly int $awsKeepLast,
		#[Autowire(env: 'DATABASE_URL')]
		private readonly string $databaseUrl,
	) {
		$parts = explode('/', $awsBucket, 2);
		$this->s3Bucket = $parts[0];
		$this->s3Prefix = isset($parts[1]) ? rtrim($parts[1], '/') . '/' : '';
	}

	/**
	 * @return array{file: string, deleted: string[]}
	 *
	 * @throws ProcessFailedException
	 * @throws Throwable
	 */
	public function run(): array
	{
		$tmpPath = $this->dump();
		$s3 = $this->buildS3Client();
		$s3Key = $this->upload($s3, $tmpPath);
		$deleted = $this->pruneOldBackups($s3);

		return ['file' => $s3Key, 'deleted' => $deleted];
	}

	private function dump(): string
	{
		$filename = sprintf('backup_%s.sql', gmdate('Y-m-d_H-i-s'));
		$tmpPath = sys_get_temp_dir() . '/' . $filename;

		[$command, $env] = $this->dumpCommand(parse_url($this->databaseUrl), $tmpPath);

		$process = new Process($command);
		$process->setEnv($env);
		$process->setTimeout(120);

		try {
			$process->mustRun();
		} catch (ProcessFailedException $e) {
			$this->emailService->sendBackupError('Database dump failed', $e->getMessage());
			throw $e;
		}

		return $tmpPath;
	}

	/**
	 * The only engine-specific code: the dump command writing to $tmpPath, and the environment carrying the password.
	 * Add one arm per engine the project uses (see Step 1 of /setup-backup).
	 *
	 * @param array<string, string|int> $dsn
	 *
	 * @return array{0: string[], 1: array<string, string>}
	 */
	private function dumpCommand(array $dsn, string $tmpPath): array
	{
		$host = $dsn['host'];
		$user = $dsn['user'];
		$pass = $dsn['pass'];
		$db = ltrim($dsn['path'], '/');

		return match ($dsn['scheme']) {
			'postgresql' => [
				['pg_dump', '-h', $host, '-p', (string) ($dsn['port'] ?? 5432), '-U', $user, '-d', $db, '-f', $tmpPath],
				['PGPASSWORD' => $pass],
			],
			'mysql' => [
				['mysqldump', '-h', $host, '-P', (string) ($dsn['port'] ?? 3306), '-u', $user, '--single-transaction', '--result-file=' . $tmpPath, $db],
				['MYSQL_PWD' => $pass],
			],
			default => throw new LogicException(sprintf('No dump command for the "%s" database engine.', $dsn['scheme'])),
		};
	}

	private function upload(S3Client $s3, string $tmpPath): string
	{
		$filename = basename($tmpPath);
		$s3Key = $this->s3Prefix . $filename;

		try {
			$s3->putObject([
				'Bucket' => $this->s3Bucket,
				'Key' => $s3Key,
				'SourceFile' => $tmpPath,
			]);
		} catch (Throwable $e) {
			$this->emailService->sendBackupError('S3 upload failed', $e->getMessage());
			throw $e;
		} finally {
			@unlink($tmpPath);
		}

		return $s3Key;
	}

	/** @return string[] */
	private function pruneOldBackups(S3Client $s3): array
	{
		$result = $s3->listObjectsV2([
			'Bucket' => $this->s3Bucket,
			'Prefix' => $this->s3Prefix,
		]);
		$objects = $result['Contents'] ?? [];
		// Only prune files named like backup_2026-10-29_14-39-26.sql; leave anything else in the prefix alone.
		$objects = array_filter($objects, fn ($o) => 1 === preg_match('/(?:^|\/)backup_\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}\.sql$/', $o['Key']));

		if (count($objects) <= $this->awsKeepLast) {
			return [];
		}

		usort($objects, fn ($a, $b) => strcmp($a['Key'], $b['Key']));

		$toDelete = array_slice($objects, 0, count($objects) - $this->awsKeepLast);
		$deleteKeys = array_map(fn ($o) => ['Key' => $o['Key']], $toDelete);

		$s3->deleteObjects([
			'Bucket' => $this->s3Bucket,
			'Delete' => ['Objects' => $deleteKeys],
		]);

		return array_column($toDelete, 'Key');
	}

	private function buildS3Client(): S3Client
	{
		return new S3Client([
			'version' => 'latest',
			'region' => $this->awsRegion,
			'credentials' => [
				'key' => $this->awsKey,
				'secret' => $this->awsSecret,
			],
		]);
	}
}
```

### Mode A - `backend/src/ApiResource/BackupRun.php`

```php
<?php

declare(strict_types=1);

namespace App\ApiResource;

use ApiPlatform\Metadata\ApiResource;
use ApiPlatform\Metadata\Post;
use App\State\BackupRunProcessor;

/**
 * Triggers a database backup, called by the scheduler only (the `webhook` firewall).
 */
#[ApiResource(
	shortName: 'BackupRun',
	operations: [
		new Post(
			name: 'webhook_backup',
			uriTemplate: '/webhook/backup',
			status: 200,
			input: false,
			processor: BackupRunProcessor::class,
			formats: ['json'],
		),
	],
)]
final class BackupRun
{
	/**
	 * @param string[] $deleted the keys of the old backups removed by the retention policy
	 */
	public function __construct(
		public readonly string $file,
		public readonly array $deleted,
		public readonly string $message = 'Backup uploaded',
	) {}
}
```

### Mode A - `backend/src/State/BackupRunProcessor.php`

```php
<?php

declare(strict_types=1);

namespace App\State;

use ApiPlatform\Metadata\Operation;
use ApiPlatform\State\ProcessorInterface;
use App\ApiResource\BackupRun;
use App\Service\BackupService;

/**
 * @implements ProcessorInterface<mixed, BackupRun>
 */
final readonly class BackupRunProcessor implements ProcessorInterface
{
	public function __construct(
		private BackupService $backupService,
	) {}

	public function process(mixed $data, Operation $operation, array $uriVariables = [], array $context = []): BackupRun
	{
		$result = $this->backupService->run();

		return new BackupRun($result['file'], $result['deleted']);
	}
}
```

### Mode A - `backend/src/Security/BackupSecretAuthenticator.php`

```php
<?php

declare(strict_types=1);

namespace App\Security;

use Symfony\Component\DependencyInjection\Attribute\Autowire;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Security\Core\Authentication\Token\TokenInterface;
use Symfony\Component\Security\Core\Exception\AuthenticationException;
use Symfony\Component\Security\Core\Exception\BadCredentialsException;
use Symfony\Component\Security\Core\User\InMemoryUser;
use Symfony\Component\Security\Http\Authenticator\AbstractAuthenticator;
use Symfony\Component\Security\Http\Authenticator\Passport\Badge\UserBadge;
use Symfony\Component\Security\Http\Authenticator\Passport\Passport;
use Symfony\Component\Security\Http\Authenticator\Passport\SelfValidatingPassport;

/**
 * Authenticates the scheduler (n8n) that triggers the database backup. The secret is compared in constant time and
 * the request carries no user, so it is granted a stateless role.
 */
final class BackupSecretAuthenticator extends AbstractAuthenticator
{
	public const string HEADER = 'X-Backup-Secret';

	public function __construct(
		#[Autowire(env: 'AWS_S3_BACKUP_WEBHOOK_SECRET')]
		private readonly string $secret,
	) {}

	public function supports(Request $request): ?bool
	{
		return true;
	}

	public function authenticate(Request $request): Passport
	{
		$provided = $request->headers->get(self::HEADER);

		if (null === $provided || '' === $this->secret || !hash_equals($this->secret, $provided)) {
			throw new BadCredentialsException('Invalid backup secret.');
		}

		return new SelfValidatingPassport(new UserBadge('backup-scheduler', fn (): InMemoryUser => new InMemoryUser('backup-scheduler', null, ['ROLE_BACKUP'])));
	}

	public function onAuthenticationSuccess(Request $request, TokenInterface $token, string $firewallName): ?Response
	{
		return null;
	}

	public function onAuthenticationFailure(Request $request, AuthenticationException $exception): Response
	{
		return new JsonResponse(
			['title' => 'Unauthorized', 'detail' => 'A valid backup secret is required.', 'status' => Response::HTTP_UNAUTHORIZED],
			Response::HTTP_UNAUTHORIZED,
			['Content-Type' => 'application/problem+json'],
		);
	}
}
```

### Mode B - `backend/src/Controller/Webhook/BackupController.php`

```php
<?php

declare(strict_types=1);

namespace App\Controller\Webhook;

use App\Service\BackupService;
use Symfony\Component\DependencyInjection\Attribute\Autowire;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Attribute\Route;
use Throwable;

class BackupController
{
	public function __construct(
		private readonly BackupService $backupService,
		#[Autowire(env: 'AWS_S3_BACKUP_WEBHOOK_SECRET')]
		private readonly string $webhookSecret,
	) {
	}

	#[Route('/api/webhook/backup', name: 'app_webhook_backup', methods: ['POST'])]
	public function __invoke(Request $request): JsonResponse
	{
		if (!hash_equals($this->webhookSecret, $request->headers->get('X-Backup-Secret', ''))) {
			return new JsonResponse([
				'message' => 'Unauthorized.',
			], Response::HTTP_UNAUTHORIZED);
		}

		try {
			$result = $this->backupService->run();
		} catch (Throwable $e) {
			return new JsonResponse([
				'message' => $e->getMessage(),
			], Response::HTTP_INTERNAL_SERVER_ERROR);
		}

		return new JsonResponse([
			'message' => 'Backup uploaded',
			'file' => $result['file'],
			'deleted' => $result['deleted'],
		]);
	}
}
```

### `backend/config/packages/mailer.yaml` (create only if missing)

```yaml
framework:
    mailer:
        dsn: '%env(MAILER_DSN)%'
```

---

## Step 4 - Update security.yaml

**Mode A**: the `webhook` firewall authenticates the scheduler with the secret header. Create or extend `backend/config/packages/security.yaml`, placing the `webhook` firewall before any other `^/api` firewall and its access rule before `^/api`. Keep every existing firewall and rule. A minimal file when the project has none yet:

```yaml
security:
    providers:
        backup_users:
            memory: ~
    firewalls:
        dev:
            pattern: ^/(_profiler|_wdt)
            security: false
        webhook:
            pattern: ^/api/webhook
            stateless: true
            provider: backup_users
            custom_authenticators:
                - App\Security\BackupSecretAuthenticator
    access_control:
        - { path: ^/api/webhook, roles: ROLE_BACKUP }
```

When the project has other firewalls (for example one that verifies the user's JWT), the `webhook` firewall goes first. Routes outside the firewalls (such as `/api/health`) must stay public: keep their existing `PUBLIC_ACCESS` rule.

**Mode B**: the `^/api/webhook` pattern must be public (the controller checks the secret itself). If it is not already, add:

```yaml
firewalls:
    webhook:
        pattern: ^/api/webhook
        security: false

access_control:
    - { path: ^/api/webhook, roles: PUBLIC_ACCESS }
```

Place the `webhook` firewall before the `api` firewall, and the `^/api/webhook` access rule before `^/api`.

---

## Step 5 - Update composer.json

For each of these packages, check if it is already in `backend/composer.json`. Add any that are missing to the `require` section, using the Symfony version the project already runs (`8.1.*` below is an example, never downgrade):

```json
"aws/aws-sdk-php": "^3.0",
"symfony/amazon-mailer": "8.1.*",
"symfony/process": "8.1.*"
```

Mode A also needs `"symfony/security-bundle": "8.1.*"`. Keep `sort-packages: true` order.

---

## Step 6 - Update env files

For each missing key, append it to `backend/.env` under the relevant section comment. Use placeholder values for secrets the user must fill in; never write real secrets into a committed file (real secrets go in the untracked production env file described in `.context/infra.md`).

```
# AWS SES
AWS_SES_ACCESS_KEY_ID=
AWS_SES_SECRET_ACCESS_KEY=

# Mailer
MAILER_DSN=ses+https://ACCESS_KEY:URL_ENCODED_SECRET@default?region=us-east-2
MAILER_FROM=contact@example.com

# AWS S3 Backup
AWS_DEFAULT_REGION=us-east-2
AWS_S3_BACKUP_ACCESS_KEY_ID=
AWS_S3_BACKUP_SECRET_ACCESS_KEY=
AWS_S3_BACKUP_BUCKET=my-bucket/backups/db/my-project
AWS_S3_BACKUP_KEEP_LAST=4
AWS_S3_BACKUP_WEBHOOK_SECRET=CHANGE_ME
```

In the committed `backend/.env`, `MAILER_DSN` may be `null://null` (mails are discarded) with the real SES DSN only in the production env file. Do the same for `backend/.env.example`, using empty values or safe placeholder strings (never real credentials).

---

## Step 7 - Install packages and test

Install the missing packages. Run from `backend/` against the running stack, or with a one-off container if it is not running:

```bash
docker compose run --no-deps --rm <backend-service> composer require aws/aws-sdk-php "symfony/amazon-mailer:8.1.*" "symfony/process:8.1.*" --no-interaction
```

(add `"symfony/security-bundle:8.1.*"` in Mode A). This updates `composer.lock` via the volume mount. If Docker is not running, tell the user to run this command manually before pushing.

Add a functional test of the webhook following `.context/coding-conventions/tdd.md` (location and command from the Testing table in `.context/architecture.md`): `POST /api/webhook/backup` returns 401 without the header and with a wrong secret, and 200 with the right secret when `BackupService` is replaced by a test double so no dump or S3 call happens. Pitfalls proven on a real project:
- `BackupRun` must have **no** `#[ApiProperty(identifier: true)]`: the S3 key contains `/`, so the real 200 response would fail to build an IRI and return 400. The operation has `input: false` and no item operation, so no identifier is needed.
- Force the test secret in `phpunit.dist.xml` (`<server name="AWS_S3_BACKUP_WEBHOOK_SECRET" value="..." force="true"/>`): the `.env` injected by Docker Compose (empty value) overrides `.env.test`, and the authenticator is fail-closed on an empty secret.
- Cover the 200 case in the test, since only a real response exposes the identifier defect.

Run it with the project's test command, and run static analysis.

---

## Step 8 - Check Dockerfile

Open `backend/Dockerfile` and confirm the database client tools of the detected engine (package table in Step 1) are installed in the base stage, through `apt-get` on a Debian image such as FrankenPHP, or through `apk add` on Alpine. Without them, the dump tool is not found at runtime. For PostgreSQL, the client version may be newer than the server's (for example 17 against a 16 server): this works for a dump, so note it rather than pin it.

If it is missing, add it to the existing package block of the base stage, matching the image's package manager. The client major version must be at least the database server's major version.

---

## Step 9 - Record the Backup row

Add or update the `Backup` row in the Stack table of `.context/architecture.md`, for example `| Backup | <dump tool of the engine, e.g. pg_dump> to S3 through a webhook, triggered by the scheduler | Webhook secret and S3 credentials in the production env file |`. `/spec` and `/status` read this row to stop reminding, so write it only once the files, packages and test are in place.

---

## Step 10 - Report

Tell the user:

- Which files were created.
- Which env vars were added (keys only, never values).
- Whether `composer require` ran successfully or needs to be run manually, and the test and static analysis results.
- Then show this checklist:

---

**Next steps:**

1. Fill in the real values for `AWS_S3_BACKUP_*`, `AWS_SES_*`, `MAILER_DSN`, and `MAILER_FROM` in the untracked production env file on the server (see `.context/infra.md`), and keep the placeholders in the committed `backend/.env`.
2. **Duplicate the backup workflow** - go to your backup automation tool (e.g. n8n), duplicate the existing backup workflow, then:
   - Tag it with the app name (e.g. `MyApp`)
   - Move it into the folder `Personal > [AppName]`
   - Update the HTTP request node URL (`https://<backend-domain>/api/webhook/backup`) and the `X-Backup-Secret` header to match this project
3. Redeploy the backend with the project's deploy flow (commit and push through `/commit-and-push`), then trigger the workflow once and check that the dump appears in the bucket.
