import unittest

from helpers.parsing import map_lines
from day01.trebuchet import double_digits, double_digits_refined


class Test(unittest.TestCase):
    def test_ex1(self):
        input = """
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
    """.strip()
        expected = [12, 38, 15, 77]
        actual = map_lines(input, double_digits)
        self.assertEqual(expected, actual)

    def test_ex2(self):
        input = """
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
    """.strip()
        expected = [29, 83, 13, 24, 42, 14, 76]
        actual = map_lines(input, double_digits_refined)
        self.assertEqual(expected, actual)
