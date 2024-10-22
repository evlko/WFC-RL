import numpy as np
from typing import List
from project.wfc.wobj import WeightedObject


class Utils:
    @staticmethod
    def weighted_choice(possible_objects: List[WeightedObject]) -> WeightedObject:
        """Select a weighted object based on its weight."""
        weights = np.array([obj.weight for obj in possible_objects])
        probabilities = weights / np.sum(weights)
        return np.random.choice(possible_objects, p=probabilities)
