"""Day 05."""
from __future__ import annotations

from collections import defaultdict
from typing import Any, Iterator, TextIO

from utils.parse import read_sections


class PageNumber:
    def __init__(self, rules: dict[str, set[str]], number: str) -> None:
        self.number = number
        self.rules = rules

    def __lt__(self, other: PageNumber) -> bool:
        if other.number in self.rules.get(self.number, {}):
            return True
        return False


def run(file: TextIO) -> Iterator[Any]:
    """Solution for Day 05."""
    raw_rules, page_orders = read_sections(file)
    rules = defaultdict(set)
    for rule in raw_rules:
        left, right = rule.split("|")
        rules[left].add(right)

    p1 = 0
    p2 = 0
    for page_order in page_orders:
        pages = [PageNumber(rules, p) for p in page_order.split(",")]
        sorted_pages = sorted(pages)
        if pages == sorted_pages:
            p1 += int(sorted_pages[len(sorted_pages) // 2].number)
        else:
            p2 += int(sorted_pages[len(sorted_pages) // 2].number)

    yield p1
    yield p2
