#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Unit tests for cursor_stream_bridge transform."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from cursor_stream_bridge import transform_line


class BridgeTransformTests(unittest.TestCase):
    def test_read_emits_claude_tool_use_with_file_path(self) -> None:
        cursor = {
            "type": "tool_call",
            "subtype": "started",
            "call_id": "c1",
            "tool_call": {
                "readToolCall": {
                    "args": {
                        "path": "/tmp/stage/.cursor/skills/team-status-trig-abc/SKILL.md"
                    }
                }
            },
        }
        lines = transform_line(json.dumps(cursor))
        self.assertEqual(len(lines), 2)
        claude = json.loads(lines[1])
        self.assertEqual(claude["type"], "assistant")
        item = claude["message"]["content"][0]
        self.assertEqual(item["type"], "tool_use")
        self.assertEqual(item["name"], "Read")
        self.assertIn("team-status-trig-abc", item["input"]["file_path"])

    def test_completed_does_not_duplicate(self) -> None:
        cursor = {
            "type": "tool_call",
            "subtype": "completed",
            "tool_call": {"readToolCall": {"args": {"path": "/x/SKILL.md"}}},
        }
        lines = transform_line(json.dumps(cursor))
        self.assertEqual(len(lines), 1)

    def test_detect_load_compatible(self) -> None:
        # Import vendor detector without editing it.
        root = (
            Path(__file__).resolve().parents[3]
            / ".agents/skills/bmad-eval-runner/scripts"
        )
        sys.path.insert(0, str(root))
        from run_triggers import detect_load

        cursor = {
            "type": "tool_call",
            "subtype": "started",
            "tool_call": {
                "readToolCall": {
                    "args": {
                        "path": "/stage/.cursor/skills/team-status-trig-deadbeef/SKILL.md"
                    }
                }
            },
        }
        transcript = "\n".join(transform_line(json.dumps(cursor)))
        self.assertTrue(
            detect_load(
                transcript,
                {"skill_tool": "Skill", "read_tool": "Read"},
                "team-status-trig-deadbeef",
            )
        )
        self.assertFalse(
            detect_load(
                transcript,
                {"skill_tool": "Skill", "read_tool": "Read"},
                "other-skill-trig-00000000",
            )
        )


if __name__ == "__main__":
    unittest.main()
