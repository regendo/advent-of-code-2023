import unittest
from day03.gear_ratios import Schematic

from helpers.parsing import map_lines_with_line_numbers


class Test(unittest.TestCase):
    def test_ex1(self):
        input = """
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
""".strip()
        expected = [467, 35, 633, 617, 592, 755, 664, 598]
        schema = Schematic.merge(
            map_lines_with_line_numbers(input, Schematic.from_line)
        )
        actual = [part.value for part in schema.part_numbers()]
        self.assertEqual(expected, actual)
