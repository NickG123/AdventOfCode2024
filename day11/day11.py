"""Day 11."""

from functools import cache
from typing import Any, Iterator, TextIO

from utils.parse import read_lines


def mutate(stone: int) -> list[int]:
    if stone == 0:
        return [1]
    stone_str = str(stone)
    if len(stone_str) % 2 == 0:
        return [
            int(stone_str[: len(stone_str) // 2]),
            int(stone_str[len(stone_str) // 2 :]),
        ]
    return [stone * 2024]


@cache
def blink(stone: int, steps: int) -> int:
    if steps == 0:
        return 1
    return sum(blink(mutation, steps - 1) for mutation in mutate(stone))


def run(file: TextIO) -> Iterator[Any]:
    """Solution for Day 11."""
    stones = [int(c) for c in next(read_lines(file)).split()]
    yield sum(blink(stone, 25) for stone in stones)
    yield sum(blink(stone, 75) for stone in stones)
