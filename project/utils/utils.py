import base64
from typing import List, Tuple

import numpy as np

from project.wfc.wobj import WeightedObject


class Utils:
    @staticmethod
    def weighted_choice(
        objects: List[WeightedObject], seed: int = None
    ) -> WeightedObject:
        """Select a weighted object based on its weight."""
        random_gen = np.random.RandomState(seed)

        weights = np.array([obj.weight for obj in objects])
        probabilities = weights / np.sum(weights)

        return random_gen.choice(objects, p=probabilities)

    @staticmethod
    def encode_np_array(arr: np.ndarray) -> str:
        return base64.b64encode(arr.tobytes()).decode("utf-8")

    @staticmethod
    def decode_np_array(
        encoded_str: str, shape: Tuple[int, ...], dtype: np.dtype = int
    ) -> np.ndarray:
        byte_data = base64.b64decode(encoded_str)
        return np.frombuffer(byte_data, dtype=dtype).reshape(shape)
