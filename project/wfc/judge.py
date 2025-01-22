from abc import ABC, abstractmethod
from typing import List

from project.utils.utils import Utils
from project.wfc.grid import Rect
from project.wfc.wobj import WeightedObject


class Judge(ABC):
    def __init__(self, seed: int | None = None, judge_view: Rect | None = Rect(1, 1)):
        self.seed = seed
        self.judge_view = judge_view

    @abstractmethod
    def select(
        self, objects: List[WeightedObject], view: Rect | None = None
    ) -> WeightedObject:
        pass


class RandomJudge(Judge):
    def __init__(self, seed: int | None = None):
        super().__init__(seed)

    def select(
        self, objects: List[WeightedObject], view: Rect | None = None
    ) -> WeightedObject:
        return Utils.weighted_choice(objects=objects, seed=self.seed)


class GreedyJudge(Judge):
    def __init__(self, seed: int | None = None):
        super().__init__(seed)

    def select(
        self, objects: List[WeightedObject], view: Rect | None = None
    ) -> WeightedObject:
        return max(objects, key=lambda obj: obj.weight)
