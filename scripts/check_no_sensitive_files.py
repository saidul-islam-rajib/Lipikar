"""Block deed data, images, and model weights from entering git history. See ADR-004."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

CONFIG_PATH = Path(__file__).resolve().parent.parent / "configs" / "privacy_guard.json"


@dataclass(frozen=True)
class GuardConfig:
    forbidden_prefixes: tuple[str, ...]
    restricted_suffixes: tuple[str, ...]
    allowed_image_prefixes: tuple[str, ...]
    weight_suffixes: tuple[str, ...]
    allowed_basenames: frozenset[str]
    reasons: dict[str, str]


@dataclass(frozen=True)
class Violation:
    path: str
    reason: str


def load_config(path: Path = CONFIG_PATH) -> GuardConfig:
    """Load guard patterns; raises if absent or malformed so the guard fails closed."""
    raw = json.loads(path.read_text(encoding="utf-8"))
    return GuardConfig(
        forbidden_prefixes=tuple(raw["forbidden_prefixes"]),
        restricted_suffixes=tuple(s.lower() for s in raw["restricted_suffixes"]),
        allowed_image_prefixes=tuple(raw["allowed_image_prefixes"]),
        weight_suffixes=tuple(s.lower() for s in raw["weight_suffixes"]),
        allowed_basenames=frozenset(raw["allowed_basenames"]),
        reasons=dict(raw["reasons"]),
    )


def _git(*args: str) -> list[str]:
    """Run a git command, returning stdout as non-empty lines."""
    result = subprocess.run(
        ("git", *args), capture_output=True, text=True, check=True, encoding="utf-8"
    )
    return [line for line in result.stdout.splitlines() if line.strip()]


def find_violations(paths: list[str], config: GuardConfig) -> list[Violation]:
    """Return a Violation for every path that must not be committed."""
    found: list[Violation] = []

    for raw in paths:
        path = PurePosixPath(raw.replace("\\", "/"))
        posix = path.as_posix()
        suffix = path.suffix.lower()

        if path.name in config.allowed_basenames:
            continue

        if any(posix.startswith(prefix) for prefix in config.forbidden_prefixes):
            found.append(Violation(posix, config.reasons["forbidden_prefix"]))
            continue

        if suffix in config.restricted_suffixes and not any(
            posix.startswith(prefix) for prefix in config.allowed_image_prefixes
        ):
            found.append(Violation(posix, f"'{suffix}' {config.reasons['restricted_suffix']}"))
            continue

        if suffix in config.weight_suffixes:
            found.append(Violation(posix, f"'{suffix}' {config.reasons['weight_suffix']}"))

    return found


def collect_paths(explicit: list[str], check_all: bool) -> tuple[list[str], str]:
    """Resolve which paths to check, returning them with a human-readable scope label."""
    if explicit:
        return explicit, "given paths"
    if check_all:
        return _git("ls-files"), "all tracked files"
    return _git("diff", "--cached", "--name-only", "--diff-filter=ACMR"), "staged files"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*")
    parser.add_argument("--all", action="store_true")
    args = parser.parse_args()

    config = load_config()
    paths, scope = collect_paths(args.paths, args.all)

    if not paths:
        print(f"privacy guard: nothing to check ({scope})")
        return 0

    violations = find_violations(paths, config)
    if not violations:
        print(f"privacy guard: OK - {len(paths)} path(s) checked ({scope})")
        return 0

    print(f"privacy guard: FAILED - {len(violations)} violation(s) in {scope}\n", file=sys.stderr)
    for violation in violations:
        print(f"  {violation.path}\n      {violation.reason}", file=sys.stderr)
    print(f"\n{config.reasons['epilogue']}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
