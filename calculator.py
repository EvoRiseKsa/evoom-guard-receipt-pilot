"""Deliberately small public-safe CLI fixture used by the receipt pilot."""

from __future__ import annotations

import argparse
from collections.abc import Sequence


def add(left: int, right: int) -> int:
    """Return the exact integer sum without external I/O or side effects."""

    return left + right


def main(argv: Sequence[str] | None = None) -> int:
    """Run the tiny public CLI protocol exercised by the judge-owned pack."""

    parser = argparse.ArgumentParser(description="Public-safe receipt-pilot calculator")
    commands = parser.add_subparsers(dest="command", required=True)
    add_parser = commands.add_parser("add", help="add two integers")
    add_parser.add_argument("left", type=int)
    add_parser.add_argument("right", type=int)
    arguments = parser.parse_args(argv)

    if arguments.command == "add":
        print(add(arguments.left, arguments.right))
        return 0
    raise AssertionError("argparse accepted an unknown command")


if __name__ == "__main__":
    raise SystemExit(main())
