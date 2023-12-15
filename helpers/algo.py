from typing import Generator, Iterable, List, TypeVar


T = TypeVar("T")


def batched(it: Iterable[T], width: int) -> Generator[List[T], None, None]:
    """Because `itertools.batched` requires python3.12"""
    batch = []

    for elem in iter(it):
        batch.append(elem)
        if len(batch) == width:
            yield batch
            batch = []
