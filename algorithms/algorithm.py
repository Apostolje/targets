from algorithms import Solution

from abc import ABC, abstractmethod
from typing import Iterator


class Algorithm(ABC):

    @abstractmethod
    def run(self) -> Iterator[Solution]:
        ...
