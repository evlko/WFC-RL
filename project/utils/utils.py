from typing import List

import numpy as np

from project.wfc.wobj import WeightedObject


class Utils:
    @staticmethod
    def weighted_choice(
        possible_objects: List[WeightedObject], seed: int = None
    ) -> WeightedObject:
        """Select a weighted object based on its weight."""
        random_gen = np.random.RandomState(seed)

        weights = np.array([obj.weight for obj in possible_objects])
        probabilities = weights / np.sum(weights)

        return random_gen.choice(possible_objects, p=probabilities)
