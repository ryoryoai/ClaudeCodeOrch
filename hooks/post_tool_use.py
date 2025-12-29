#!/usr/bin/env python3
"""
Claude Code hook: post_tool_use

Contract:
- Reads JSON from stdin (tool_use result event)
- Exit 0: continue normally
- Exit 2: stop session (not commonly used for post hooks)
- Exit 1: error

Expected stdin schema:
{
  "session_id": "...",
  "type": "tool_result",
  "tool": { "name": "...", "input": {...} },
  "result": {...}
}
"""

import json
import sys
from typing import Any, Dict


def main() -> int:
    try:
        raw = sys.stdin.read()
        if not raw.strip():
            return 0

        data: Dict[str, Any] = json.loads(raw)

        # Example: log tool usage (in real use, could write to audit log)
        # tool = data.get("tool") or {}
        # tool_name = tool.get("name", "unknown")
        # print(f"[audit] Tool executed: {tool_name}", file=sys.stderr)

        return 0

    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Hook error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
