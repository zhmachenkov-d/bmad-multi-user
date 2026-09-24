#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Tests for claims.py"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "claims.py"


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


class ClaimsTests(unittest.TestCase):
    def test_claim_check_release(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            team = root / "team"
            pa = root / "planning"
            pa.mkdir()
            art = pa / "prd.md"
            art.write_text("# prd\n", encoding="utf-8")

            out = run(
                "claim",
                "--team-dir",
                str(team),
                "--planning-artifacts",
                str(pa),
                "--target",
                "prd.md",
                "--actor",
                "Ada",
            )
            self.assertTrue(out["ok"])
            self.assertEqual(out["action"], "claimed")
            self.assertEqual(out["target"], "prd.md")
            self.assertFalse(out["conflict"])

            chk = run(
                "check",
                "--team-dir",
                str(team),
                "--planning-artifacts",
                str(pa),
                "--target",
                str(art),
                "--actor",
                "Bob",
            )
            self.assertTrue(chk["claimed"])
            self.assertTrue(chk["conflict"])
            self.assertEqual(chk["holder"], "Ada")

            same = run(
                "claim",
                "--team-dir",
                str(team),
                "--planning-artifacts",
                str(pa),
                "--target",
                "prd.md",
                "--actor",
                "Ada",
            )
            self.assertTrue(same["ok"])
            self.assertEqual(same["action"], "already")

            conflict = run(
                "claim",
                "--team-dir",
                str(team),
                "--planning-artifacts",
                str(pa),
                "--target",
                "prd.md",
                "--actor",
                "Bob",
            )
            self.assertFalse(conflict["ok"])
            self.assertTrue(conflict["conflict"])
            self.assertEqual(conflict["_code"], 1)

            take = run(
                "claim",
                "--team-dir",
                str(team),
                "--planning-artifacts",
                str(pa),
                "--target",
                "prd.md",
                "--actor",
                "Bob",
                "--force",
            )
            self.assertTrue(take["ok"])
            self.assertEqual(take["action"], "takeover")
            self.assertEqual(take["claim"]["actor"], "Bob")
            self.assertEqual(take["claim"]["took_from"], "Ada")

            rel = run(
                "release",
                "--team-dir",
                str(team),
                "--planning-artifacts",
                str(pa),
                "--target",
                "prd.md",
            )
            self.assertTrue(rel["released"])
            lst = run("list", "--team-dir", str(team))
            self.assertEqual(lst["count"], 0)

    def test_release_absent_and_stale_clear(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            team = Path(td) / "team"
            out = run(
                "release",
                "--team-dir",
                str(team),
                "--target",
                "gone.md",
            )
            self.assertTrue(out["ok"])
            self.assertFalse(out["released"])
            self.assertEqual(out["action"], "absent")


if __name__ == "__main__":
    unittest.main()
