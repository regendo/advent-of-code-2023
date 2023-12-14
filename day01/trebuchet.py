import re

from helpers.parsing import map_lines


def double_digits(line: str) -> int:
    found = re.findall(r"(\d)", line)
    # assumes found has the correct sort of elements
    return int(found[0]) * 10 + int(found[-1])


def solve_1():
    with open("day01/input1.txt", "r") as file:
        nums = map_lines(file, double_digits)
        print(f"Day 01 Part 1: {sum(nums)}")
