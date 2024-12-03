"""Day 03."""

import re
from typing import Any, Iterator, TextIO

from utils.parse import read_lines

mul_regex = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don't\(\)")


def run(file: TextIO) -> Iterator[Any]:
    """Solution for Day 03."""
    result_p1 = 0
    result_p2 = 0
    enabled = True
    for line in read_lines(file):
        for step in mul_regex.finditer(line):
            match step.group(0):
                case "do()":
                    enabled = True
                case "don't()":
                    enabled = False
                case _:
                    mul = int(step.group(1)) * int(step.group(2))
                    result_p1 += mul
                    if enabled:
                        result_p2 += mul
    yield result_p1
    yield result_p2
