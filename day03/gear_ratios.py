from dataclasses import dataclass
import re
from typing import Dict, List, Set, Tuple
from typing_extensions import Self

from helpers.parsing import map_lines_with_line_numbers


# eq and frozen imply hashable
@dataclass(eq=True, frozen=True)
class Pos:
    """A position on our schematic.

    Note that both x and y axes start at 1. The top left corner is at Pos(1,1)."""

    x: int
    y: int


@dataclass
class EnginePart:
    """An engine part located on our schematic.

    Note that both start and end positions are 1-indexed and that `end` is the location of the last character, not the location behind it. If our engine part is only one character in length, start == end.
    """

    # all parts are horizontal (start.y == end.y)
    start: Pos
    end: Pos
    value: int

    def surrounding_box_unchecked(self) -> Set[Pos]:
        """Calculate all surrounding positions.

        Note that these aren't validated in any way; they might not even have valid coordinates that fall within the bounds of the schematic.
        """
        box = set()

        # left bar
        box.add(Pos(self.start.x - 1, self.start.y - 1))
        box.add(Pos(self.start.x - 1, self.start.y))
        box.add(Pos(self.start.x - 1, self.start.y + 1))
        # right bar
        box.add(Pos(self.end.x + 1, self.end.y - 1))
        box.add(Pos(self.end.x + 1, self.end.y))
        box.add(Pos(self.end.x + 1, self.end.y + 1))
        # top and bottom bars
        for x in range(self.start.x, self.end.x + 1):
            box.add(Pos(x, self.end.y - 1))
            box.add(Pos(x, self.end.y + 1))

        return box


@dataclass
class Schematic:
    parts: List[EnginePart]
    symbols: Dict[Pos, str]

    @classmethod
    def merge(cls, schematics: List[Self]) -> Self:
        merged = cls(parts=list(), symbols=dict())
        for other in schematics:
            merged.parts.extend(other.parts)
            merged.symbols.update(other.symbols)
        return merged

    @classmethod
    def from_line(cls, line: str, line_no: int) -> Self:
        schema = cls(parts=list(), symbols=dict())
        matches = re.finditer(r"(\d+|[^.\n])", line)
        for match in matches:
            start = Pos(x=match.start() + 1, y=line_no + 1)
            end = Pos(x=match.end(), y=line_no + 1)
            if match.group().isdecimal():
                schema.parts.append(
                    EnginePart(start=start, end=end, value=int(match.group()))
                )
            else:
                schema.symbols[start] = match.group()
        return schema

    def part_numbers(self) -> List[EnginePart]:
        return [
            part
            for part in self.parts
            if self.is_part_adjacent_to_positions(part, list(self.symbols))
        ]

    @staticmethod
    def is_part_adjacent_to_positions(part: EnginePart, positions: List[Pos]) -> bool:
        return any(
            (True for pos in part.surrounding_box_unchecked() if pos in positions)
        )

    def parts_adjacent_to_positions(self, positions: List[Pos]) -> List[EnginePart]:
        return [
            part
            for part in self.parts
            if self.is_part_adjacent_to_positions(part, positions)
        ]

    def gears(self) -> List[Tuple[Pos, List[EnginePart]]]:
        return [
            (pos, parts)
            for (pos, sym) in self.symbols.items()
            if sym == "*"
            if len(parts := self.parts_adjacent_to_positions([pos])) == 2
        ]


def solve_1():
    with open("day03/input.txt", "r") as file:
        schema = Schematic.merge(map_lines_with_line_numbers(file, Schematic.from_line))
        valid_part_numbers = [part.value for part in schema.part_numbers()]
        print(f"Day 03 Part 1: {sum(valid_part_numbers)}")


def solve_2():
    with open("day03/input.txt", "r") as file:
        schema = Schematic.merge(map_lines_with_line_numbers(file, Schematic.from_line))
        gear_ratios = [parts[0].value * parts[1].value for (_, parts) in schema.gears()]
        print(f"Day 03 Part 2: {sum(gear_ratios)}")
