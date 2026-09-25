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
CLI_VERSION = "0.1.0"


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
        if payload.get("version") != CLI_VERSION:
            failures.append(f"version={payload.get('version')!r}, want {CLI_VERSION!r}")
        warnings = payload.get("warnings")
        if not isinstance(warnings, list) or not warnings:
            failures.append(f"warnings={warnings!r}, want non-empty list")
        if payload.get("error") is not None:
            failures.append(f"error={payload.get('error')!r}, want null")
        if "warning:" not in ok.stderr:
            failures.append("stderr missing warning: prefix")
        if "no gate rules loaded" not in ok.stderr:
            failures.append("stderr missing human pass-substrate message")

        no_story = run(["-p", str(root)])
        if no_story.returncode != 0:
            failures.append(f"no --story exit {no_story.returncode}, want 0")
        try:
            no_story_payload = json.loads(no_story.stdout)
        except json.JSONDecodeError as err:
            failures.append(f"no --story stdout not JSON: {err}")
            no_story_payload = {}
        if no_story_payload.get("ok") is not True:
            failures.append(f"no --story ok={no_story_payload.get('ok')!r}, want True")
        if no_story_payload.get("mode") != "pass_substrate":
            failures.append(f"no --story mode={no_story_payload.get('mode')!r}")
        if no_story_payload.get("story") is not None:
            failures.append(
                f"no --story story={no_story_payload.get('story')!r}, want null"
            )
        if no_story_payload.get("version") != CLI_VERSION:
            failures.append(f"no --story version={no_story_payload.get('version')!r}")

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
        if err_payload.get("version") != CLI_VERSION:
            failures.append(f"missing root version={err_payload.get('version')!r}")
        if "error:" not in missing.stderr:
            failures.append("missing root stderr missing error: prefix")

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
        if "error:" not in no_arg.stderr:
            failures.append("usage stderr missing error: prefix")

        empty_root = run(["-p", "", "--story", story_id])
        if empty_root.returncode != 2:
            failures.append(f"empty -p exit {empty_root.returncode}, want 2")
        try:
            empty_payload = json.loads(empty_root.stdout)
        except json.JSONDecodeError as err:
            failures.append(f"empty -p stdout not JSON: {err}")
            empty_payload = {}
        if empty_payload.get("ok") is not False:
            failures.append(f"empty -p ok={empty_payload.get('ok')!r}, want False")
        if empty_payload.get("story") != story_id:
            failures.append(
                f"empty -p story={empty_payload.get('story')!r}, want {story_id!r}"
            )
        if "error:" not in empty_root.stderr:
            failures.append("empty -p stderr missing error: prefix")
        if "empty" not in (empty_payload.get("error") or "").lower():
            failures.append(
                f"empty -p error={empty_payload.get('error')!r}, want empty mention"
            )

        usage_with_story = run(["--story", story_id])
        if usage_with_story.returncode != 2:
            failures.append(f"usage+story exit {usage_with_story.returncode}, want 2")
        try:
            usage_story_payload = json.loads(usage_with_story.stdout)
        except json.JSONDecodeError as err:
            failures.append(f"usage+story stdout not JSON: {err}")
            usage_story_payload = {}
        if usage_story_payload.get("story") != story_id:
            failures.append(
                f"usage+story story={usage_story_payload.get('story')!r}, "
                f"want {story_id!r}"
            )
        if "error:" not in usage_with_story.stderr:
            failures.append("usage+story stderr missing error: prefix")

    if failures:
        sys.stderr.write("FAIL:\n" + "\n".join(f"- {f}" for f in failures) + "\n")
        return 1
    sys.stdout.write("ok\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
