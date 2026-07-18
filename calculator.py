"""Deliberately small public-safe fixture used by the receipt pilot."""


def add(left: int, right: int) -> int:
    """Return the exact integer sum without external I/O or side effects."""

    return left + right
