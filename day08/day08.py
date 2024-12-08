"""Day 08."""

from collections import defaultdict
from itertools import combinations
from typing import Any, Iterator, TextIO

from utils.geometry import Point2D
from utils.parse import read_lines


def in_range(width: int, height: int, point: Point2D) -> bool:
    """Check if a point is in range."""
    return 0 <= point.x < width and 0 <= point.y < height


def run(file: TextIO) -> Iterator[Any]:
    """Solution for Day 08."""
    antennae = defaultdict(list)
    for y, line in enumerate(read_lines(file)):
        height = y + 1
        width = len(line)
        for x, char in enumerate(line):
            if char != ".":
                antennae[char].append(Point2D(x, y))

    antinodes = set()
    antinodes_p2 = set()
    for _, points in antennae.items():
        for point_a, point_b in combinations(points, 2):
            delta = Point2D(point_b.x - point_a.x, point_b.y - point_a.y)
            p = point_a - delta
            if in_range(width, height, p):
                antinodes.add(p)
            p = point_b + delta
            if in_range(width, height, p):
                antinodes.add(p)

            p = point_a
            while in_range(width, height, p):
                antinodes_p2.add(p)
                p -= delta
            p = point_b
            while in_range(width, height, p):
                antinodes_p2.add(p)
                p += delta

    yield len(antinodes)
    yield len(antinodes_p2)
