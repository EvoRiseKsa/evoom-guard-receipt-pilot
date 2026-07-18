from calculator import add


def test_add_returns_the_integer_sum() -> None:
    assert add(19, 23) == 42
