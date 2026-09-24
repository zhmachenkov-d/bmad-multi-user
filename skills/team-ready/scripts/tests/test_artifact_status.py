#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Tests for artifact_status.py"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "artifact_status.py"


def run(*args: str) -> dict:
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
        check=False,
    )
    data = json.loads(proc.stdout)
    data["_code"] = proc.returncode
    return data


class ArtifactStatusTests(unittest.TestCase):
    def test_get_missing_status(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "doc.md"
            path.write_text("# Hello\n", encoding="utf-8")
            out = run("get", "--path", str(path))
            self.assertTrue(out["ok"])
            self.assertIsNone(out["status"])

    def test_set_and_get(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "doc.md"
            path.write_text(
                "---\ntitle: Demo\nstatus: draft\n---\n\n# Body\n",
                encoding="utf-8",
            )
            out = run(
                "set", "--path", str(path), "--status", "ready", "--actor", "Test"
            )
            self.assertTrue(out["ok"])
            self.assertEqual(out["previous"], "draft")
            self.assertEqual(out["status"], "ready")
            text = path.read_text(encoding="utf-8")
            self.assertIn("status: ready", text)
            self.assertIn("status_set_by: Test", text)
            self.assertIn("# Body", text)
            got = run("get", "--path", str(path))
            self.assertEqual(got["status"], "ready")
            self.assertTrue(got["known"])

    def test_reject_bad_status(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "doc.md"
            path.write_text("---\nstatus: draft\n---\n\nx\n", encoding="utf-8")
            proc = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "set",
                    "--path",
                    str(path),
                    "--status",
                    "final",
                ],
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(proc.returncode, 0)


if __name__ == "__main__":
    unittest.main()
