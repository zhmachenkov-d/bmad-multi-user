#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Run Cursor `agent` and rewrite stream-json to Claude-compatible tool_use.

bmad-eval-runner trigger detection only counts assistant tool_use events
(Skill / Read with file_path). Cursor agent emits tool_call / readToolCall
with args.path. This bridge is the adapter seam: same argv contract as agent,
stdout is JSONL the runner already understands.

Usage (adapter invocation):
  python3 skills/adapters/cursor_stream_bridge.py --cwd {cwd} -- {prompt}
  # or pass through full agent argv after -- :
  python3 skills/adapters/cursor_stream_bridge.py -- agent -p --force --trust \\
      --workspace {cwd} --output-format stream-json {prompt}
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys


def _read_args(tc: dict) -> dict:
    for key in (
        "readToolCall",
        "shellToolCall",
        "grepToolCall",
        "globToolCall",
        "writeToolCall",
        "editToolCall",
        "skillToolCall",
        "taskToolCall",
    ):
        if key in tc and isinstance(tc[key], dict):
            return key, tc[key].get("args") or {}
    # unknown shape — first *ToolCall
    for key, val in tc.items():
        if key.endswith("ToolCall") and isinstance(val, dict):
            return key, val.get("args") or {}
    return "", {}


def cursor_tool_to_claude(tool_key: str, args: dict) -> tuple[str, dict] | None:
    """Map a Cursor tool_call blob to (Claude tool name, input dict)."""
    if tool_key == "readToolCall":
        path = args.get("path") or args.get("file_path") or ""
        return "Read", {"file_path": path, "path": path}
    if tool_key == "shellToolCall":
        return "Shell", {"command": args.get("command", "")}
    if tool_key == "grepToolCall":
        return "Grep", dict(args)
    if tool_key == "globToolCall":
        return "Glob", dict(args)
    if tool_key == "writeToolCall":
        path = args.get("path") or args.get("file_path") or ""
        return "Write", {
            "file_path": path,
            "path": path,
            **{k: v for k, v in args.items() if k not in ("path", "file_path")},
        }
    if tool_key == "editToolCall":
        path = args.get("path") or args.get("file_path") or ""
        return "Edit", {
            "file_path": path,
            "path": path,
            **{k: v for k, v in args.items() if k not in ("path", "file_path")},
        }
    if tool_key == "skillToolCall":
        # Preserve whatever Cursor puts in args; detector matches skill name in JSON.
        return "Skill", dict(args)
    if tool_key:
        # Generic fallback: strip ToolCall suffix → PascalCase-ish name
        name = tool_key.replace("ToolCall", "")
        name = name[:1].upper() + name[1:] if name else "Tool"
        return name, dict(args)
    return None


def transform_line(line: str) -> list[str]:
    """Return zero or more JSONL lines to emit for one Cursor stdout line.

    Passes through non-tool events. On tool_call started/completed, also emits
    a Claude-style assistant tool_use event (file_path aliased for Read).
    """
    raw = line.strip()
    if not raw:
        return []
    try:
        ev = json.loads(raw)
    except json.JSONDecodeError:
        return [raw]

    out = [raw]
    if not isinstance(ev, dict) or ev.get("type") != "tool_call":
        return out

    # Emit once per call — prefer started (args present); skip completed duplicates
    if ev.get("subtype") not in (None, "started"):
        return out

    tc = ev.get("tool_call") or {}
    if not isinstance(tc, dict):
        return out
    tool_key, args = _read_args(tc)
    if not isinstance(args, dict):
        args = {}
    mapped = cursor_tool_to_claude(tool_key, args)
    if not mapped:
        return out
    name, inp = mapped
    claude_ev = {
        "type": "assistant",
        "message": {
            "role": "assistant",
            "content": [{"type": "tool_use", "name": name, "input": inp}],
        },
        # Keep a breadcrumb for debugging; detector ignores unknown keys.
        "_cursor_bridge": {"from": tool_key, "call_id": ev.get("call_id")},
    }
    out.append(json.dumps(claude_ev, ensure_ascii=False))
    return out


def build_agent_argv(cwd: str, prompt: str, passthrough: list[str]) -> list[str]:
    if passthrough:
        # Replace placeholders if the caller left them (adapter already expands).
        return [
            t.replace("{cwd}", cwd)
            .replace("{prompt}", prompt)
            .replace("{query}", prompt)
            for t in passthrough
        ]
    return [
        "agent",
        "-p",
        "--force",
        "--trust",
        "--workspace",
        cwd,
        "--output-format",
        "stream-json",
        prompt,
    ]


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--cwd", default=os.getcwd(), help="workspace for agent")
    p.add_argument(
        "--prompt",
        default="",
        help="prompt text (optional if prompt is last passthrough arg)",
    )
    p.add_argument(
        "passthrough",
        nargs=argparse.REMAINDER,
        help="optional full agent argv after --",
    )
    args = p.parse_args(argv)
    passthrough = list(args.passthrough or [])
    if passthrough and passthrough[0] == "--":
        passthrough = passthrough[1:]

    prompt = args.prompt
    if not prompt and passthrough:
        # Last token is the prompt when using full argv form.
        prompt = passthrough[-1]

    agent_argv = build_agent_argv(args.cwd, prompt, passthrough)
    try:
        proc = subprocess.Popen(
            agent_argv,
            stdout=subprocess.PIPE,
            stderr=sys.stderr,
            cwd=args.cwd,
            env=os.environ.copy(),
            text=True,
            bufsize=1,
        )
    except FileNotFoundError as e:
        print(json.dumps({"type": "result", "error": str(e)}))
        return 127

    assert proc.stdout is not None
    for line in proc.stdout:
        for out_line in transform_line(line):
            sys.stdout.write(out_line + "\n")
        sys.stdout.flush()
    return proc.wait()


if __name__ == "__main__":
    sys.exit(main())
