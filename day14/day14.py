"""Day 14."""

import operator
import re
from collections import Counter
from dataclasses import dataclass
from functools import reduce
from itertools import count
from typing import Any, Iterator, TextIO

from utils.geometry import Point2D
from utils.parse import read_lines, regex_groups

ROBOT_REGEX = re.compile(r"p=(-?\d*),(-?\d*) v=(-?\d*),(-?\d*)")
WIDTH = 101
HEIGHT = 103


@dataclass
class Robot:
    position: Point2D
    movement: Point2D

    def move(self) -> None:
        self.position = Point2D(
            (self.position.x + self.movement.x) % WIDTH,
            (self.position.y + self.movement.y) % HEIGHT,
        )


def print_robots(robots: list[Robot]) -> None:
    positions = {robot.position for robot in robots}
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if Point2D(x, y) in positions:
                print("#", end="")
            else:
                print(".", end="")
        print()
    print()


def run(file: TextIO) -> Iterator[Any]:
    """Solution for Day 14."""
    quadrants = {(0, 0): 0, (0, 1): 0, (1, 0): 0, (1, 1): 0}
    robots = []
    for line in read_lines(file):
        x, y, dx, dy = regex_groups(ROBOT_REGEX, line)
        robot = Robot(Point2D(int(x), int(y)), Point2D(int(dx), int(dy)))
        for _ in range(100):
            robot.move()

        if robot.position.x == WIDTH // 2 or robot.position.y == HEIGHT // 2:
            continue
        robots.append(robot)
        quadrants[
            (int(robot.position.x > WIDTH // 2), int(robot.position.y > HEIGHT // 2))
        ] += 1

    yield reduce(operator.mul, quadrants.values())

    for i in count(start=101):
        for robot in robots:
            robot.move()

        # Hacky way to look for a "cluster"
        # just look for a row and column with a lot of robots
        rows = Counter(robot.position.y for robot in robots)
        columns = Counter(robot.position.x for robot in robots)
        if rows.most_common(1)[0][1] > 20 and columns.most_common(1)[0][1] > 20:
            print_robots(robots)
            yield i
            break
