#!/usr/bin/env python3
"""
Claude Code hook: pre_tool_use

Contract:
- Reads JSON from stdin (tool_use event)
- Exit 0: allow the tool call
- Exit 2: block the tool call
- Exit 1: error (treated as allow with warning)

Expected stdin schema:
{
  "session_id": "...",
  "type": "tool_use",
  "tool": { "name": "...", "input": {...} },
  "message": {...}
}
"""

import json
import sys
from typing import Any, Dict

# Add tools to block here
BLOCKED_TOOLS: set[str] = set()


def main() -> int:
    try:
        raw = sys.stdin.read()
        if not raw.strip():
            return 0

        data: Dict[str, Any] = json.loads(raw)

        tool = data.get("tool") or {}
        tool_name = tool.get("name", "")

        if tool_name in BLOCKED_TOOLS:
            print(f"Blocked tool: {tool_name}", file=sys.stderr)
            return 2

        return 0

    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Hook error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
