"""Day 18."""

from collections import deque
from typing import Any, Iterator, TextIO

from utils.geometry import COMPASS, Point2D
from utils.parse import read_lines

WIDTH = 71
HEIGHT = 71
OBSTACLE_COUNT = 1024


def bfs(
    width: int, height: int, obstacles: set[Point2D], start: Point2D, end: Point2D
) -> list[Point2D] | None:
    queue = deque[tuple[Point2D, list[Point2D]]]([(start, [])])
    visited = {start}
    while queue:
        pos, steps = queue.popleft()
        if pos == end:
            return steps
        for d in COMPASS:
            new_pos = pos + d
            if new_pos in visited:
                continue
            if new_pos in obstacles:
                continue
            if 0 <= new_pos.x < width and 0 <= new_pos.y < height:
                visited.add(new_pos)
                queue.append((new_pos, steps + [new_pos]))
    return None


def run(file: TextIO) -> Iterator[Any]:
    """Solution for Day 18."""
    obstacle_list = [
        Point2D(*[int(c) for c in line.split(",")]) for line in read_lines(file)
    ]
    obstacles = set(obstacle_list[:OBSTACLE_COUNT])
    remaining_obstacles = obstacle_list[OBSTACLE_COUNT:]
    path_list = bfs(
        WIDTH, HEIGHT, obstacles, Point2D(0, 0), Point2D(WIDTH - 1, HEIGHT - 1)
    )
    assert path_list is not None
    yield len(path_list)

    path = set(path_list)
    for obstacle in remaining_obstacles:
        obstacles.add(obstacle)
        if obstacle in path:
            path_list = bfs(
                WIDTH, HEIGHT, obstacles, Point2D(0, 0), Point2D(WIDTH - 1, HEIGHT - 1)
            )
            if path_list is None:
                yield obstacle
                break
            path = set(path_list)
