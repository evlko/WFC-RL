from typing import List, Tuple

import numpy as np


class Rectangulator:
    @staticmethod
    def find_max_rectangle(array: np.ndarray) -> Tuple[int, int, int, int]:
        n_rows, n_cols = array.shape
        max_area = 0
        best_rectangle = None

        for i in range(n_rows):
            for j in range(n_cols):
                if array[i, j] == 1:
                    for x2 in range(i, n_rows):
                        if array[x2, j] == 0:
                            break
                        for y2 in range(j, n_cols):
                            if np.any(array[i : x2 + 1, j : y2 + 1] == 0):
                                break
                            area = (x2 - i + 1) * (y2 - j + 1)
                            if area > max_area:
                                max_area = area
                                best_rectangle = (i, j, x2, y2)
        return best_rectangle

    @staticmethod
    def remove_rectangle(
        array: np.ndarray, rectangle: Tuple[int, int, int, int]
    ) -> None:
        x1, y1, x2, y2 = rectangle
        array[x1 : x2 + 1, y1 : y2 + 1] = 0

    def split_into_minimum_rectangles(
        self, array: np.ndarray
    ) -> List[Tuple[int, int, int, int]]:
        rectangles = []

        while np.any(array):
            rectangle = self.find_max_rectangle(array)
            if rectangle is None:
                break
            rectangles.append(rectangle)
            self.remove_rectangle(array, rectangle)

        return rectangles
