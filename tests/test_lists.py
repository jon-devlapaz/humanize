from __future__ import annotations

from collections.abc import Iterable
from typing import Any

import pytest

import humanize


@pytest.mark.parametrize(
    "test_args, expected",
    [
        ([["1", "2", "3"]], "1, 2 and 3"),
        ([["one", "two", "three"]], "one, two and three"),
        ([["one", "two"]], "one and two"),
        ([["one"]], "one"),
        ([[]], ""),
        ([[""]], ""),
        ([[1, 2, 3]], "1, 2 and 3"),
        ([[1, "two"]], "1 and two"),
        ([("one", "two", "three")], "one, two and three"),
        ([("one", "two")], "one and two"),
        ([("one",)], "one"),
        ([{"one": 1, "two": 2}.keys()], "one and two"),
        ([(x for x in ["one", "two", "three"])], "one, two and three"),
        ([range(1, 4)], "1, 2 and 3"),
    ],
)
def test_natural_list(test_args: Iterable[Any], expected: str) -> None:
    assert humanize.natural_list(*test_args) == expected


@pytest.mark.parametrize(
    "items, conjunction, expected",
    [
        ([], "or", ""),
        (["one"], "or", "one"),
        (["one", "two"], "or", "one or two"),
        (["one", "two", "three"], "or", "one, two or three"),
        (["one", "two"], "and also", "one and also two"),
        (["one", "two", "three"], "and also", "one, two and also three"),
        (["one", "two"], "and", "one and two"),
        (["one", "two"], "", "one  two"),
        (["one", "two"], " OR ", "one  OR  two"),
        (["one", "two"], "或", "one 或 two"),
        ((1, "two", 3), "or", "1, two or 3"),
        ((x for x in ["one", "two", "three"]), "or", "one, two or three"),
        (range(1, 4), "and also", "1, 2 and also 3"),
    ],
)
def test_natural_list_custom_conjunction(
    items: Iterable[Any], conjunction: str, expected: str
) -> None:
    assert humanize.natural_list(items, conjunction=conjunction) == expected


def test_natural_list_positional_conjunction() -> None:
    assert humanize.natural_list(["one", "two"], "or") == "one or two"
