"""Refresh the local security rules snapshot at most once every seven days."""

import json
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path


SOURCE = "https://github.com/vchirrav-eng/owasp-secure-coding-md.git"
MAX_AGE_SECONDS = 7 * 24 * 60 * 60
ROOT = Path(__file__).resolve().parents[2]
CACHE = ROOT / ".cache" / "security-rules"
SNAPSHOT = CACHE / "snapshot"
MANIFEST = SNAPSHOT / "source.json"


def current_snapshot():
	try:
		metadata = json.loads(MANIFEST.read_text(encoding="utf-8"))
		if not isinstance(metadata["checked_at"], (int, float)) or not isinstance(metadata["commit"], str):
			return None
		if not (SNAPSHOT / "rules" / "input-validation.md").is_file():
			return None
		return metadata
	except (OSError, ValueError, KeyError):
		return None


def main():
	backup = CACHE / "previous"
	if not SNAPSHOT.exists() and backup.exists():
		backup.rename(SNAPSHOT)
	previous = current_snapshot()
	now = time.time()
	if previous and now - previous["checked_at"] < MAX_AGE_SECONDS:
		print(f"Security rules: {SNAPSHOT / 'rules'} ({previous['commit']})")
		return 0

	CACHE.mkdir(parents=True, exist_ok=True)
	lock = CACHE / "refresh.lock"
	if lock.exists() and now - lock.stat().st_mtime > 300:
		lock.rmdir()
	try:
		lock.mkdir()
	except FileExistsError:
		if previous:
			print(f"Security rules: refresh in progress; using {previous['commit']}")
			return 0
		print("Security rules: refresh in progress; no snapshot available", file=sys.stderr)
		return 1

	try:
		with tempfile.TemporaryDirectory(dir=CACHE) as temporary:
			checkout = Path(temporary) / "upstream"
			candidate = Path(temporary) / "snapshot"
			subprocess.run(["git", "clone", "--depth", "1", "--quiet", SOURCE, str(checkout)], check=True, timeout=120)
			commit = subprocess.check_output(["git", "-C", str(checkout), "rev-parse", "HEAD"], text=True).strip()
			rules = checkout / "rules"
			files = sorted(rules.glob("*.md"))
			if not files or any(path.is_symlink() or not path.is_file() for path in files):
				raise ValueError("The upstream rules directory is empty or contains symbolic links")
			candidate.mkdir()
			(candidate / "rules").mkdir()
			for path in files:
				shutil.copy2(path, candidate / "rules" / path.name)
			(candidate / "source.json").write_text(json.dumps({
				"source": SOURCE,
				"commit": commit,
				"checked_at": now,
				"checked_utc": datetime.fromtimestamp(now, timezone.utc).isoformat(),
			}, indent=2) + "\n", encoding="utf-8")
			if backup.exists():
				shutil.rmtree(backup)
			if SNAPSHOT.exists():
				SNAPSHOT.rename(backup)
			try:
				candidate.rename(SNAPSHOT)
			except OSError:
				if backup.exists():
					backup.rename(SNAPSHOT)
				raise
			if backup.exists():
				shutil.rmtree(backup)
			print(f"Security rules: {SNAPSHOT / 'rules'} ({commit})")
			return 0
	except (OSError, ValueError, subprocess.SubprocessError) as error:
		if previous:
			print(f"Security rules: refresh failed ({error}); using {previous['commit']}", file=sys.stderr)
			return 0
		print(f"Security rules: first download failed ({error})", file=sys.stderr)
		return 1
	finally:
		lock.rmdir()


if __name__ == "__main__":
	sys.exit(main())
