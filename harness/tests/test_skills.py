"""
Regression tests for skills.

Contract verification:
- YAML frontmatter structure
- Required fields: name, description, path
"""

import re
from pathlib import Path
from typing import Any, Dict, Optional

import pytest
import yaml


SKILLS_DIR = Path(".claude/skills")


def parse_frontmatter(content: str) -> Optional[Dict[str, Any]]:
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return None
    try:
        return yaml.safe_load(match.group(1))
    except yaml.YAMLError:
        return None


def get_skill_files():
    if not SKILLS_DIR.exists():
        return []
    return [f for f in SKILLS_DIR.glob("*.md") if f.name.lower() != "readme.md"]


@pytest.mark.parametrize("skill_path", get_skill_files(), ids=lambda p: p.name)
def test_skill_has_frontmatter(skill_path: Path):
    content = skill_path.read_text(encoding="utf-8")
    fm = parse_frontmatter(content)
    assert fm is not None, f"Missing frontmatter in {skill_path}"


@pytest.mark.parametrize("skill_path", get_skill_files(), ids=lambda p: p.name)
def test_skill_has_name(skill_path: Path):
    content = skill_path.read_text(encoding="utf-8")
    fm = parse_frontmatter(content)
    assert fm and "name" in fm and fm["name"]


@pytest.mark.parametrize("skill_path", get_skill_files(), ids=lambda p: p.name)
def test_skill_has_description(skill_path: Path):
    content = skill_path.read_text(encoding="utf-8")
    fm = parse_frontmatter(content)
    assert fm and "description" in fm and fm["description"]


@pytest.mark.parametrize("skill_path", get_skill_files(), ids=lambda p: p.name)
def test_skill_has_path(skill_path: Path):
    content = skill_path.read_text(encoding="utf-8")
    fm = parse_frontmatter(content)
    assert fm and "path" in fm and fm["path"].startswith("/")
