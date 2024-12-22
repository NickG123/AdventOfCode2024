"""Day 17."""

import re
from enum import Enum
from typing import Any, Iterator, TextIO

from utils.parse import read_sections, regex_groups

REGISTER_REGEX = re.compile(r"Register \w: (\d*)")
PROGRAM_REGEX = re.compile(r"Program: ([\d,]*)")


class OPCode(Enum):
    adv = 0
    bxl = 1
    bst = 2
    jnz = 3
    bxc = 4
    out = 5
    bdv = 6
    cdv = 7


# Manual work time
# This program has some nice properties so might not be so bad
# 2,4 -> BST 4 -> B = (A % 8)
# 1,5 -> BXL 5 -> B = B ^ 5
# 7,5 -> CDV 5 -> C = A // 2**B
# 1,6 -> BXL 6 -> B = B ^ 6
# 0,3 -> ADV 3 -> A = A // 8
# 4,6 -> BXC 6 -> B = B ^ C
# 5,5 -> OUT 5 -> output B
# 3,0 -> JNZ 0 -> if A != 0: goto 0
def full_program(A: int) -> list[int]:
    result = []
    while A != 0:
        B = A % 8
        B ^= 5
        C = A // 2**B
        B ^= 6
        A //= 8
        B ^= C
        result.append(B % 8)
    return result


# So we know:
# - The program will loop until A == 0
# - A decreases by a factor of 8 each iteration and is otherwise unchanged
# - A value is output each iteration
# - The minimum value of A is 8**16, since the output program is 16 characters
# - B and C are reset each iteration, so we don't have to worry about their leftover values
# - So for any given "A", we can compute the output of the program for one step
def run_one(A: int) -> int:
    B = A % 8
    B ^= 5
    C = A // 2**B
    B ^= 6
    B ^= C
    return B % 8


# Starting from the end of the program and working our way to the front, we know for each
# value of A, its successor must be in the range of (A * 8, A * 8 + 8) (since A' // 8 == A)
#
# There are some "local" solutions which do not work for the entire program, so we need
# to backtrack and keep checking until we find a solution that works for the entire program
def compute_a(a: int, expected_outputs: list[int]) -> int | None:
    for a in range(a, a + 8):
        if run_one(a) == expected_outputs[0]:
            if len(expected_outputs) == 1:
                return a
            next_a = compute_a(a * 8, expected_outputs[1:])
            if next_a is not None:
                return next_a
    return None


def combo_operand(operand: int, *registers: int) -> int:
    if operand >= 7:
        raise Exception(f"Invalid operand {operand}")
    if operand < 4:
        return operand
    return registers[operand - 4]


def run(file: TextIO) -> Iterator[Any]:
    """Solution for Day 17."""
    registers, program = read_sections(file)
    register_a = int(regex_groups(REGISTER_REGEX, registers[0])[0])
    register_b = int(regex_groups(REGISTER_REGEX, registers[1])[0])
    register_c = int(regex_groups(REGISTER_REGEX, registers[2])[0])
    [instruction_string] = regex_groups(PROGRAM_REGEX, program[0])
    instructions = [int(x) for x in instruction_string.split(",")]
    instruction_pointer = 0

    output = []
    while instruction_pointer < len(instructions):
        opcode, operand = instructions[instruction_pointer : instruction_pointer + 2]
        combo_operand_value = combo_operand(operand, register_a, register_b, register_c)
        match OPCode(opcode):
            case OPCode.adv:
                register_a //= 2**combo_operand_value
            case OPCode.bxl:
                register_b ^= operand
            case OPCode.bst:
                register_b = combo_operand_value % 8
            case OPCode.jnz:
                if register_a != 0:
                    instruction_pointer = operand
                    continue
            case OPCode.bxc:
                register_b ^= register_c
            case OPCode.out:
                output.append(combo_operand_value % 8)
            case OPCode.cdv:
                register_c = register_a // 2**combo_operand_value
            case _:
                print(f"Unknown opcode {opcode}")
                break
        instruction_pointer += 2
    yield ",".join(str(x) for x in output)
    assert full_program(51064159) == output
    yield compute_a(0, list(reversed(instructions)))
