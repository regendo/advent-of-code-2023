from io import TextIOWrapper
from typing import Callable, List, TypeVar, Union

T = TypeVar("T")


def map_lines(text: Union[str, TextIOWrapper], fn: Callable[[str], T]) -> List[T]:
    if isinstance(text, TextIOWrapper):
        return [fn(line) for line in text.readlines()]
    else:
        return [fn(line) for line in text.splitlines()]
