#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Ready / unfinished / explain from team gates + optional sprint-status. Stdlib only."""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path
from types import ModuleType

UNFINISHED_STATUSES = frozenset({"in-progress", "review"})
DONE_STATUS = "done"
STORY_KEY_RE = re.compile(r"^(\d+)-(\d+[a-z]?)(?:-|$)")
GATE_DOT_RE = re.compile(r"^(\d+)\.(\d+[a-z]?)$")
EPIC_OR_RETRO = re.compile(r"^(epic-\d+|epic-\d+-retrospective|\d+-retrospective)$")


def default_gates_py() -> Path:
    # skills/team-status/scripts → skills/team-gates/scripts/gates.py
    return (
        Path(__file__).resolve().parent.parent.parent
        / "team-gates"
        / "scripts"
        / "gates.py"
    )


def load_gates(gates_py: Path) -> ModuleType:
    if not gates_py.is_file():
        raise FileNotFoundError(f"gates.py not found at {gates_py}")
    spec = importlib.util.spec_from_file_location("team_gates_gates", gates_py)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load gates module from {gates_py}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def gate_story_keys(story: str) -> set[str]:
    """Aliases so gate id '1.1' matches sprint key '1-1-foo'."""
    keys = {story}
    m = GATE_DOT_RE.match(story)
    if m:
        keys.add(f"{m.group(1)}-{m.group(2)}")
        return keys
    m = STORY_KEY_RE.match(story)
    if m:
        keys.add(f"{m.group(1)}.{m.group(2)}")
        keys.add(f"{m.group(1)}-{m.group(2)}")
    return keys


def sprint_matches_gate(sprint_key: str, gate_story: str) -> bool:
    aliases = gate_story_keys(gate_story)
    if sprint_key in aliases:
        return True
    m = STORY_KEY_RE.match(sprint_key)
    if not m:
        return False
    prefix = f"{m.group(1)}-{m.group(2)}"
    dotted = f"{m.group(1)}.{m.group(2)}"
    return prefix in aliases or dotted in aliases


def is_story_sprint_key(key: str) -> bool:
    if EPIC_OR_RETRO.match(key):
        return False
    return STORY_KEY_RE.match(key) is not None


def parse_sprint_development_status(path: Path) -> dict[str, str]:
    """Light parse of sprint-status.yaml development_status map. No PyYAML."""
    text = path.read_text(encoding="utf-8")
    in_block = False
    out: dict[str, str] = {}
    for line in text.splitlines():
        if re.match(r"^development_status:\s*$", line):
            in_block = True
            continue
        if not in_block:
            continue
        if line and not line[0].isspace() and ":" in line and not line.startswith(" "):
            # next top-level key
            break
        if line.strip().startswith("#") or not line.strip():
            continue
        m = re.match(r"^\s+([^\s:#][^:]*?):\s*(.+?)\s*$", line)
        if not m:
            continue
        key, val = m.group(1).strip(), m.group(2).strip().strip("\"'")
        if key and val:
            out[key] = val
    return out


_DEP_UNDEFINED_RE = re.compile(r"^depends_on '([^']+)' has no gate definition$")
_DEP_NOT_PASS_RE = re.compile(r"^depends_on '([^']+)' not pass$")


def soft_offer_for_check(result: dict) -> dict:
    """Mirror team-gates soft-offer table for one check result.

    Match depends_on reason shapes before bare 'no gate definition' so a
    dep-undefined string cannot soft-offer the checked story.
    """
    if result.get("undefined"):
        return {
            "soft_offer": "team-gates",
            "soft_offer_intent": "define",
            "soft_offer_story": result.get("story"),
        }
    reasons = list(result.get("reasons") or [])
    story = result.get("story")
    for r in reasons:
        m = _DEP_UNDEFINED_RE.match(r)
        if m:
            return {
                "soft_offer": "team-gates",
                "soft_offer_intent": "define",
                "soft_offer_story": m.group(1),
            }
        m = _DEP_NOT_PASS_RE.match(r)
        if m:
            return {
                "soft_offer": "team-gates",
                "soft_offer_intent": "check",
                "soft_offer_story": m.group(1),
            }
        if "status=" in r and "need ready" in r:
            return {"soft_offer": "team-ready", "soft_offer_intent": "set"}
        if (
            r == "no gate definition"
            or "has no path in artifacts map" in r
            or "missing at" in r
        ):
            return {
                "soft_offer": "team-gates",
                "soft_offer_intent": "define",
                "soft_offer_story": story,
            }
        if "cycle" in r:
            return {}
    return {}


