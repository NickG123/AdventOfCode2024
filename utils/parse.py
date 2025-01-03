"""Helper functions for parsing input."""
import re
from itertools import takewhile
from typing import Iterator, TextIO


def read_lines(file: TextIO) -> Iterator[str]:
    """Read lines from a file, stripping newlines."""
    for line in file:
        yield line.strip("\r\n")


def read_number_list(file: TextIO) -> list[tuple[int, ...]]:
    """Read a list of numbers on each line of a file."""
    return [tuple([int(val) for val in line.split()]) for line in read_lines(file)]


def read_number_columns(file: TextIO) -> list[tuple[int, ...]]:
    """Read a list of columns from a file."""
    return list(zip(*read_number_list(file)))


def read_sections(file: TextIO) -> list[list[str]]:
    """Read sections from a file."""
    lines = read_lines(file)
    results = []
    while True:
        section = list(takewhile(lambda s: s, lines))
        if not section:
            break
        results.append(section)
    return results


def regex_groups(regex: re.Pattern[str], line: str) -> tuple[str, ...]:
    match = regex.match(line)
    if match is None:
        raise ValueError(f"Regex {regex} did not match line {line}")
    return match.groups()
