import re
from dataclasses import dataclass
from typing import List

from helpers.parsing import map_lines


@dataclass
class BallSet:
    red: int
    green: int
    blue: int

    def power(self) -> int:
        """Product (multiplication) of the individual colored balls."""
        return self.red * self.green * self.blue


@dataclass
class Game:
    id: int
    reveals: List[BallSet]

    def is_possible_with_balls(self, available_balls: BallSet) -> bool:
        for balls in self.reveals:
            if (
                balls.red > available_balls.red
                or balls.green > available_balls.green
                or balls.blue > available_balls.blue
            ):
                return False
        return True

    def minimum_necessary_balls(self) -> BallSet:
        necessary = BallSet(0, 0, 0)
        for reveal in self.reveals:
            necessary.red = max(necessary.red, reveal.red)
            necessary.green = max(necessary.green, reveal.green)
            necessary.blue = max(necessary.blue, reveal.blue)

        return necessary


def parse_game(line: str) -> Game:
    # assumes everything just works
    [game_str, rest] = line.split(":", 1)
    id = int(game_str.split()[1])
    game = Game(id, list())
    for reveal in rest.split(";"):
        found = re.findall(r"(\d+) (red|green|blue)", reveal)
        balls = BallSet(0, 0, 0)
        for num, color in found:
            if color == "red":
                balls.red = int(num)
            if color == "green":
                balls.green = int(num)
            if color == "blue":
                balls.blue = int(num)
        game.reveals.append(balls)
    return game


def solve_1():
    with open("day02/input.txt", "r") as file:
        games = map_lines(file, parse_game)
        available_balls = BallSet(red=12, green=13, blue=14)
        possible_games = [
            game.id for game in games if game.is_possible_with_balls(available_balls)
        ]
        print(f"Day 02 Part 1: {sum(possible_games)}")


def solve_2():
    with open("day02/input.txt", "r") as file:
        games = map_lines(file, parse_game)
        powers = [game.minimum_necessary_balls().power() for game in games]

        print(f"Day 02 Part 2: {sum(powers)}")
