import unittest

from helpers.parsing import map_lines
from day01.trebuchet import double_digits


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
