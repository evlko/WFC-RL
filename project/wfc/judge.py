from abc import ABC, abstractmethod
from typing import List

from project.utils.utils import Utils
from project.wfc.grid import Grid
from project.wfc.wobj import WeightedObject


class Judge(ABC):
    def __init__(self, seed: int | None = None):
        self.seed = seed

    @abstractmethod
    def select(
        self, objects: List[WeightedObject], grid: Grid | None = None
    ) -> WeightedObject:
        pass


class RandomJudge(Judge):
    def __init__(self, seed: int | None = None):
        super().__init__(seed)

    def select(
        self, objects: List[WeightedObject], grid: Grid | None = None
    ) -> WeightedObject:
        return Utils.weighted_choice(objects=objects, seed=self.seed)


class GreedyJudge(Judge):
    def __init__(self, seed: int | None = None):
        super().__init__(seed)

    def select(
        self, objects: List[WeightedObject], grid: Grid | None = None
    ) -> WeightedObject:
        return max(objects, key=lambda obj: obj.weight)
