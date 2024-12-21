"""Day 16."""

from collections import defaultdict
from heapq import heappop, heappush
from typing import Any, Generic, Iterator, TextIO, TypeVar

from utils.geometry import COMPASS, DOWN, LEFT, RIGHT, UP, Point2D, get_grid_point
from utils.parse import read_lines

ROTATION = {
    RIGHT: [DOWN, UP],
    LEFT: [UP, DOWN],
    UP: [RIGHT, LEFT],
    DOWN: [LEFT, RIGHT],
}

T = TypeVar("T")


# Because I don't like heapq
class Heap(Generic[T]):
    def __init__(self) -> None:
        self.heap: list[tuple[int, int, T]] = []
        self.counter = 0

    def push(self, priority: int, item: T) -> None:
        self.counter += 1
        heappush(self.heap, (priority, self.counter, item))

    def pop(self) -> tuple[int, T]:
        priority, _, item = heappop(self.heap)
        return priority, item

    @property
    def empty(self) -> bool:
        return not self.heap


def dijkstra(
    grid: list[list[str]], start: Point2D
) -> tuple[
    dict[tuple[Point2D, Point2D], int],
    dict[tuple[Point2D, Point2D], list[tuple[Point2D | None, Point2D | None]]],
]:
    direction = Point2D(1, 0)
    visited = set()
    heap = Heap[tuple[Point2D, Point2D, Point2D | None, Point2D | None]]()
    heap.push(0, (start, direction, None, None))
    previous = defaultdict(list)
    distances: dict[tuple[Point2D, Point2D], int] = {}

    while not heap.empty:
        distance, (node, direction, prev, prev_direction) = heap.pop()
        if (node, direction) not in distances or distance <= distances[
            (node, direction)
        ]:
            distances[(node, direction)] = distance
            previous[(node, direction)].append((prev, prev_direction))
        if (node, direction) in visited:
            continue
        visited.add((node, direction))
        forward = node + direction
        if get_grid_point(grid, forward) in {".", "E"}:
            heap.push(distance + 1, (forward, direction, node, direction))
        for rotation in ROTATION[direction]:
            heap.push(distance + 1000, (node, rotation, node, direction))

    return distances, previous


def print_grid(grid: list[list[str]], tiles: set[Point2D]) -> None:
    for y, row in enumerate(grid):
        for x, tile in enumerate(row):
            if x == 15 and y == 7:
                print("X", end="")
            elif Point2D(x, y) in tiles:
                print("O", end="")
            else:
                print(tile, end="")
        print()
    print()


def run(file: TextIO) -> Iterator[Any]:
    """Solution for Day 16."""
    grid = [list(line) for line in read_lines(file)]
    start = Point2D(1, len(grid) - 2)
    end = Point2D(len(grid[0]) - 2, 1)
    assert get_grid_point(grid, start) == "S"
    assert get_grid_point(grid, end) == "E"

    distances, paths = dijkstra(grid, start)
    end_direction = min(COMPASS, key=lambda direction: distances[(end, direction)])
    yield distances[(end, end_direction)]

    tiles = {start, end}
    queue = [(end, end_direction)]
    while queue:
        node, direction = queue.pop()
        for prev, prev_direction in paths[(node, direction)]:
            if prev is None or prev_direction is None or prev == start:
                continue
            tiles.add(prev)
            queue.append((prev, prev_direction))

    yield len(tiles)
