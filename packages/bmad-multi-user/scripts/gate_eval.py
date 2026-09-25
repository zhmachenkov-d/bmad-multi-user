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

CLI_VERSION = "0.1.0"
PASS_SUBSTRATE_MODE = "pass_substrate"
PASS_SUBSTRATE_MESSAGE = "no gate rules loaded (pass-substrate)"
PASS_SUBSTRATE_WARNING = (
    "no gate rules loaded (pass-substrate); Hard Block rules not active"
)

_EPILOG = """\
Pass-substrate (Story 1.2): ok=true with mode=pass_substrate and a warnings[] entry;
no Hard Block rules yet (exit 0 — does not block).

Stdout JSON fields (success and error):
  ok (bool), mode (str|null), message (str), reasons (list),
  story (str|null), version (str), warnings (list of str),
  error (str|null) — set on usage/runtime failure.

Stderr: human one-liner / warning on success; error text on failure.
Exit codes: 0=pass (may include warnings), 1=fail/block, 2=usage/runtime error.
"""


def write_json_stdout(payload: dict) -> None:
    reconfigure = getattr(sys.stdout, "reconfigure", None)
    if reconfigure is not None:
        reconfigure(encoding="utf-8")
    sys.stdout.write(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")


def result_payload(
    *,
    ok: bool,
    mode: str | None,
    message: str,
    reasons: list[str] | None = None,
    story: str | None = None,
    warnings: list[str] | None = None,
    error: str | None = None,
) -> dict:
    return {
        "ok": ok,
        "mode": mode,
        "message": message,
        "reasons": list(reasons or []),
        "story": story,
        "version": CLI_VERSION,
        "warnings": list(warnings or []),
        "error": error,
    }


def evaluate(*, project_root: Path, story: str | None) -> dict:
    """Return structured gate result. Pass-substrate only — no real rules yet."""
    _ = project_root  # reserved for later Hard Block rules
    return result_payload(
        ok=True,
        mode=PASS_SUBSTRATE_MODE,
        message=PASS_SUBSTRATE_MESSAGE,
        story=story,
        warnings=[PASS_SUBSTRATE_WARNING],
    )


def _peek_option(argv: list[str] | None, option: str) -> str | None:
    """Return the value following ``option`` in argv, if present."""
    if not argv:
        return None
    for i, arg in enumerate(argv):
        if arg == option and i + 1 < len(argv):
            return argv[i + 1]
        prefix = f"{option}="
        if arg.startswith(prefix):
            return arg[len(prefix) :] or None
    return None


def _project_root_path(value: str) -> Path:
    if not value.strip():
        raise argparse.ArgumentTypeError("project-root is empty")
    return Path(value)


class _JsonArgumentParser(argparse.ArgumentParser):
    """Emit machine-readable JSON on usage errors (exit 2)."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._argv_for_errors: list[str] | None = None

    def parse_args(self, args=None, namespace=None):  # type: ignore[override]
        self._argv_for_errors = list(sys.argv[1:] if args is None else args)
        return super().parse_args(args, namespace)

    def error(self, message: str) -> None:  # type: ignore[override]
        sys.stderr.write(f"error: {message}\n")
        write_json_stdout(
            result_payload(
                ok=False,
                mode=None,
                message=message,
                story=_peek_option(self._argv_for_errors, "--story"),
                error=message,
            )
        )
        self.exit(2)


def _emit_usage_error(*, message: str, story: str | None) -> int:
    sys.stderr.write(f"error: {message}\n")
    write_json_stdout(
        result_payload(
            ok=False,
            mode=None,
            message=message,
            story=story,
            error=message,
        )
    )
    return 2


def main(argv: list[str] | None = None) -> int:
    parser = _JsonArgumentParser(
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
        type=_project_root_path,
        help="Absolute or relative path to the project root",
    )
    parser.add_argument(
        "--story",
        default=None,
        help=(
            "Optional sprint-status story key — echoed in JSON as story; "
            "not used for gating until Hard Block rules land"
        ),
    )
    args = parser.parse_args(argv)

    try:
        project_root = args.project_root.expanduser().resolve()
        is_dir = project_root.is_dir()
    except OSError as exc:
        return _emit_usage_error(
            message=f"project root is not accessible: {exc}",
            story=args.story,
        )

    if not is_dir:
        return _emit_usage_error(
            message=f"project root is not a directory: {project_root}",
            story=args.story,
        )

    result = evaluate(project_root=project_root, story=args.story)
    for warning in result.get("warnings") or []:
        sys.stderr.write(f"warning: {warning}\n")
    sys.stderr.write(f"{result['message']}\n")
    write_json_stdout(result)
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
