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

    def source_stop(self) -> int:
        return self.source_start + self.width

    def dest_stop(self) -> int:
        return self.dest_start + self.width

    def try_map(self, num: int) -> Optional[int]:
        off = num - self.source_start
        if off >= 0 and off < self.width:
            return self.dest_start + off
        else:
            return None

    def try_map_range(self, nums: range) -> Optional[range]:
        last_num = nums.stop - 1
        match (self.try_map(nums.start), self.try_map(last_num)):
            case (int(start), int(stop)):
                return range(start, stop + 1)
            case (None, int(stop)):
                return range(self.dest_start, stop + 1)
            case (int(start), None):
                return range(start, self.dest_stop())
            case (_, _):
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
    def map_range(cls, nums: range, maps: List[Self]) -> List[range]:
        mapped_ranges = [
            mapped for map in maps if (mapped := map.try_map_range(nums)) is not None
        ]
        if mapped_ranges:
            return mapped_ranges
        else:
            return [nums]

    @classmethod
    def chain_map(cls, num: int, maps: List[List[Self]]) -> int:
        return reduce(lambda n, fn: cls.map(n, fn), maps, num)

    @classmethod
    def chain_map_ranges(
        cls, nums: Generator[range, None, None], maps: List[List[Self]]
    ) -> Generator[range, None, None]:
        return reduce(
            lambda current_ranges, fn: (
                mapped_range
                for source_range in current_ranges
                for mapped_range in cls.map_range(source_range, fn)
            ),
            maps,
            nums,
        )


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

    def seed_ranges_to_location_ranges(self) -> Generator[range, None, None]:
        return RangeMap.chain_map_ranges(
            self.seed_ranges(),
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

    def seed_ranges(self) -> Generator[range, None, None]:
        return (
            range(start, start + width) for (start, width) in batched(self.seeds, 2)
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


def first_num_in_ranges(gen: Generator[range, None, None]) -> int:
    return min(r.start for r in gen)


def solve_1():
    with open("day05/input.txt", "r") as file:
        farm = Farm.from_multiline(text(file))
        locations = farm.seeds_to_location()
        print(f"Day 05 Part 1: {min(locations)}")


def solve_2():
    with open("day05/input.txt", "r") as file:
        farm = Farm.from_multiline(text(file))
        locations = farm.seed_ranges_to_location_ranges()

        print(f"Day 05 Part 2: {first_num_in_ranges(locations)}")
