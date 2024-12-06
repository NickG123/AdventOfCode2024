"""Day 06."""

from typing import Any, Iterator, TextIO

from utils.geometry import DOWN, LEFT, RIGHT, UP, Point2D, get_grid_point, iter_grid
from utils.parse import read_lines

NEXT_DIRECTION = {UP: RIGHT, RIGHT: DOWN, DOWN: LEFT, LEFT: UP}


def follow_route(
    grid: list[list[str]],
    position: Point2D,
    direction: Point2D,
    extra_obstacle: Point2D | None = None,
) -> set[tuple[Point2D, Point2D]] | None:
    visited = {(position, direction)}
    while True:
        new_position = position + direction
        if new_position == extra_obstacle:
            direction = NEXT_DIRECTION[direction]
            continue
        match get_grid_point(grid, new_position):
            case "." | "^":
                if (new_position, direction) in visited:
                    return None
                position = new_position
                visited.add((position, direction))
            case "#":
                direction = NEXT_DIRECTION[direction]
            case _:
                return visited


def run(file: TextIO) -> Iterator[Any]:
    """Solution for Day 06."""
    grid = [list(line) for line in read_lines(file)]
    for val, pos in iter_grid(grid):
        if val == "^":
            current_position = pos
            break

    main_route = follow_route(grid, current_position, UP)
    assert main_route is not None
    visited_spaces = {pos for pos, _ in main_route}

    yield len(visited_spaces)

    possible_loops = 0
    for pos in visited_spaces:
        if (
            get_grid_point(grid, pos) != "^"
            and follow_route(grid, current_position, UP, pos) is None
        ):
            possible_loops += 1
    yield possible_loops
