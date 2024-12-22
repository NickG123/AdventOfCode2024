"""Day 19."""

from functools import cache
from typing import Any, Iterator, TextIO

from utils.parse import read_sections


@cache
def matches(pattern: str, towels: tuple[str, ...]) -> int:
    if pattern == "":
        return 1
    count = 0
    for towel in towels:
        if pattern.startswith(towel):
            count += matches(pattern[len(towel) :], towels)
    return count


def run(file: TextIO) -> Iterator[Any]:
    """Solution for Day 19."""
    [all_towels], patterns = read_sections(file)

    p1 = 0
    p2 = 0
    towels = tuple(all_towels.split(", "))
    for pattern in patterns:
        count = matches(pattern, towels)
        if count > 0:
            p1 += 1
        p2 += count
    yield p1
    yield p2
