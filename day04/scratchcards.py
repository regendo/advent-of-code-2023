from dataclasses import dataclass
import re
from typing import Set
from typing_extensions import Self

from helpers.parsing import map_lines


@dataclass
class Card:
    winning: Set[int]
    held: Set[int]

    def points(self) -> int:
        matching = len(self.winning.intersection(self.held))
        if matching == 0:
            return 0
        return 2 ** (matching - 1)

    @classmethod
    def from_line(cls, line: str) -> Self:
        _, rem = line.split(":", 1)
        mid, right = rem.split("|", 1)
        winning = [int(num) for num in re.findall(r"(\d+)", mid)]
        held = [int(num) for num in re.findall(r"(\d+)", right)]

        return cls(winning=set(winning), held=set(held))


def solve_1():
    with open("day04/input.txt", "r") as file:
        cards = map_lines(file, Card.from_line)
        points = [card.points() for card in cards]
        print(f"Day 04 Part 1: {sum(points)}")
