"""Helper functions for geometry."""
from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Iterator, TypeVar


@dataclass(frozen=True)
class Point2D:
    x: int
    y: int

    def __add__(self, other: Point2D) -> Point2D:
        return Point2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Point2D) -> Point2D:
        return Point2D(self.x - other.x, self.y - other.y)


UP = Point2D(0, -1)
DOWN = Point2D(0, 1)
LEFT = Point2D(-1, 0)
RIGHT = Point2D(1, 0)
UP_LEFT = Point2D(-1, -1)
UP_RIGHT = Point2D(1, -1)
DOWN_LEFT = Point2D(-1, 1)
DOWN_RIGHT = Point2D(1, 1)
DIRECTIONS = [UP, DOWN, LEFT, RIGHT, UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT]
COMPASS = [UP, DOWN, LEFT, RIGHT]
CORNERS = [UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT]


T = TypeVar("T")
Grid = Sequence[Sequence[T]]


def get_grid_point(grid: Grid[T], position: Point2D) -> T | None:
    if (
        position.y < 0
        or position.y >= len(grid)
        or position.x < 0
        or position.x >= len(grid[position.y])
    ):
        return None
    return grid[position.y][position.x]


def iter_grid(grid: Grid[T]) -> Iterator[tuple[T, Point2D]]:
    for y, line in enumerate(grid):
        for x, val in enumerate(line):
            yield val, Point2D(x, y)
