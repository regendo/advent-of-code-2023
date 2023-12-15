from dataclasses import dataclass
import re
from typing import Generator, List, Optional
from typing_extensions import Self
from functools import reduce
from helpers.parsing import skip_first_line, text
from helpers.algo import batched


@dataclass
class RangeMap:
    source_start: int
    dest_start: int
    width: int

    def try_map(self, num: int) -> Optional[int]:
        off = num - self.source_start
        if off >= 0 and off < self.width:
            return self.dest_start + off
        else:
            return None

    @classmethod
    def from_line(cls, line: str) -> Self:
        matched = re.findall(r"(\d+)", line)
        dest, src, width = matched
        return cls(source_start=int(src), dest_start=int(dest), width=int(width))

    @classmethod
    def map(cls, num: int, maps: List[Self]) -> int:
        for map in maps:
            if (val := map.try_map(num)) is not None:
                return val
        return num

    @classmethod
    def chain_map(cls, num, maps: List[List[Self]]) -> int:
        return reduce(lambda n, f: cls.map(n, f), maps, num)


@dataclass
class Farm:
    seeds: List[int]
    seeds_to_soil: List[RangeMap]
    soil_to_fertilizer: List[RangeMap]
    fertilizer_to_water: List[RangeMap]
    water_to_light: List[RangeMap]
    light_to_temperature: List[RangeMap]
    temperature_to_humidity: List[RangeMap]
    humidity_to_location: List[RangeMap]

    def seeds_to_location(self) -> Generator[int, None, None]:
        return (
            RangeMap.chain_map(
                seed,
                [
                    self.seeds_to_soil,
                    self.soil_to_fertilizer,
                    self.fertilizer_to_water,
                    self.water_to_light,
                    self.light_to_temperature,
                    self.temperature_to_humidity,
                    self.humidity_to_location,
                ],
            )
            for seed in self.seeds
        )

    def seed_ranges_to_location(self) -> Generator[int, None, None]:
        return (
            RangeMap.chain_map(
                seed,
                [
                    self.seeds_to_soil,
                    self.soil_to_fertilizer,
                    self.fertilizer_to_water,
                    self.water_to_light,
                    self.light_to_temperature,
                    self.temperature_to_humidity,
                    self.humidity_to_location,
                ],
            )
            for seed in self.seed_ranges()
        )

    def seed_ranges(self) -> Generator[int, None, None]:
        return (
            seed
            for (start, width) in batched(self.seeds, 2)
            for seed in range(start, start + width)
        )

    @classmethod
    def from_multiline(cls, text: str) -> Self:
        sections = iter(text.strip().split("\n\n"))
        seeds = [int(seed) for seed in re.findall(r"(\d+)", next(sections))]
        return cls(
            seeds,
            [RangeMap.from_line(line) for line in skip_first_line(next(sections))],
            [RangeMap.from_line(line) for line in skip_first_line(next(sections))],
            [RangeMap.from_line(line) for line in skip_first_line(next(sections))],
            [RangeMap.from_line(line) for line in skip_first_line(next(sections))],
            [RangeMap.from_line(line) for line in skip_first_line(next(sections))],
            [RangeMap.from_line(line) for line in skip_first_line(next(sections))],
            [RangeMap.from_line(line) for line in skip_first_line(next(sections))],
        )


def solve_1():
    with open("day05/input.txt", "r") as file:
        farm = Farm.from_multiline(text(file))
        locations = farm.seeds_to_location()
        print(f"Day 05 Part 1: {min(locations)}")


def solve_2():
    with open("day05/input.txt", "r") as file:
        farm = Farm.from_multiline(text(file))
        locations = farm.seed_ranges_to_location()
        print(f"Day 05 Part 2: {min(locations)}")
