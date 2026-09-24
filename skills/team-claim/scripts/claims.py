#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Soft artifact claims. Stdlib only. File: team/claims.json."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

CLAIMS_NAME = "claims.json"


def _team_file(team_dir: Path) -> Path:
    return team_dir / CLAIMS_NAME


def _empty_doc() -> dict:
    return {"claims": {}}


def load_doc(team_dir: Path) -> dict:
    path = _team_file(team_dir)
    if not path.is_file():
        return _empty_doc()
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("claims.json root must be an object")
    claims = data.get("claims")
    if claims is None:
        data["claims"] = {}
    elif not isinstance(claims, dict):
        raise ValueError("claims.json 'claims' must be an object")
    return data


def save_doc(team_dir: Path, doc: dict) -> Path:
    team_dir.mkdir(parents=True, exist_ok=True)
    path = _team_file(team_dir)
    path.write_text(
        json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return path


def normalize_target(target: str, planning_artifacts: Path | None) -> str:
    """Stable relative key when under planning_artifacts; else normalized path string."""
    raw = Path(target)
    if planning_artifacts is not None:
        pa = planning_artifacts.resolve()
        try:
            resolved = raw if raw.is_absolute() else (pa / raw)
            return resolved.resolve().relative_to(pa).as_posix()
        except (ValueError, OSError):
            pass
    if raw.is_absolute():
        return raw.as_posix()
    return raw.as_posix().lstrip("./")


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def get_claim(doc: dict, key: str) -> dict | None:
    entry = (doc.get("claims") or {}).get(key)
    return dict(entry) if isinstance(entry, dict) else None


def claim_target(
    doc: dict,
    key: str,
    actor: str,
    *,
    force: bool = False,
    note: str | None = None,
) -> dict:
    existing = get_claim(doc, key)
    if existing is not None:
        holder = existing.get("actor") or ""
        if holder == actor:
            out = {
                "ok": True,
                "target": key,
                "action": "already",
                "claim": existing,
                "conflict": False,
            }
            return out
        if not force:
            return {
                "ok": False,
                "target": key,
                "action": "conflict",
                "conflict": True,
                "claim": existing,
                "error": f"already claimed by {holder} (use --force to take over)",
            }
        previous = existing
        entry: dict = {
            "actor": actor,
            "claimed_at": now_iso(),
            "took_from": holder,
        }
        if note:
            entry["note"] = note
        doc.setdefault("claims", {})[key] = entry
        return {
            "ok": True,
            "target": key,
            "action": "takeover",
            "conflict": True,
            "previous": previous,
            "claim": entry,
        }

    entry = {"actor": actor, "claimed_at": now_iso()}
    if note:
        entry["note"] = note
    doc.setdefault("claims", {})[key] = entry
    return {
        "ok": True,
        "target": key,
        "action": "claimed",
        "conflict": False,
        "claim": entry,
    }


def release_target(doc: dict, key: str) -> dict:
    claims = doc.setdefault("claims", {})
    previous = claims.pop(key, None)
    if previous is None:
        return {
            "ok": True,
            "target": key,
            "action": "absent",
            "released": False,
            "claim": None,
        }
    return {
        "ok": True,
        "target": key,
        "action": "released",
        "released": True,
        "previous": previous,
    }


def check_target(doc: dict, key: str, actor: str | None = None) -> dict:
    existing = get_claim(doc, key)
    if existing is None:
        return {
            "ok": True,
            "target": key,
            "claimed": False,
            "conflict": False,
            "claim": None,
        }
    conflict = bool(actor and existing.get("actor") != actor)
    return {
        "ok": True,
        "target": key,
        "claimed": True,
        "conflict": conflict,
        "claim": existing,
        "holder": existing.get("actor"),
    }


def list_claims(doc: dict) -> dict:
    claims = doc.get("claims") or {}
    return {"ok": True, "claims": claims, "count": len(claims)}


def main() -> int:
    p = argparse.ArgumentParser(
        description="Soft-claim / release / check targets (team/claims.json)"
    )
    p.add_argument(
        "action",
        choices=("claim", "release", "check", "list"),
    )
    p.add_argument(
        "--team-dir",
        required=True,
        help="Path to planning_artifacts/team/",
    )
    p.add_argument("--target", help="Artifact path (abs or rel to planning_artifacts)")
    p.add_argument(
        "--planning-artifacts",
        help="planning_artifacts root (normalizes --target to a relative key)",
    )
    p.add_argument("--actor", help="Who claims (claim); optional for check conflict)")
    p.add_argument("--note", help="Optional note on claim")
    p.add_argument(
        "--force",
        action="store_true",
        help="Take over an existing claim held by someone else (soft; still records takeover)",
    )
    args = p.parse_args()

    team_dir = Path(args.team_dir)
    pa = Path(args.planning_artifacts) if args.planning_artifacts else None

    try:
        doc = load_doc(team_dir)
    except (OSError, ValueError, json.JSONDecodeError) as e:
        print(json.dumps({"ok": False, "error": str(e)}))
        return 1

    if args.action == "list":
        out = list_claims(doc)
        out["path"] = str(_team_file(team_dir))
        print(json.dumps(out, ensure_ascii=False))
        return 0

    if not args.target:
        print(json.dumps({"ok": False, "error": "--target required"}))
        return 1

    key = normalize_target(args.target, pa)

    if args.action == "check":
        out = check_target(doc, key, args.actor)
        out["path"] = str(_team_file(team_dir))
        print(json.dumps(out, ensure_ascii=False))
        return 0

    if args.action == "release":
        out = release_target(doc, key)
        path = save_doc(team_dir, doc) if out.get("released") else _team_file(team_dir)
        out["path"] = str(path)
        print(json.dumps(out, ensure_ascii=False))
        return 0

    # claim
    if not args.actor:
        print(json.dumps({"ok": False, "error": "--actor required for claim"}))
        return 1
    out = claim_target(doc, key, args.actor, force=args.force, note=args.note)
    if out.get("ok") and out.get("action") in ("claimed", "takeover"):
        path = save_doc(team_dir, doc)
        out["path"] = str(path)
    else:
        out["path"] = str(_team_file(team_dir))
    print(json.dumps(out, ensure_ascii=False))
    return 0 if out.get("ok") else 1


if __name__ == "__main__":
    sys.exit(main())
