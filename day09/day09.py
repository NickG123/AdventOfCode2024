"""Day 09."""

from dataclasses import dataclass
from typing import Any, Iterator, TextIO

from utils.parse import read_lines


@dataclass
class File:
    size: int
    file_id: int


def checksum(offset: int, file_id: int, size: int) -> int:
    offset_sum = size * (2 * offset + size - 1) // 2
    return file_id * offset_sum


def part_1(files: list[File | int]) -> int:
    l_iter = enumerate(files)
    r_iter = reversed(list(enumerate(files)))

    l_idx, l_file = next(l_iter)
    r_idx, r_file = next(r_iter)

    results = []

    while l_idx <= r_idx:
        match (l_file, r_file):
            case (File(), _):
                results.append(l_file)
                l_idx, l_file = next(l_iter)
            case (_, int()):
                r_idx, r_file = next(r_iter)
            case (0, _):
                l_idx, l_file = next(l_iter)
            case (_, File(size=0)):
                r_idx, r_file = next(r_iter)
            case (int(), File()):
                if l_file >= r_file.size:
                    results.append(r_file)
                    l_file -= r_file.size
                    r_idx, r_file = next(r_iter)
                else:
                    results.append(File(size=l_file, file_id=r_file.file_id))
                    r_file.size -= l_file
                    l_idx, l_file = next(l_iter)

    offset = 0
    total_checksum = 0
    for result in results:
        total_checksum += checksum(offset, result.file_id, result.size)
        offset += result.size
    return total_checksum


def part_2(files_and_gaps: list[File | int]) -> int:
    gaps = []
    files = []
    offset = 0
    for f in files_and_gaps:
        if isinstance(f, File):
            files.append((f, offset))
            offset += f.size
        else:
            gaps.append((f, offset))
            offset += f

    total_checksum = 0
    for file, file_offset in reversed(files):
        for i, (gap, gap_offset) in enumerate(gaps):
            if gap_offset > file_offset:
                total_checksum += checksum(file_offset, file.file_id, file.size)
                break
            if gap >= file.size:
                if gap == file.size:
                    gaps.pop(i)
                else:
                    gaps[i] = (gap - file.size, gap_offset + file.size)
                total_checksum += checksum(gap_offset, file.file_id, file.size)
                break
        else:
            total_checksum += checksum(file_offset, file.file_id, file.size)

    return total_checksum


def run(file: TextIO) -> Iterator[Any]:
    """Solution for Day 09."""
    file.seek(0)
    files: list[File | int] = [
        File(int(c), i // 2) if i % 2 == 0 else int(c)
        for i, c in enumerate(next(read_lines(file)))
    ]

    p2 = part_2(files)
    p1 = part_1(files)
    yield p1
    yield p2
