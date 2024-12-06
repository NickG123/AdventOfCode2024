"""Day 04."""
from __future__ import annotations

from collections import Counter
from typing import Any, Iterator, TextIO

from utils.geometry import (
    CORNERS,
    DIRECTIONS,
    DOWN_LEFT,
    UP_RIGHT,
    Point2D,
    get_grid_point,
    iter_grid,
)
from utils.parse import read_lines


def is_word(
    grid: list[list[str]],
    word: list[str],
    position: Point2D,
    direction: Point2D,
) -> bool:
    match word:
        case []:
            return True
        case [letter, *rest] if get_grid_point(grid, position) == letter:
            return is_word(
                grid,
                rest,
                position + direction,
                direction,
            )
        case _:
            return False


def count_words(grid: list[list[str]], word: list[str]) -> int:
    count = 0
    for _, position in iter_grid(grid):
        for direction in DIRECTIONS:
            if is_word(grid, word, position, direction):
                count += 1
    return count


def part2(grid: list[list[str]]) -> int:
    count = 0
    expected_corners = Counter("MMSS")
    for val, position in iter_grid(grid):
        if val == "A":
            corners = {
                direction: get_grid_point(grid, position + direction)
                for direction in CORNERS
            }
            if (
                Counter(corners.values()) == expected_corners
                and corners[UP_RIGHT] != corners[DOWN_LEFT]
            ):
                count += 1
    return count


def run(file: TextIO) -> Iterator[Any]:
    """Solution for Day 04."""
    grid = [list(line) for line in read_lines(file)]

    yield count_words(grid, list("XMAS"))
    yield part2(grid)
