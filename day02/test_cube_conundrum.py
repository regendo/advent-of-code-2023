import unittest

from day02.cube_conundrum import BallSet, parse_game
from helpers.parsing import map_lines


class Test(unittest.TestCase):
    def test_ex1(self):
        input = """
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
""".strip()
        available_balls = BallSet(red=12, green=13, blue=14)
        expected = [1, 2, 5]
        games = map_lines(input, parse_game)
        actual = [
            game.id for game in games if game.is_possible_with_balls(available_balls)
        ]
        self.assertEqual(expected, actual)

    def test_ex2(self):
        input = """
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
""".strip()
        expected = [48, 12, 1560, 630, 36]
        games = map_lines(input, parse_game)
        actual = [game.minimum_necessary_balls().power() for game in games]
        self.assertEqual(expected, actual)
