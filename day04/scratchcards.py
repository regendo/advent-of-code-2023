from dataclasses import dataclass
import re
from typing import List, Set
from typing_extensions import Self

from helpers.parsing import map_lines


@dataclass
class Card:
    winning: Set[int]
    held: Set[int]

    def cards_won(self) -> int:
        return len(self.winning.intersection(self.held))

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

    @classmethod
    def copies_per_card(cls, cards: List[Self]) -> List[int]:
        copies_per_card = [1] * len(cards)
        cards_won = (card.cards_won() for card in cards)
        for this_card_idx, payout in enumerate(cards_won):
            paid_out_cards = range(this_card_idx + 1, this_card_idx + 1 + payout)
            copies_of_this_card = copies_per_card[this_card_idx]
            for paid_out_card_idx in paid_out_cards:
                copies_per_card[paid_out_card_idx] += copies_of_this_card
        return copies_per_card


def solve_1():
    with open("day04/input.txt", "r") as file:
        cards = map_lines(file, Card.from_line)
        points = [card.points() for card in cards]
        print(f"Day 04 Part 1: {sum(points)}")


def solve_2():
    with open("day04/input.txt", "r") as file:
        cards = map_lines(file, Card.from_line)
        copies = Card.copies_per_card(cards)
        print(f"Day 04 Part 2: {sum(copies)}")
