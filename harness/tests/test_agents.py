"""
Regression tests for agents.

Contract verification:
- YAML frontmatter structure
- Required fields: name, description
"""

import re
from pathlib import Path
from typing import Any, Dict, Optional

import pytest
import yaml


AGENTS_DIR = Path(".claude/agents")

VALID_TOOLS = {
    "Read", "Write", "Edit", "Glob", "Grep", "Bash",
    "WebFetch", "WebSearch", "Task", "TodoWrite", "LSP",
    "AskUserQuestion", "NotebookEdit",
}

VALID_MODELS = {"sonnet", "opus", "haiku", "inherit"}


def parse_frontmatter(content: str) -> Optional[Dict[str, Any]]:
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return None
    try:
        return yaml.safe_load(match.group(1))
    except yaml.YAMLError:
        return None


def get_agent_files():
    if not AGENTS_DIR.exists():
        return []
    return [f for f in AGENTS_DIR.glob("*.md") if f.name.lower() != "readme.md"]


@pytest.mark.parametrize("agent_path", get_agent_files(), ids=lambda p: p.name)
def test_agent_has_frontmatter(agent_path: Path):
    content = agent_path.read_text(encoding="utf-8")
    fm = parse_frontmatter(content)
    assert fm is not None, f"Missing frontmatter in {agent_path}"


@pytest.mark.parametrize("agent_path", get_agent_files(), ids=lambda p: p.name)
def test_agent_has_name(agent_path: Path):
    content = agent_path.read_text(encoding="utf-8")
    fm = parse_frontmatter(content)
    assert fm and "name" in fm and fm["name"]


@pytest.mark.parametrize("agent_path", get_agent_files(), ids=lambda p: p.name)
def test_agent_has_description(agent_path: Path):
    content = agent_path.read_text(encoding="utf-8")
    fm = parse_frontmatter(content)
    assert fm and "description" in fm and fm["description"]


@pytest.mark.parametrize("agent_path", get_agent_files(), ids=lambda p: p.name)
def test_agent_tools_are_valid(agent_path: Path):
    content = agent_path.read_text(encoding="utf-8")
    fm = parse_frontmatter(content)
    if fm and "tools" in fm:
        tools = fm["tools"]
        # Support both list format and comma-separated string format
        if isinstance(tools, str):
            tools = [t.strip() for t in tools.split(",")]
        invalid = [t for t in tools if t not in VALID_TOOLS]
        assert not invalid, f"Unknown tools: {invalid}"


@pytest.mark.parametrize("agent_path", get_agent_files(), ids=lambda p: p.name)
def test_agent_model_is_valid(agent_path: Path):
    content = agent_path.read_text(encoding="utf-8")
    fm = parse_frontmatter(content)
    if fm and "model" in fm:
        assert fm["model"] in VALID_MODELS
