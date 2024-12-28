"""Day 22."""

from collections import defaultdict, deque
from typing import Any, Iterator, TextIO

from utils.parse import read_lines


def simulate(secret: int) -> int:
    secret = ((secret * 64) ^ secret) % 16777216
    secret = ((secret // 32) ^ secret) % 16777216
    return ((secret * 2048) ^ secret) % 16777216


def simulate_steps(secret: int, steps: int) -> tuple[int, dict[tuple[int, ...], int]]:
    deltas = deque[int](maxlen=4)
    sequences = {}
    for _ in range(steps):
        new_secret = simulate(secret)
        price_delta = (new_secret % 10) - (secret % 10)
        deltas.append(price_delta)
        if len(deltas) == 4:
            sequence = tuple(deltas)
            if sequence not in sequences:
                sequences[sequence] = new_secret % 10
        secret = new_secret
    return secret, sequences


def run(file: TextIO) -> Iterator[Any]:
    """Solution for Day 22."""
    total = 0
    bananas_per_sequence = defaultdict[tuple[int, ...], int](int)
    for line in read_lines(file):
        result, sequences = simulate_steps(int(line), 2000)
        for sequence, bananas in sequences.items():
            bananas_per_sequence[sequence] += bananas
        total += result
    yield total
    yield max(bananas_per_sequence.values())
