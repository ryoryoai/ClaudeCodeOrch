"""
Pytest configuration for harness tests.
"""

import os
import sys
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


@pytest.fixture(autouse=True)
def change_to_project_root():
    """Change to project root directory for all tests."""
    original_dir = os.getcwd()
    os.chdir(PROJECT_ROOT)
    yield
    os.chdir(original_dir)
