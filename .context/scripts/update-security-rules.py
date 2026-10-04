"""Refresh the committed OWASP security rules snapshot in .context/security-rules/."""

import json
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path


SOURCE = "https://github.com/vchirrav-eng/owasp-secure-coding-md.git"
ROOT = Path(__file__).resolve().parents[2]
SNAPSHOT = ROOT / ".context" / "security-rules"
MANIFEST = SNAPSHOT / "source.json"


def read_commit():
	try:
		return json.loads(MANIFEST.read_text(encoding="utf-8"))["commit"]
	except (OSError, ValueError, KeyError):
		return None


def main():
	try:
		with tempfile.TemporaryDirectory() as temporary:
			checkout = Path(temporary) / "upstream"
			subprocess.run(["git", "clone", "--depth", "1", "--quiet", SOURCE, str(checkout)], check=True, timeout=120)
			commit = subprocess.check_output(["git", "-C", str(checkout), "rev-parse", "HEAD"], text=True).strip()
			files = sorted((checkout / "rules").glob("*.md"))
			if not files or any(path.is_symlink() or not path.is_file() for path in files):
				raise ValueError("The upstream rules directory is empty or contains symbolic links")

			if commit == read_commit():
				print(f"Security rules: already up to date ({commit})")
				return 0

			shutil.rmtree(SNAPSHOT, ignore_errors=True)
			(SNAPSHOT / "rules").mkdir(parents=True)
			for path in files:
				shutil.copy2(path, SNAPSHOT / "rules" / path.name)
			MANIFEST.write_text(json.dumps({
				"source": SOURCE,
				"commit": commit,
				"updated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
			}, indent=2) + "\n", encoding="utf-8")
			print(f"Security rules: updated to {commit}")
			return 0
	except (OSError, ValueError, subprocess.SubprocessError) as error:
		print(f"Security rules: update failed ({error})", file=sys.stderr)
		return 1


if __name__ == "__main__":
	sys.exit(main())
