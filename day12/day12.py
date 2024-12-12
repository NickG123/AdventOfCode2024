"""Day 12."""

from collections import defaultdict
from itertools import pairwise
from typing import Any, Iterator, TextIO

from utils.geometry import COMPASS, LEFT, RIGHT, Point2D, get_grid_point, iter_grid
from utils.parse import read_lines


class Region:
    def __init__(self, char: str) -> None:
        self.char = char
        self.points: set[Point2D] = set()
        self.borders: dict[Point2D, dict[int, list[int]]] = {
            dir: defaultdict(list) for dir in COMPASS
        }

    @property
    def area(self) -> int:
        return len(self.points)

    @property
    def perimeter(self) -> int:
        return sum(
            len(borders)
            for directional_borders in self.borders.values()
            for borders in directional_borders.values()
        )

    @property
    def edges(self) -> int:
        edge_count = 0
        for border in self.borders.values():
            for dimension in border.values():
                edge_count += 1
                for offset, next_offset in pairwise(sorted(dimension)):
                    if next_offset != offset + 1:
                        edge_count += 1
        return edge_count

    def explore(self, grid: list[list[str]], point: Point2D) -> None:
        stack = [point]
        while stack:
            p = stack.pop()
            if p in self.points:
                continue
            self.points.add(p)
            for direction in COMPASS:
                n = p + direction
                if get_grid_point(grid, n) == self.char:
                    stack.append(n)
                else:
                    if direction in {LEFT, RIGHT}:
                        self.borders[direction][p.x].append(p.y)
                    else:
                        self.borders[direction][p.y].append(p.x)


def run(file: TextIO) -> Iterator[Any]:
    """Solution for Day 12."""
    grid = [list(line) for line in read_lines(file)]
    regions = []
    region_lookup = {}

    for v, p in iter_grid(grid):
        if p in region_lookup:
            continue
        region = Region(v)
        region.explore(grid, p)
        regions.append(region)
        region_lookup.update({point: region for point in region.points})

    yield sum(region.perimeter * region.area for region in regions)
    yield sum(region.edges * region.area for region in regions)
