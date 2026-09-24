#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Story gate definitions and soft checks. Stdlib only. File: team/gates.json."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

FM_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n?", re.DOTALL)
ALLOWED_STATUS = ("draft", "review", "ready")
GATES_NAME = "gates.json"


def _team_file(team_dir: Path) -> Path:
    return team_dir / GATES_NAME


def _empty_doc() -> dict:
    return {"artifacts": {}, "layers": [], "stories": {}}


def load_doc(team_dir: Path) -> dict:
    path = _team_file(team_dir)
    if not path.is_file():
        return _empty_doc()
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("gates.json root must be an object")
    data.setdefault("artifacts", {})
    data.setdefault("layers", [])
    data.setdefault("stories", {})
    if isinstance(data["layers"], str):
        data["layers"] = [x.strip() for x in data["layers"].split(",") if x.strip()]
    return data


def save_doc(team_dir: Path, doc: dict) -> Path:
    team_dir.mkdir(parents=True, exist_ok=True)
    path = _team_file(team_dir)
    path.write_text(
        json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return path


def parse_frontmatter_status(path: Path) -> str | None:
    text = path.read_text(encoding="utf-8")
    m = FM_RE.match(text)
    if not m:
        return None
    for line in m.group(1).splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        if key.strip() == "status":
            return val.strip().strip("\"'")
    return None


def resolve_layers(cli_layers: str | None, doc: dict, team_dir: Path) -> list[str]:
    if cli_layers:
        return [x.strip() for x in cli_layers.split(",") if x.strip()]
    if doc.get("layers"):
        return list(doc["layers"])
    layers_path = team_dir / "layers.yaml"
    if layers_path.is_file():
        # minimal: "layers: a, b" or "layers:\n  - a"
        text = layers_path.read_text(encoding="utf-8")
        for line in text.splitlines():
            if line.strip().startswith("layers:"):
                _, _, rest = line.partition(":")
                rest = rest.strip()
                if rest:
                    return [
                        x.strip().strip("\"'") for x in rest.split(",") if x.strip()
                    ]
        items = []
        for line in text.splitlines():
            s = line.strip()
            if s.startswith("- "):
                items.append(s[2:].strip().strip("\"'"))
        if items:
            return items
    return []


def split_csv(raw: str | None) -> list[str]:
    if not raw:
        return []
    return [x.strip() for x in raw.split(",") if x.strip()]


def get_story(doc: dict, story: str) -> dict | None:
    stories = doc.get("stories") or {}
    return stories.get(story)


def set_story(
    doc: dict,
    story: str,
    requires: list[str] | None,
    layer: str | None,
    depends_on: list[str] | None,
) -> dict:
    entry = dict(doc.get("stories", {}).get(story) or {})
    if requires is not None:
        entry["requires"] = requires
    if layer is not None:
        entry["layer"] = layer
    if depends_on is not None:
        entry["depends_on"] = depends_on
    entry.setdefault("requires", [])
    entry.setdefault("depends_on", [])
    doc.setdefault("stories", {})[story] = entry
    return entry


def check_story(
    doc: dict,
    story: str,
    planning_artifacts: Path,
    layers: list[str],
    _stack: list[str] | None = None,
) -> dict:
    stack = list(_stack or [])
    if story in stack:
        return {
            "ok": True,
            "story": story,
            "pass": False,
            "undefined": False,
            "reasons": [f"depends_on cycle: {' → '.join(stack + [story])}"],
        }
    entry = get_story(doc, story)
    if entry is None:
        return {
            "ok": True,
            "story": story,
            "pass": False,
            "undefined": True,
            "reasons": ["no gate definition"],
            "requires": [],
            "layer": None,
            "depends_on": [],
        }

    reasons: list[str] = []
    requires = list(entry.get("requires") or [])
    depends_on = list(entry.get("depends_on") or [])
    layer = entry.get("layer")
    artifacts = doc.get("artifacts") or {}

    for key in requires:
        rel = artifacts.get(key)
        if not rel:
            reasons.append(f"artifact key '{key}' has no path in artifacts map")
            continue
        path = (planning_artifacts / rel).resolve()
        if not path.is_file():
            reasons.append(f"artifact '{key}' missing at {rel}")
            continue
        status = parse_frontmatter_status(path)
        if status != "ready":
            reasons.append(
                f"artifact '{key}' status={status or 'missing'} (need ready)"
            )

    for dep in depends_on:
        dep_result = check_story(doc, dep, planning_artifacts, layers, stack + [story])
        if dep_result.get("undefined"):
            reasons.append(f"depends_on '{dep}' has no gate definition")
        elif not dep_result.get("pass"):
            reasons.append(f"depends_on '{dep}' not pass")

    # `layers` reserved for order / future soft hints — not auto-fail here.

    return {
        "ok": True,
        "story": story,
        "pass": len(reasons) == 0,
        "undefined": False,
        "reasons": reasons,
        "requires": requires,
        "layer": layer,
        "depends_on": depends_on,
    }


def order_stories(doc: dict, layers: list[str]) -> dict:
    stories = doc.get("stories") or {}
    indexed: list[tuple[int, str, dict]] = []
    unknown_idx = len(layers) if layers else 0
    for sid, entry in stories.items():
        layer = entry.get("layer")
        if layers and layer in layers:
            li = layers.index(layer)
        elif layer:
            li = unknown_idx
        else:
            li = unknown_idx + 1
        indexed.append((li, sid, entry))
    indexed.sort(key=lambda t: (t[0], t[1]))
    ordered = [
        {
            "story": sid,
            "layer": entry.get("layer"),
            "layer_index": li,
            "requires": list(entry.get("requires") or []),
            "depends_on": list(entry.get("depends_on") or []),
        }
        for li, sid, entry in indexed
    ]
    return {"ok": True, "layers": layers, "ordered": ordered}


def main() -> int:
    p = argparse.ArgumentParser(
        description="Define/view/check/order soft story gates (team/gates.json)"
    )
    p.add_argument(
        "action",
        choices=("get", "list", "set", "set-artifacts", "set-layers", "check", "order"),
    )
    p.add_argument(
        "--team-dir",
        required=True,
        help="Path to planning_artifacts/team/",
    )
    p.add_argument("--story", help="Story id (get/set/check)")
    p.add_argument("--requires", help="Comma-separated artifact keys (set)")
    p.add_argument("--layer", help="Story layer (set)")
    p.add_argument("--depends-on", help="Comma-separated story ids (set)")
    p.add_argument(
        "--map",
        help="Artifact map prd=rel/path.md,ux=... (set-artifacts)",
    )
    p.add_argument("--layers", help="Comma-separated layer order")
    p.add_argument(
        "--planning-artifacts",
        help="planning_artifacts root (check)",
    )
    args = p.parse_args()

    team_dir = Path(args.team_dir)
    try:
        doc = load_doc(team_dir)
    except (OSError, ValueError, json.JSONDecodeError) as e:
        print(json.dumps({"ok": False, "error": str(e)}))
        return 1

    if args.action == "list":
        print(
            json.dumps(
                {
                    "ok": True,
                    "path": str(_team_file(team_dir)),
                    "artifacts": doc.get("artifacts") or {},
                    "layers": doc.get("layers") or [],
                    "stories": doc.get("stories") or {},
                },
                ensure_ascii=False,
            )
        )
        return 0

    if args.action == "get":
        if not args.story:
            print(json.dumps({"ok": False, "error": "--story required"}))
            return 1
        entry = get_story(doc, args.story)
        print(
            json.dumps(
                {
                    "ok": True,
                    "story": args.story,
                    "defined": entry is not None,
                    "gate": entry,
                    "artifacts": doc.get("artifacts") or {},
                    "layers": doc.get("layers") or [],
                },
                ensure_ascii=False,
            )
        )
        return 0

    if args.action == "set":
        if not args.story:
            print(json.dumps({"ok": False, "error": "--story required"}))
            return 1
        requires = split_csv(args.requires) if args.requires is not None else None
        depends = split_csv(args.depends_on) if args.depends_on is not None else None
        # Allow clearing layer with empty string
        layer = args.layer
        entry = set_story(doc, args.story, requires, layer, depends)
        path = save_doc(team_dir, doc)
        print(
            json.dumps(
                {"ok": True, "path": str(path), "story": args.story, "gate": entry},
                ensure_ascii=False,
            )
        )
        return 0

    if args.action == "set-artifacts":
        if not args.map:
            print(json.dumps({"ok": False, "error": "--map required"}))
            return 1
        mapping = dict(doc.get("artifacts") or {})
        for part in args.map.split(","):
            if "=" not in part:
                print(json.dumps({"ok": False, "error": f"bad map entry: {part}"}))
                return 1
            k, _, v = part.partition("=")
            mapping[k.strip()] = v.strip()
        doc["artifacts"] = mapping
        path = save_doc(team_dir, doc)
        print(
            json.dumps(
                {"ok": True, "path": str(path), "artifacts": mapping},
                ensure_ascii=False,
            )
        )
        return 0

    if args.action == "set-layers":
        if args.layers is None:
            print(json.dumps({"ok": False, "error": "--layers required"}))
            return 1
        doc["layers"] = [x.strip() for x in args.layers.split(",") if x.strip()]
        path = save_doc(team_dir, doc)
        print(
            json.dumps(
                {"ok": True, "path": str(path), "layers": doc["layers"]},
                ensure_ascii=False,
            )
        )
        return 0

    if args.action == "check":
        if not args.planning_artifacts:
            print(json.dumps({"ok": False, "error": "--planning-artifacts required"}))
            return 1
        pa = Path(args.planning_artifacts)
        layers = resolve_layers(args.layers, doc, team_dir)
        if args.story:
            result = check_story(doc, args.story, pa, layers)
            print(json.dumps(result, ensure_ascii=False))
            return 0 if result.get("ok") else 1
        results = [
            check_story(doc, sid, pa, layers)
            for sid in sorted(doc.get("stories") or {})
        ]
        print(
            json.dumps(
                {
                    "ok": True,
                    "layers": layers,
                    "results": results,
                    "all_pass": all(r.get("pass") for r in results)
                    if results
                    else True,
                },
                ensure_ascii=False,
            )
        )
        return 0

    if args.action == "order":
        layers = resolve_layers(args.layers, doc, team_dir)
        print(json.dumps(order_stories(doc, layers), ensure_ascii=False))
        return 0

    print(json.dumps({"ok": False, "error": "unknown action"}))
    return 1


if __name__ == "__main__":
    sys.exit(main())
