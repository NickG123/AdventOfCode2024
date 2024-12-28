"""Day 24."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterator, TextIO

from utils.parse import read_sections


@dataclass
class Rule:
    input1: str
    input2: str
    output: str
    operation: str
    swapped: bool = False
    value: int | None = None
    visited: bool = False

    def reset(self) -> None:
        self.value = None
        self.visited = False

    def solve(self, rules: dict[str, Rule], initial_values: dict[str, int]) -> int:
        if self.value is None:
            if self.visited:
                raise ValueError("Circular dependency")
            self.visited = True
            v1 = get_input_value(self.input1, rules, initial_values)
            v2 = get_input_value(self.input2, rules, initial_values)

            match self.operation:
                case "AND":
                    self.value = v1 & v2
                case "OR":
                    self.value = v1 | v2
                case "XOR":
                    self.value = v1 ^ v2
                case _:
                    raise ValueError(f"Unknown operation: {self.operation}")
        return self.value


def get_input_value(
    name: str, rules: dict[str, Rule], initial_values: dict[str, int]
) -> int:
    if name in initial_values:
        return initial_values[name]
    return rules[name].solve(rules, initial_values)


def int_to_iv(prefix: str, value: int, num_bits: int) -> dict[str, int]:
    return {f"{prefix}{i:02}": (value >> i) & 1 for i in range(num_bits)}


def evaluate(rules: dict[str, Rule], num_bits: int, x: int, y: int) -> int:
    for rule in rules.values():
        rule.reset()
    initial_values = int_to_iv("x", x, num_bits) | int_to_iv("y", y, num_bits)
    return compute_z(
        rules,
        initial_values,
    )


def compute_z(rules: dict[str, Rule], initial_values: dict[str, int]) -> int:
    z_rules = sorted(
        [rule for wire, rule in rules.items() if wire.startswith("z")],
        key=lambda r: r.output,
    )
    return sum(rule.solve(rules, initial_values) << i for i, rule in enumerate(z_rules))


def is_bit_correct(rules: dict[str, Rule], bit: int, num_bits: int) -> bool:
    for x_bit, y_bit, expected_bit, expected_greater_bit in [
        (0, 0, 0, 0),
        (1, 0, 1, 0),
        (0, 1, 1, 0),
        (1, 1, 0, 1),
    ]:
        x = x_bit << bit
        y = y_bit << bit
        expected = (expected_bit << bit) | (expected_greater_bit << (bit + 1))
        if evaluate(rules, num_bits, x, y) != expected:
            return False
    return True


def find_swaps(
    rules: dict[str, Rule], bit: int, num_bits: int
) -> Iterator[tuple[dict[str, Rule], str, str]]:
    # only consider rules that were used to calculate this bit (though any rule can be swapped in)
    used_rules = [rule for rule in rules.values() if rule.value is not None]
    for rule1 in used_rules:
        for rule2 in rules.values():
            if rule1 == rule2 or rule1.swapped or rule2.swapped:
                continue
            new_rules = rules.copy()
            new_rules[rule1.output] = Rule(
                rule2.input1, rule2.input2, rule1.output, rule2.operation, swapped=True
            )
            new_rules[rule2.output] = Rule(
                rule1.input1, rule1.input2, rule2.output, rule1.operation, swapped=True
            )
            try:
                if is_bit_correct(new_rules, bit, num_bits):
                    yield new_rules, rule1.output, rule2.output
            except ValueError:
                continue


def part2(
    rules: dict[str, Rule], num_bits: int, bit: int
) -> tuple[dict[str, Rule], set[str]] | None:
    if bit == num_bits:
        return rules, set()
    if is_bit_correct(rules, bit, num_bits):
        return part2(rules, num_bits, bit + 1)
    for new_rules, swap1, swap2 in find_swaps(rules, bit, num_bits):
        recurse = part2(new_rules, num_bits, bit + 1)
        if recurse is not None:
            result, swaps = recurse
            for i in range(0, bit):
                if not is_bit_correct(result, i, num_bits):
                    break
            else:
                return result, swaps | {swap1, swap2}
    return None


def run(file: TextIO) -> Iterator[Any]:
    """Solution for Day 24."""
    initial_values_lines, rule_lines = read_sections(file)
    initial_values = {}
    for line in initial_values_lines:
        key, value = line.split(": ")
        initial_values[key] = int(value)
    rules = {}
    for rule in rule_lines:
        inputs, output = rule.split(" -> ")
        input1, operation, input2 = inputs.split(" ")
        rules[output] = Rule(input1, input2, output, operation)
    yield compute_z(rules, initial_values)

    num_bits = max(int(k.lstrip("y")) for k in initial_values if k.startswith("y")) + 1
    result = part2(rules, num_bits, 0)
    assert result is not None
    _, swaps = result
    yield ",".join(sorted(swaps))
