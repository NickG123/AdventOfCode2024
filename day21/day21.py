"""Day 21."""

from collections import deque
from functools import cache
from itertools import pairwise
from typing import Any, Callable, Iterator, TextIO

from utils.geometry import (
    COMPASS,
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Point2D,
    get_grid_point,
    iter_grid,
)
from utils.parse import read_lines

DIRECTION_LOOKUP = {
    UP: "^",
    DOWN: "v",
    LEFT: "<",
    RIGHT: ">",
}
NUMERIC_PAD: list[list[str | None]] = [
    ["7", "8", "9"],
    ["4", "5", "6"],
    ["1", "2", "3"],
    [None, "0", "A"],
]
DIRECTIONAL_PAD: list[list[str | None]] = [
    [None, "^", "A"],
    ["<", "v", ">"],
]


def bfs(
    grid: list[list[str | None]],
    start: Point2D,
    end: Point2D,
) -> list[list[str]]:
    queue = deque[tuple[Point2D, list[str], set[Point2D]]]([(start, [], set())])
    paths = []
    while queue:
        pos, path, visited = queue.popleft()
        visited |= {pos}
        if pos == end:
            paths.append(path + ["A"])
        for direction in COMPASS:
            new_pos = pos + direction
            if new_pos in visited:
                continue
            if get_grid_point(grid, new_pos) is not None:
                queue.append((new_pos, path + [DIRECTION_LOOKUP[direction]], visited))
    return paths


def precompute_paths(
    grid: list[list[str | None]],
) -> dict[tuple[Point2D, Point2D], list[list[str]]]:
    paths = {}
    for start_value, start in iter_grid(grid):
        if start_value is not None:
            for end_value, end in iter_grid(grid):
                if end_value is not None:
                    path = bfs(grid, start, end)
                    paths[start, end] = path
    return paths


@cache
def best_path(
    a: str,
    b: str,
    lookup: Callable[[str, str], list[list[str]]],
    next_lookup: Callable[[str, str], list[list[str]]],
    robots: int,
) -> int:
    paths = lookup(a, b)
    return min(
        compute_cost(path, next_lookup, next_lookup, robots - 1) for path in paths
    )


def compute_cost(
    path: list[str],
    lookup: Callable[[str, str], list[list[str]]],
    next_lookup: Callable[[str, str], list[list[str]]],
    robots: int,
) -> int:
    if robots == 0:
        return len(path)
    total_cost = 0
    for a, b in pairwise(["A"] + path):
        total_cost += best_path(a, b, lookup, next_lookup, robots)
    return total_cost


def compute_total_cost(
    lines: list[str],
    get_numeric_paths: Callable[[str, str], list[list[str]]],
    get_directional_paths: Callable[[str, str], list[list[str]]],
    robots: int,
) -> int:
    total_cost = 0
    for line in lines:
        cost = compute_cost(
            ["A"] + list(line), get_numeric_paths, get_directional_paths, robots
        )
        cost -= 1  # Account for the extra "A" in the path
        total_cost += int(line.rstrip("A")) * cost
    return total_cost


def run(file: TextIO) -> Iterator[Any]:
    """Solution for Day 21."""
    numeric_paths = precompute_paths(NUMERIC_PAD)
    directional_paths = precompute_paths(DIRECTIONAL_PAD)

    numeric_position_lookup = {c: pos for c, pos in iter_grid(NUMERIC_PAD)}
    directional_position_lookup = {c: pos for c, pos in iter_grid(DIRECTIONAL_PAD)}

    def get_numeric_paths(start: str, end: str) -> list[list[str]]:
        return numeric_paths[
            numeric_position_lookup[start], numeric_position_lookup[end]
        ]

    def get_directional_paths(start: str, end: str) -> list[list[str]]:
        return directional_paths[
            directional_position_lookup[start], directional_position_lookup[end]
        ]

    lines = list(read_lines(file))

    yield compute_total_cost(lines, get_numeric_paths, get_directional_paths, 3)
    yield compute_total_cost(lines, get_numeric_paths, get_directional_paths, 26)
