"""Day 23."""

from collections import defaultdict
from typing import Any, Iterator, TextIO

from utils.parse import read_lines


def find_triangles(connections: dict[str, set[str]]) -> set[tuple[str, ...]]:
    triangles = set()
    for start in connections:
        for end in connections[start]:
            for third in connections[end]:
                if start in connections[third]:
                    triangle = tuple(sorted([start, end, third]))
                    triangles.add(triangle)
    return triangles


# A quick google search says this is the easiest solution
def bron_kerbosch(
    R: set[str], P: set[str], X: set[str], connections: dict[str, set[str]]
) -> set[str] | None:
    if not P and not X:
        return R
    max_set = None
    for v in P.copy():
        result = bron_kerbosch(
            R | {v}, P & connections[v], X & connections[v], connections
        )
        if result is not None and (max_set is None or len(result) > len(max_set)):
            max_set = result
        P.remove(v)
        X.add(v)
    return max_set


def run(file: TextIO) -> Iterator[Any]:
    """Solution for Day 23."""
    connections = defaultdict[str, set[str]](set)
    for line in read_lines(file):
        start, end = line.split("-")
        connections[start].add(end)
        connections[end].add(start)

    triangles = find_triangles(connections)
    triangles_with_t = {
        triangle for triangle in triangles if any(n.startswith("t") for n in triangle)
    }
    yield len(triangles_with_t)
    p2 = bron_kerbosch(set(), set(connections.keys()), set(), connections)
    assert p2 is not None
    yield ",".join(sorted(p2))
