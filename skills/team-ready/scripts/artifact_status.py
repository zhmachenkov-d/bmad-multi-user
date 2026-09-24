#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Get or set YAML frontmatter `status` on a markdown artifact. Stdlib only."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ALLOWED = ("draft", "review", "ready")
FM_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n?", re.DOTALL)


def parse_frontmatter(text: str) -> tuple[dict[str, str], str, str]:
    """Return (fields, body, raw_fm_block_or_empty)."""
    m = FM_RE.match(text)
    if not m:
        return {}, text, ""
    raw = m.group(1)
    fields: dict[str, str] = {}
    for line in raw.splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        fields[key.strip()] = val.strip().strip("\"'")
    body = text[m.end() :]
    return fields, body, raw


def render_frontmatter(
    fields: dict[str, str], preferred_order: list[str] | None = None
) -> str:
    order = preferred_order or []
    keys = [k for k in order if k in fields] + [k for k in fields if k not in order]
    lines = [f"{k}: {fields[k]}" for k in keys]
    return "---\n" + "\n".join(lines) + "\n---\n"


def get_status(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    fields, _, _ = parse_frontmatter(text)
    status = fields.get("status")
    return {
        "ok": True,
        "path": str(path),
        "has_frontmatter": bool(fields) or text.startswith("---"),
        "status": status,
        "known": status in ALLOWED if status is not None else False,
        "allowed": list(ALLOWED),
    }


def set_status(path: Path, status: str, actor: str | None) -> dict:
    if status not in ALLOWED:
        return {
            "ok": False,
            "error": f"status must be one of {ALLOWED}",
            "path": str(path),
        }
    text = path.read_text(encoding="utf-8")
    fields, body, _ = parse_frontmatter(text)
    previous = fields.get("status")
    # Preserve key order when possible
    preferred = list(fields.keys())
    if "status" not in preferred:
        preferred = ["title", "status", "created", "updated"] + preferred
    fields["status"] = status
    if actor:
        fields["status_set_by"] = actor
    new_text = render_frontmatter(fields, preferred) + body.lstrip("\n")
    if not body.endswith("\n") and body:
        new_text = new_text.rstrip("\n") + "\n"
    path.write_text(new_text, encoding="utf-8")
    return {
        "ok": True,
        "path": str(path),
        "previous": previous,
        "status": status,
        "actor": actor,
        "changed": previous != status,
    }


def main() -> int:
    p = argparse.ArgumentParser(description="Get or set markdown frontmatter status")
    p.add_argument("action", choices=("get", "set"), help="get or set status")
    p.add_argument("--path", required=True, help="Path to markdown artifact")
    p.add_argument("--status", choices=ALLOWED, help="New status (set only)")
    p.add_argument("--actor", default=None, help="Who set the status (optional)")
    args = p.parse_args()

    path = Path(args.path)
    if not path.is_file():
        print(json.dumps({"ok": False, "error": "file not found", "path": str(path)}))
        return 1

    if args.action == "get":
        print(json.dumps(get_status(path), ensure_ascii=False))
        return 0

    if not args.status:
        print(json.dumps({"ok": False, "error": "--status required for set"}))
        return 1
    result = set_status(path, args.status, args.actor)
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    sys.exit(main())
