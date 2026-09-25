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

        ok = run(["-p", str(root), "--story", "1-2-example"])
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
        if "no gate rules loaded" not in ok.stderr:
            failures.append("stderr missing human pass-substrate message")

        missing = run(["--project-root", str(root / "does-not-exist")])
        if missing.returncode != 2:
            failures.append(f"missing root exit {missing.returncode}, want 2")
        if missing.stdout.strip():
            failures.append("missing root must not emit JSON on stdout")

        no_arg = run([])
        if no_arg.returncode != 2:
            failures.append(f"missing --project-root exit {no_arg.returncode}, want 2")

    if failures:
        sys.stderr.write("FAIL:\n" + "\n".join(f"- {f}" for f in failures) + "\n")
        return 1
    sys.stdout.write("ok\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
