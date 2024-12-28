"""Day 25."""

from typing import Any, Iterator, TextIO

from utils.parse import read_sections


def parse(diagram: list[str]) -> tuple[int, ...]:
    result = [-1] * 5
    for row in diagram:
        for i, c in enumerate(row):
            result[i] += 1 if c == "#" else 0
    return tuple(result)


def run(file: TextIO) -> Iterator[Any]:
    """Solution for Day 25."""
    keys = []
    locks = []
    for section in read_sections(file):
        if section[0] == "#####":
            locks.append(parse(section))
        elif section[0] == ".....":
            keys.append(parse(section))
        else:
            raise ValueError("Invalid section")

    fits = 0
    for key in keys:
        for lock in locks:
            if all(a + b <= 5 for a, b in zip(key, lock)):
                fits += 1

    yield fits
