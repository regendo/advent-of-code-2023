import re

from helpers.parsing import map_lines


def double_digits(line: str) -> int:
    found = re.findall(r"(\d)", line)
    # assumes found has the correct sort of elements
    return int(found[0]) * 10 + int(found[-1])


def double_digits_refined(line: str) -> int:
    found = re.findall(r"(\d|one|two|three|four|five|six|seven|eight|nine)", line)
    # assumes found has the correct sort of elements
    return str_to_digit(found[0]) * 10 + str_to_digit(found[-1])


def str_to_digit(word: str) -> int:
    if len(word) == 1 and word.isdigit():
        return int(word)
    # assumes only valid input
    return {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        # zero not allowed here
    }[word]


def solve_1():
    with open("day01/input.txt", "r") as file:
        nums = map_lines(file, double_digits)
        print(f"Day 01 Part 1: {sum(nums)}")


def solve_2():
    with open("day01/input.txt", "r") as file:
        nums = map_lines(file, double_digits_refined)
        print(f"Day 01 Part 2: {sum(nums)}")
