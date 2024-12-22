"""Day 20."""

from typing import Any, Iterator, TextIO

from utils.geometry import COMPASS, Point2D, get_grid_point
from utils.parse import read_lines


def bfs(
    grid: list[list[str]],
    start: Point2D,
    end: Point2D,
) -> dict[Point2D, int]:
    queue = [(end, 0)]
    distances = {end: 0}
    while queue:
        pos, distance = queue.pop(0)
        if pos == start:
            break
        for direction in COMPASS:
            new_pos = pos + direction
            if new_pos in distances:
                continue
            if get_grid_point(grid, new_pos) == ".":
                distances[new_pos] = distance + 1
                queue.append((new_pos, distance + 1))
    return distances


def get_savings(
    grid: list[list[str]], path: dict[Point2D, int], distance: int
) -> list[int]:
    results = []
    for point in path:
        results.extend(find_cheats(grid, path, point, distance))
    return results


def find_cheats(
    grid: list[list[str]], path: dict[Point2D, int], start: Point2D, distance: int
) -> list[int]:
    result = []
    for x_offset in range(-distance, distance + 1):
        remaining_distance = distance - abs(x_offset)
        for y_offset in range(-remaining_distance, remaining_distance + 1):
            p = Point2D(start.x + x_offset, start.y + y_offset)
            if get_grid_point(grid, p) == ".":
                savings = path[start] - path[p] - abs(x_offset) - abs(y_offset)
                if savings > 0:
                    result.append(savings)
    return result


def run(file: TextIO) -> Iterator[Any]:
    """Solution for Day 20."""
    grid = []
    for y, line in enumerate(read_lines(file)):
        row = []
        for x, c in enumerate(line):
            if c == "S":
                start = Point2D(x, y)
                row.append(".")
            elif c == "E":
                end = Point2D(x, y)
                row.append(".")
            else:
                row.append(c)
        grid.append(row)

    path = bfs(grid, start, end)
    savings = get_savings(grid, path, 2)
    savings_p2 = get_savings(grid, path, 20)
    yield len([x for x in savings if x >= 100])
    yield len([x for x in savings_p2 if x >= 100])
