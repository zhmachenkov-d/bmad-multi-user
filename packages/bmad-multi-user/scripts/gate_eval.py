#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///
"""Single gate evaluator CLI (pass-substrate). Shared entrypoint for Hard Block checks."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True

PASS_SUBSTRATE_MODE = "pass_substrate"
PASS_SUBSTRATE_MESSAGE = "no gate rules loaded (pass-substrate)"

_EPILOG = """\
Pass-substrate (Story 1.2): always ok=true with mode=pass_substrate; no Hard Block rules yet.

Stdout JSON fields: ok (bool), mode (str), message (str), reasons (list of str).
Stderr: human one-liner on success; error text on failure.
Exit codes: 0=pass, 1=fail/block, 2=usage/runtime error.
"""


def evaluate(*, project_root: Path, story: str | None) -> dict:
    """Return structured gate result. Pass-substrate only — no real rules yet."""
    _ = project_root, story  # reserved for later Hard Block rules
    return {
        "ok": True,
        "mode": PASS_SUBSTRATE_MODE,
        "message": PASS_SUBSTRATE_MESSAGE,
        "reasons": [],
    }


def write_json_stdout(payload: dict) -> None:
    reconfigure = getattr(sys.stdout, "reconfigure", None)
    if reconfigure is not None:
        reconfigure(encoding="utf-8")
    sys.stdout.write(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "BMAD Multi-User single gate evaluator. "
            "Build hooks, status reports, and coherent-merge checks must invoke this entrypoint."
        ),
        epilog=_EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--project-root",
        "-p",
        required=True,
        type=Path,
        help="Absolute or relative path to the project root",
    )
    parser.add_argument(
        "--story",
        default=None,
        help="Optional sprint-status story key (unused in pass-substrate)",
    )
    args = parser.parse_args(argv)

    project_root = args.project_root.expanduser().resolve()
    if not project_root.is_dir():
        sys.stderr.write(f"error: project root is not a directory: {project_root}\n")
        return 2

    result = evaluate(project_root=project_root, story=args.story)
    sys.stderr.write(f"{result['message']}\n")
    write_json_stdout(result)
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
