"""Day 02."""

from itertools import pairwise
from typing import Any, Iterator, TextIO

from utils.parse import read_number_list


def is_safe(levels: list[int], increasing: bool) -> int | None:
    for i, (level1, level2) in enumerate(pairwise(levels)):
        if (
            abs(level2 - level1) > 3
            or (level2 - level1 <= 0 and increasing)
            or (level2 - level1 >= 0 and not increasing)
        ):
            return i
    return None


def is_safe_p1(levels: list[int]) -> bool:
    return is_safe(levels, True) is None or is_safe(levels, False) is None


def is_safe_p2(levels: list[int]) -> bool:
    for direction in [True, False]:
        break_idx = is_safe(levels, direction)
        if break_idx is None:
            return True
        # Try removing next number
        remove_next = levels[break_idx:]
        remove_next.pop(1)
        if is_safe(remove_next, direction) is None:
            return True
        # Try removing current number
        if break_idx > 0:
            remove_current = levels[break_idx - 1 :]
            remove_current.pop(1)
        else:
            remove_current = levels[1:]
        if is_safe(remove_current, direction) is None:
            return True
    return False


def run(file: TextIO) -> Iterator[Any]:
    """Solution for Day 02."""
    reports = read_number_list(file)
    yield sum(is_safe_p1(list(report)) for report in reports)
    yield sum(is_safe_p2(list(report)) for report in reports)
