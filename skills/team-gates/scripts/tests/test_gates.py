#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Tests for gates.py"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "gates.py"


def run(*args: str) -> dict:
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
        check=False,
    )
    if not proc.stdout.strip():
        raise AssertionError(f"empty stdout rc={proc.returncode} stderr={proc.stderr}")
    data = json.loads(proc.stdout)
    data["_code"] = proc.returncode
    return data


class GatesTests(unittest.TestCase):
    def test_set_get_check_order(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            team = root / "team"
            pa = root / "planning"
            pa.mkdir()
            (pa / "prd.md").write_text(
                "---\nstatus: ready\n---\n\n# PRD\n", encoding="utf-8"
            )
            (pa / "arch.md").write_text(
                "---\nstatus: draft\n---\n\n# Arch\n", encoding="utf-8"
            )

            out = run(
                "set-artifacts",
                "--team-dir",
                str(team),
                "--map",
                "prd=prd.md,architecture=arch.md",
            )
            self.assertTrue(out["ok"])

            out = run(
                "set-layers",
                "--team-dir",
                str(team),
                "--layers",
                "backend,frontend",
            )
            self.assertEqual(out["layers"], ["backend", "frontend"])

            out = run(
                "set",
                "--team-dir",
                str(team),
                "--story",
                "1.1",
                "--requires",
                "prd",
                "--layer",
                "backend",
            )
            self.assertTrue(out["ok"])

            out = run(
                "set",
                "--team-dir",
                str(team),
                "--story",
                "1.2",
                "--requires",
                "prd,architecture",
                "--layer",
                "frontend",
                "--depends-on",
                "1.1",
            )
            self.assertTrue(out["ok"])

            got = run("get", "--team-dir", str(team), "--story", "1.2")
            self.assertTrue(got["defined"])
            self.assertEqual(got["gate"]["layer"], "frontend")

            chk11 = run(
                "check",
                "--team-dir",
                str(team),
                "--planning-artifacts",
                str(pa),
                "--story",
                "1.1",
            )
            self.assertTrue(chk11["pass"])

            chk12 = run(
                "check",
                "--team-dir",
                str(team),
                "--planning-artifacts",
                str(pa),
                "--story",
                "1.2",
            )
            self.assertFalse(chk12["pass"])
            self.assertTrue(
                any("architecture" in r for r in chk12["reasons"]),
                chk12["reasons"],
            )

            # Ready architecture → 1.2 passes
            (pa / "arch.md").write_text(
                "---\nstatus: ready\n---\n\n# Arch\n", encoding="utf-8"
            )
            chk12b = run(
                "check",
                "--team-dir",
                str(team),
                "--planning-artifacts",
                str(pa),
                "--story",
                "1.2",
            )
            self.assertTrue(chk12b["pass"], chk12b)

            ordered = run("order", "--team-dir", str(team))
            ids = [x["story"] for x in ordered["ordered"]]
            self.assertEqual(ids, ["1.1", "1.2"])

    def test_undefined_not_pass(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            team = root / "team"
            pa = root / "planning"
            pa.mkdir()
            team.mkdir()
            (team / "gates.json").write_text("{}\n", encoding="utf-8")
            out = run(
                "check",
                "--team-dir",
                str(team),
                "--planning-artifacts",
                str(pa),
                "--story",
                "9.9",
            )
            self.assertTrue(out["undefined"])
            self.assertFalse(out["pass"])


if __name__ == "__main__":
    unittest.main()
