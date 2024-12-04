"""Day 04."""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Any, Iterator, TextIO

from utils.parse import read_lines


@dataclass(frozen=True)
class Point2D:
    x: int
    y: int

    def __add__(self, other: Point2D) -> Point2D:
        return Point2D(self.x + other.x, self.y + other.y)


UP = Point2D(0, -1)
DOWN = Point2D(0, 1)
LEFT = Point2D(-1, 0)
RIGHT = Point2D(1, 0)
UP_LEFT = Point2D(-1, -1)
UP_RIGHT = Point2D(1, -1)
DOWN_LEFT = Point2D(-1, 1)
DOWN_RIGHT = Point2D(1, 1)
DIRECTIONS = [UP, DOWN, LEFT, RIGHT, UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT]
CORNERS = [UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT]


def get_letter(grid: list[list[str]], position: Point2D) -> str | None:
    if (
        position.y < 0
        or position.y >= len(grid)
        or position.x < 0
        or position.x >= len(grid[position.y])
    ):
        return None
    return grid[position.y][position.x]


def is_word(
    grid: list[list[str]],
    word: list[str],
    position: Point2D,
    direction: Point2D,
) -> bool:
    match word:
        case []:
            return True
        case [letter, *rest] if get_letter(grid, position) == letter:
            return is_word(
                grid,
                rest,
                position + direction,
                direction,
            )
        case _:
            return False


def iter_grid(grid: list[list[str]]) -> Iterator[Point2D]:
    for y, _ in enumerate(grid):
        for x, _ in enumerate(grid[y]):
            yield Point2D(x, y)


def count_words(grid: list[list[str]], word: list[str]) -> int:
    count = 0
    for position in iter_grid(grid):
        for direction in DIRECTIONS:
            if is_word(grid, word, position, direction):
                count += 1
    return count


def part2(grid: list[list[str]]) -> int:
    count = 0
    expected_corners = Counter("MMSS")
    for position in iter_grid(grid):
        if get_letter(grid, position) == "A":
            corners = {
                direction: get_letter(grid, position + direction)
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
