"""Helper functions for parsing input."""
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
