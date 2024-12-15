"""Day 13."""

import re
from dataclasses import dataclass
from typing import Any, Iterator, TextIO

from utils.parse import read_sections, regex_groups

# Math time...
# We have: a * (dx1, dy1) + b (dx2, dy2) = (x, y) where only a and b are unknown.
# So we can split this into two dimensions:
# a * dx1 + b * dx2 = x
# a * dy1 + b * dy2 = y
# And solve the linear equations

# a * dx1 + b * dx2 = x
# => a * dx1 = x - b * dx2
# => a = (x - b * dx2) / dx1
#
# a * dy1 + b * dy2 = y
# => a * dy1 = y - b * dy2
# => a = (y - b * dy2) / dy1
#
# (x - b * dx2) / dx1 = (y - b * dy2) / dy1
# => dy1 * (x - b * dx2) = dx1 * (y - b * dy2)
# => dy1 * x - dy1 * b * dx2 = dx1 * y - dx1 * b * dy2
# => dy1 * x - dx1 * y = dy1 * b * dx2 - dx1 * b * dy2
# => dy1 * x - dx1 * y = b * (dy1 * dx2 - dx1 * dy2)
# => b = (dy1 * x - dx1 * y) / (dy1 * dx2 - dx1 * dy2)

# In theory we need to worry about co-linear lines (dx1 * dy2 == dx2 * dy1)
# which could have multiple solutions but there don't seem to be any instances
# in the input, meaning "minimizing" coins is irrelevant

BUTTON_REGEX = re.compile(r"Button (A|B): X\+(\d*), Y\+(\d*)")
PRIZE_REGEX = re.compile(r"Prize: X=(\d*), Y=(\d*)")


@dataclass
class ClawMachine:
    dx1: int
    dy1: int
    dx2: int
    dy2: int
    x: int
    y: int


def int_divide_or_none(num: int, denom: int) -> int | None:
    if num % denom != 0:
        return None
    if denom == 0:
        raise ValueError("Colinear solution")
    return num // denom


def solve(cm: ClawMachine) -> tuple[int, int] | None:
    # In order for the solution to be valid, a and b must be integers
    b = int_divide_or_none(
        cm.dy1 * cm.x - cm.dx1 * cm.y, cm.dy1 * cm.dx2 - cm.dx1 * cm.dy2
    )
    if b is None:
        return None
    a = int_divide_or_none(cm.x - b * cm.dx2, cm.dx1)
    if a is None:
        return None
    if a < 0 or b < 0:
        return None
    return a, b


def run(file: TextIO) -> Iterator[Any]:
    """Solution for Day 13."""
    total_cost = 0
    total_cost_p2 = 0
    for button_a, button_b, prize in read_sections(file):
        _, dx1, dy1 = regex_groups(BUTTON_REGEX, button_a)
        _, dx2, dy2 = regex_groups(BUTTON_REGEX, button_b)
        x, y = regex_groupsups(PRIZE_REGEX, prize)
        claw_machine = ClawMachine(
            int(dx1), int(dy1), int(dx2), int(dy2), int(x), int(y)
        )
        p2_claw_machine = ClawMachine(
            int(dx1),
            int(dy1),
            int(dx2),
            int(dy2),
            int(x) + 10000000000000,
            int(y) + 10000000000000,
        )
        solution = solve(claw_machine)
        if solution is not None:
            a, b = solution
            total_cost += 3 * a + b
        solution2 = solve(p2_claw_machine)
        if solution2 is not None:
            a, b = solution2
            total_cost_p2 += 3 * a + b

    yield total_cost
    yield total_cost_p2
