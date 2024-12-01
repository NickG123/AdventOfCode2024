"""Day 01."""

from collections import Counter
from typing import Any, Iterator, TextIO

from utils.parse import read_number_columns


def run(file: TextIO) -> Iterator[Any]:
    """Solution for Day 01."""
    nums1, nums2 = read_number_columns(file)
    yield sum(abs(num1 - num2) for num1, num2 in zip(sorted(nums1), sorted(nums2)))
    num2_counts = Counter(nums2)
    yield sum(num * num2_counts[num] for num in nums1)
