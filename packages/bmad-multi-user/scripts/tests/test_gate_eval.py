#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///
"""Lightweight self-check for gate_eval pass-substrate."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "gate_eval.py"


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
        check=False,
    )


def main() -> int:
    failures: list[str] = []

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        story_id = "1-2-example"

        ok = run(["-p", str(root), "--story", story_id])
        if ok.returncode != 0:
            failures.append(f"happy path exit {ok.returncode}, want 0")
        try:
            payload = json.loads(ok.stdout)
        except json.JSONDecodeError as err:
            failures.append(f"stdout not JSON: {err}")
            payload = {}
        if payload.get("ok") is not True:
            failures.append(f"ok={payload.get('ok')!r}, want True")
        if payload.get("mode") != "pass_substrate":
            failures.append(f"mode={payload.get('mode')!r}")
        if payload.get("message") != "no gate rules loaded (pass-substrate)":
            failures.append(f"message={payload.get('message')!r}")
        if payload.get("reasons") != []:
            failures.append(f"reasons={payload.get('reasons')!r}, want []")
        if payload.get("story") != story_id:
            failures.append(f"story={payload.get('story')!r}, want {story_id!r}")
        if not payload.get("version"):
            failures.append("version missing")
        warnings = payload.get("warnings")
        if not isinstance(warnings, list) or not warnings:
            failures.append(f"warnings={warnings!r}, want non-empty list")
        if payload.get("error") is not None:
            failures.append(f"error={payload.get('error')!r}, want null")
        if "warning:" not in ok.stderr:
            failures.append("stderr missing warning: prefix")
        if "no gate rules loaded" not in ok.stderr:
            failures.append("stderr missing human pass-substrate message")

        missing = run(["--project-root", str(root / "does-not-exist")])
        if missing.returncode != 2:
            failures.append(f"missing root exit {missing.returncode}, want 2")
        try:
            err_payload = json.loads(missing.stdout)
        except json.JSONDecodeError as err:
            failures.append(f"missing root stdout not JSON: {err}")
            err_payload = {}
        if err_payload.get("ok") is not False:
            failures.append(f"missing root ok={err_payload.get('ok')!r}, want False")
        if not err_payload.get("error"):
            failures.append("missing root error field empty")
        if err_payload.get("version") is None:
            failures.append("missing root version missing")

        no_arg = run([])
        if no_arg.returncode != 2:
            failures.append(f"missing --project-root exit {no_arg.returncode}, want 2")
        try:
            usage_payload = json.loads(no_arg.stdout)
        except json.JSONDecodeError as err:
            failures.append(f"usage error stdout not JSON: {err}")
            usage_payload = {}
        if usage_payload.get("ok") is not False:
            failures.append(f"usage ok={usage_payload.get('ok')!r}, want False")
        if not usage_payload.get("error"):
            failures.append("usage error field empty")

    if failures:
        sys.stderr.write("FAIL:\n" + "\n".join(f"- {f}" for f in failures) + "\n")
        return 1
    sys.stdout.write("ok\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
