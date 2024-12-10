"""Day 10."""

from functools import cache
from typing import Any, Iterator, TextIO

from utils.geometry import COMPASS, Point2D, get_grid_point, iter_grid
from utils.parse import read_lines


@cache
def get_trailhead_score(grid: tuple[tuple[int]], position: Point2D) -> list[Point2D]:
    current_height = grid[position.y][position.x]
    if current_height == 9:
        return [position]

    results = []
    for direction in COMPASS:
        new_position = position + direction
        new_value = get_grid_point(grid, new_position)
        if new_value is not None and new_value == current_height + 1:
            results.extend(get_trailhead_score(grid, new_position))
    return results


def run(file: TextIO) -> Iterator[Any]:
    """Solution for Day 10."""
    grid = tuple(tuple(int(c) for c in line) for line in read_lines(file))
    trails = [
        get_trailhead_score(grid, position)
        for val, position in iter_grid(grid)
        if val == 0
    ]

    yield sum([len(set(trail)) for trail in trails])
    yield sum([len(trail) for trail in trails])
