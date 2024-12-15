"""Day 15."""

from collections import deque
from typing import Any, Iterator, TextIO

from utils.geometry import DOWN, LEFT, RIGHT, UP, Point2D, iter_grid
from utils.parse import read_sections

DIRECTION_LOOKUP = {
    "<": LEFT,
    ">": RIGHT,
    "^": UP,
    "v": DOWN,
}


def move_obj(positions: dict[Point2D, str], pos: Point2D, new_pos: Point2D) -> None:
    positions[new_pos] = positions[pos]
    positions[pos] = "."


def make_move(positions: dict[Point2D, str], pos: Point2D, direction: Point2D) -> bool:
    search_queue = deque([pos + direction])
    moved_objects = set()
    while search_queue:
        new_pos = search_queue.popleft()
        new_val = positions[new_pos]
        match (new_val, direction):
            case ".", _:
                continue
            case ("O", _) | (("[" | "]"), Point2D(_, 0)):
                moved_objects.add(new_pos)
                search_queue.append(new_pos + direction)
            case ("[" | "]", Point2D(0, _)):
                offset = RIGHT if new_val == "[" else LEFT
                moved_objects.add(new_pos)
                moved_objects.add(new_pos + offset)
                search_queue.append(new_pos + direction)
                search_queue.append(new_pos + direction + offset)
            case "#", _:
                return False
            case _:
                raise ValueError(
                    f"Unknown object at {new_pos} with direction {direction}: {positions[new_pos]}"
                )
    for obj in sorted(
        moved_objects,
        key=lambda p: (p.y * direction.y, p.x * direction.x),
        reverse=True,
    ):
        move_obj(positions, obj, obj + direction)
    return True


def run(file: TextIO) -> Iterator[Any]:
    """Solution for Day 15."""
    [starting_grid, moves] = read_sections(file)

    positions = {}
    positions_p2 = {}
    robot = None
    for obj, pos in iter_grid(starting_grid):
        p2_pos = Point2D(pos.x * 2, pos.y)
        p2_pos2 = Point2D(pos.x * 2 + 1, pos.y)
        if obj == "@":
            robot = pos
            robot_p2 = p2_pos
            positions_p2[p2_pos] = "@"
            positions_p2[p2_pos2] = "."
        elif obj == "O":
            positions_p2[p2_pos] = "["
            positions_p2[p2_pos2] = "]"
        else:
            positions_p2[p2_pos] = obj
            positions_p2[p2_pos2] = obj

        positions[pos] = obj
    assert robot is not None
    assert robot_p2 is not None

    for move in "".join(moves):
        direction = DIRECTION_LOOKUP[move]
        moved = make_move(positions, robot, direction)
        if moved:
            move_obj(positions, robot, robot + direction)
            robot = robot + direction

        moved = make_move(positions_p2, robot_p2, direction)
        if moved:
            move_obj(positions_p2, robot_p2, robot_p2 + direction)
            robot_p2 = robot_p2 + direction

    yield sum(pos.x + 100 * pos.y for pos, obj in positions.items() if obj == "O")
    yield sum(pos.x + 100 * pos.y for pos, obj in positions_p2.items() if obj == "[")
