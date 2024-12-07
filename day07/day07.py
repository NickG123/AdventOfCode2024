"""Day 07."""

from typing import Any, Iterator, TextIO

from utils.parse import read_lines


def can_be_true(
    target: int,
    nums: list[int],
    curr_val: int,
    allow_concat: bool = False,
) -> bool:
    if curr_val == target and not nums:
        return True
    if curr_val > target or not nums:
        return False
    rest = nums[1:]

    return (
        can_be_true(target, rest, curr_val + nums[0], allow_concat)
        or can_be_true(target, rest, curr_val * nums[0], allow_concat)
        or (
            allow_concat
            and can_be_true(target, rest, int(str(curr_val) + str(nums[0])), True)
        )
    )


def run(file: TextIO) -> Iterator[Any]:
    """Solution for Day 07."""
    total_p1 = 0
    total_p2 = 0

    for line in read_lines(file):
        target, num_list = line.split(": ")
        nums = [int(num) for num in num_list.split(" ")]
        if can_be_true(int(target), nums[1:], nums[0]):
            total_p1 += int(target)
        elif can_be_true(int(target), nums[1:], nums[0], True):
            total_p2 += int(target)

    yield total_p1
    yield total_p1 + total_p2
