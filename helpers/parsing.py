from io import TextIOWrapper
from typing import Callable, List, TypeVar

T = TypeVar("T")


def map_lines(text: str | TextIOWrapper, fn: Callable[[str], T]) -> List[T]:
    return [fn(line) for line in lines(text)]


def map_lines_with_line_numbers(
    text: str | TextIOWrapper, fn: Callable[[str, int], T]
) -> List[T]:
    return [fn(line, idx) for (idx, line) in enumerate(lines(text))]


def skip_first_line(text: str | TextIOWrapper) -> List[str]:
    return lines(text)[1:]


def lines(text: str | TextIOWrapper) -> List[str]:
    if isinstance(text, TextIOWrapper):
        return text.readlines()
    else:
        return text.splitlines()


def text(text: str | TextIOWrapper) -> str:
    if isinstance(text, TextIOWrapper):
        return text.read()
    else:
        return text
