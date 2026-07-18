import subprocess
import sys
import unittest

from calculator import add


class CalculatorTests(unittest.TestCase):
    def test_add_returns_the_integer_sum(self) -> None:
        self.assertEqual(add(19, 23), 42)

    def test_module_cli_exposes_the_public_protocol(self) -> None:
        completed = subprocess.run(
            [sys.executable, "-m", "calculator", "add", "19", "23"],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(completed.stdout, "42\n")
