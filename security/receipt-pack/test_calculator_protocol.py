"""Judge-owned black-box protocol checks for the public calculator fixture."""

from __future__ import annotations

import os
import subprocess
import sys

import pytest


if not os.environ.get("EVOGUARD_EXEC"):
    pytest.skip(
        "receipt-pilot verifier pack runs only under the EvoOM Guard judge",
        allow_module_level=True,
    )


def _run(*arguments: str) -> str:
    """Exercise the candidate only through Guard's delivered launcher."""

    launcher = os.environ["EVOGUARD_EXEC"]
    python = os.environ.get("EVOGUARD_PYTHON") or sys.executable
    completed = subprocess.run(
        [launcher, python, "-m", "calculator", "add", *arguments],
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr
    return completed.stdout.strip()


def test_addition_is_correct() -> None:
    assert _run("19", "23") == "42"


def test_addition_is_commutative() -> None:
    assert _run("7", "5") == _run("5", "7")
