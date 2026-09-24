#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Tests for status.py"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "status.py"
GATES = (
    Path(__file__).resolve().parent.parent.parent.parent
    / "team-gates"
    / "scripts"
    / "gates.py"
)


def _load_status():
    spec = importlib.util.spec_from_file_location("team_status_status", SCRIPT)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


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


def run_gates(*args: str) -> dict:
    proc = subprocess.run(
        [sys.executable, str(GATES), *args],
        capture_output=True,
        text=True,
        check=False,
    )
    data = json.loads(proc.stdout)
    data["_code"] = proc.returncode
    return data


class SoftOfferUnitTests(unittest.TestCase):
    def test_depends_on_undefined_targets_dep(self) -> None:
        status = _load_status()
        out = status.soft_offer_for_check(
            {
                "story": "1.2",
                "undefined": False,
                "reasons": ["depends_on '1.1' has no gate definition"],
                "pass": False,
            }
        )
        self.assertEqual(out["soft_offer"], "team-gates")
        self.assertEqual(out["soft_offer_intent"], "define")
        self.assertEqual(out["soft_offer_story"], "1.1")

    def test_depends_on_not_pass_targets_dep(self) -> None:
        status = _load_status()
        out = status.soft_offer_for_check(
            {
                "story": "1.2",
                "undefined": False,
                "reasons": ["depends_on '1.1' not pass"],
                "pass": False,
            }
        )
        self.assertEqual(out["soft_offer"], "team-gates")
        self.assertEqual(out["soft_offer_intent"], "check")
        self.assertEqual(out["soft_offer_story"], "1.1")

    def test_bare_no_gate_definition_targets_checked(self) -> None:
        status = _load_status()
        out = status.soft_offer_for_check(
            {
                "story": "1.2",
                "undefined": False,
                "reasons": ["no gate definition"],
                "pass": False,
            }
        )
        self.assertEqual(out["soft_offer_story"], "1.2")


class StatusTests(unittest.TestCase):
    def test_ready_explain_unfinished(self) -> None:
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
            sprint = root / "sprint-status.yaml"
            sprint.write_text(
                "\n".join(
                    [
                        "development_status:",
                        "  epic-1: in-progress",
                        "  1-1-backend-api: in-progress",
                        "  1-2-frontend-ui: ready-for-dev",
                        "  epic-1-retrospective: optional",
                        "",
                    ]
                ),
                encoding="utf-8",
            )

            run_gates(
                "set-artifacts",
                "--team-dir",
                str(team),
                "--map",
                "prd=prd.md,architecture=arch.md",
            )
            run_gates(
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
            run_gates(
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

            ready = run(
                "ready",
                "--team-dir",
                str(team),
                "--planning-artifacts",
                str(pa),
                "--gates-py",
                str(GATES),
                "--sprint-status",
                str(sprint),
                "--include-unfinished",
            )
            self.assertTrue(ready["ok"])
            self.assertEqual([x["story"] for x in ready["ready"]], ["1.1"])
            self.assertEqual(ready["soft_offer"], "bmad-build")
            self.assertEqual(
                [u["story"] for u in ready["unfinished"]],
                ["1-1-backend-api"],
            )

            expl = run(
                "explain",
                "--team-dir",
                str(team),
                "--planning-artifacts",
                str(pa),
                "--gates-py",
                str(GATES),
                "--story",
                "1.2",
            )
            self.assertTrue(expl["ok"])
            self.assertFalse(expl["ready"])
            self.assertEqual(expl["soft_offer"], "team-ready")

    def test_empty_fleet(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            team = root / "team"
            team.mkdir()
            pa = root / "planning"
            pa.mkdir()
            out = run(
                "ready",
                "--team-dir",
                str(team),
                "--planning-artifacts",
                str(pa),
                "--gates-py",
                str(GATES),
            )
            self.assertTrue(out["ok"])
            self.assertTrue(out["empty_fleet"])
            self.assertEqual(out["soft_offer"], "team-gates")

    def test_explain_depends_on_undefined(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            team = root / "team"
            pa = root / "planning"
            pa.mkdir()
            (pa / "prd.md").write_text(
                "---\nstatus: ready\n---\n\n# PRD\n", encoding="utf-8"
            )
            run_gates(
                "set-artifacts",
                "--team-dir",
                str(team),
                "--map",
                "prd=prd.md",
            )
            run_gates(
                "set",
                "--team-dir",
                str(team),
                "--story",
                "1.2",
                "--requires",
                "prd",
                "--depends-on",
                "1.1",
            )
            expl = run(
                "explain",
                "--team-dir",
                str(team),
                "--planning-artifacts",
                str(pa),
                "--gates-py",
                str(GATES),
                "--story",
                "1.2",
            )
            self.assertTrue(expl["ok"])
            self.assertFalse(expl["ready"])
            self.assertEqual(expl["soft_offer"], "team-gates")
            self.assertEqual(expl["soft_offer_intent"], "define")
            self.assertEqual(expl["soft_offer_story"], "1.1")


if __name__ == "__main__":
    unittest.main()
