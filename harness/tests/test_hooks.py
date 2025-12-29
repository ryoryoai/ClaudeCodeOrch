"""
Regression tests for hooks.

Contract verification:
- stdin JSON parsing
- exit code semantics (0 = allow, 2 = block, 1 = error)
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest


HOOKS_DIR = Path("hooks")


def get_hook_scripts():
    return list(HOOKS_DIR.glob("*.py"))


@pytest.mark.parametrize("hook_path", get_hook_scripts(), ids=lambda p: p.name)
def test_hook_syntax(hook_path: Path):
    """Verify hook scripts have valid Python syntax."""
    result = subprocess.run(
        [sys.executable, "-m", "py_compile", str(hook_path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Syntax error in {hook_path}: {result.stderr}"


@pytest.mark.parametrize("hook_path", get_hook_scripts(), ids=lambda p: p.name)
def test_hook_accepts_empty_stdin(hook_path: Path):
    """Hook should handle empty stdin gracefully."""
    result = subprocess.run(
        [sys.executable, str(hook_path)],
        input="",
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert result.returncode in (0, 1)


@pytest.mark.parametrize("hook_path", get_hook_scripts(), ids=lambda p: p.name)
def test_hook_accepts_valid_json(hook_path: Path):
    """Hook should accept valid JSON and return 0 for normal input."""
    sample_input = json.dumps({
        "session_id": "test-session",
        "type": "tool_use",
        "tool": {"name": "Read", "input": {"file_path": "/tmp/test.txt"}},
        "message": {},
    })
    result = subprocess.run(
        [sys.executable, str(hook_path)],
        input=sample_input,
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert result.returncode == 0


@pytest.mark.parametrize("hook_path", get_hook_scripts(), ids=lambda p: p.name)
def test_hook_rejects_invalid_json(hook_path: Path):
    """Hook should return 1 for invalid JSON."""
    result = subprocess.run(
        [sys.executable, str(hook_path)],
        input="not valid json {{{",
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert result.returncode == 1