def build_status(
    gates: ModuleType,
    team_dir: Path,
    planning_artifacts: Path,
    include_unfinished: bool,
    sprint_status: Path | None,
    layers_cli: str | None,
    story: str | None,
) -> dict:
    doc = gates.load_doc(team_dir)
    layers = gates.resolve_layers(layers_cli, doc, team_dir)
    stories = doc.get("stories") or {}

    sprint_map: dict[str, str] = {}
    sprint_error: str | None = None
    if sprint_status is not None:
        if not sprint_status.is_file():
            sprint_error = f"sprint-status not found: {sprint_status}"
        else:
            try:
                sprint_map = parse_sprint_development_status(sprint_status)
            except OSError as e:
                sprint_error = str(e)

    if story:
        result = gates.check_story(doc, story, planning_artifacts, layers)
        payload: dict = {
            "ok": True,
            "intent": "explain",
            "result": result,
            "ready": bool(result.get("pass")),
        }
        if result.get("pass"):
            payload["soft_offer"] = "bmad-build"
            payload["soft_offer_story"] = story
        else:
            payload.update(soft_offer_for_check(result))
        return payload

    results = [
        gates.check_story(doc, sid, planning_artifacts, layers)
        for sid in sorted(stories)
    ]
    ready: list[dict] = []
    blocked: list[dict] = []
    for r in results:
        sid = r["story"]
        sprint_st = None
        for sk, sv in sprint_map.items():
            if sprint_matches_gate(sk, sid):
                sprint_st = sv
                break
        entry = {
            "story": sid,
            "layer": r.get("layer"),
            "pass": bool(r.get("pass")),
            "undefined": bool(r.get("undefined")),
            "reasons": list(r.get("reasons") or []),
            "sprint_status": sprint_st,
        }
        if r.get("pass") and sprint_st != DONE_STATUS:
            ready.append(entry)
        else:
            blocked.append(entry)

    unfinished: list[dict] = []
    if include_unfinished:
        for sk, sv in sorted(sprint_map.items()):
            if not is_story_sprint_key(sk):
                continue
            if sv not in UNFINISHED_STATUSES:
                continue
            unfinished.append({"story": sk, "sprint_status": sv})

    payload = {
        "ok": True,
        "intent": "ready",
        "layers": layers,
        "ready": ready,
        "blocked": blocked,
        "empty_fleet": len(stories) == 0,
        "include_unfinished": include_unfinished,
        "unfinished": unfinished if include_unfinished else [],
    }
    if sprint_status is not None:
        payload["sprint_status_path"] = str(sprint_status)
    if sprint_error:
        payload["sprint_warning"] = sprint_error

    if payload["empty_fleet"]:
        payload["soft_offer"] = "team-gates"
        payload["soft_offer_intent"] = "define"
    elif ready:
        payload["soft_offer"] = "bmad-build"
        payload["soft_offer_story"] = ready[0]["story"]
    elif blocked:
        mini = {
            "story": blocked[0]["story"],
            "undefined": blocked[0]["undefined"],
            "reasons": blocked[0]["reasons"],
            "pass": False,
        }
        payload.update(soft_offer_for_check(mini))

    return payload


def main() -> int:
    p = argparse.ArgumentParser(
        description="List ready stories / unfinished / explain gate blockers"
    )
    p.add_argument(
        "action",
        choices=("ready", "explain"),
        help="ready = fleet list; explain = one story",
    )
    p.add_argument("--team-dir", required=True)
    p.add_argument("--planning-artifacts", required=True)
    p.add_argument("--story", help="Required for explain")
    p.add_argument(
        "--include-unfinished",
        action="store_true",
        help="Include in-progress/review from sprint-status",
    )
    p.add_argument(
        "--sprint-status",
        help="Path to sprint-status.yaml (optional; needed for unfinished / done filter)",
    )
    p.add_argument("--layers", help="Comma-separated layer order override")
    p.add_argument(
        "--gates-py",
        help="Path to team-gates scripts/gates.py (default: sibling skill)",
    )
    args = p.parse_args()

    team_dir = Path(args.team_dir)
    pa = Path(args.planning_artifacts)
    sprint = Path(args.sprint_status) if args.sprint_status else None
    gates_py = Path(args.gates_py) if args.gates_py else default_gates_py()

    try:
        gates = load_gates(gates_py)
    except (OSError, ImportError, FileNotFoundError) as e:
        print(json.dumps({"ok": False, "error": str(e)}))
        return 1

    if args.action == "explain" and not args.story:
        print(json.dumps({"ok": False, "error": "--story required for explain"}))
        return 1

    try:
        if args.action == "explain":
            out = build_status(
                gates, team_dir, pa, False, sprint, args.layers, args.story
            )
        else:
            out = build_status(
                gates,
                team_dir,
                pa,
                args.include_unfinished,
                sprint,
                args.layers,
                None,
            )
    except (OSError, ValueError, json.JSONDecodeError) as e:
        print(json.dumps({"ok": False, "error": str(e)}))
        return 1

    print(json.dumps(out, ensure_ascii=False))
    return 0 if out.get("ok") else 1


if __name__ == "__main__":
    sys.exit(main())
