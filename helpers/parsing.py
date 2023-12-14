from io import TextIOWrapper
from typing import Callable, List, TypeVar

T = TypeVar("T")


def map_lines(text: str | TextIOWrapper, fn: Callable[[str], T]) -> List[T]:
    if isinstance(text, TextIOWrapper):
        return [fn(line) for line in text.readlines()]
    else:
        return [fn(line) for line in text.splitlines()]


def map_lines_with_line_numbers(
    text: str | TextIOWrapper, fn: Callable[[str, int], T]
) -> List[T]:
    if isinstance(text, TextIOWrapper):
        return [fn(line, idx) for (idx, line) in enumerate(text.readlines())]
    else:
        return [fn(line, idx) for (idx, line) in enumerate(text.splitlines())]
