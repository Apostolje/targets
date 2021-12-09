from abc import ABC, abstractmethod
from typing import Iterator, Tuple, List


class Algorithm(ABC):

    @abstractmethod
    def run(self) -> Iterator[Tuple[int, float, List[int]]]:
        ...
