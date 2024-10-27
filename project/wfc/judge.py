from abc import ABC, abstractmethod
from typing import List

from project.utils.utils import Utils
from project.wfc.grid import Grid
from project.wfc.wobj import WeightedObject


class Judge(ABC):
    @staticmethod
    @abstractmethod
    def select(
        objects: List[WeightedObject], grid: Grid | None = None, seed: int = None
    ) -> WeightedObject:
        pass


class RandomJudge(Judge):
    @staticmethod
    def select(
        objects: List[WeightedObject], grid: Grid | None = None, seed: int = None
    ) -> WeightedObject:
        return Utils.weighted_choice(objects=objects, seed=seed)


class GreedyJudge(Judge):
    @staticmethod
    def select(
        objects: List[WeightedObject], grid: Grid | None = None, seed: int = None
    ) -> WeightedObject:
        return max(objects, key=lambda obj: obj.weight)
