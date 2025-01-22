import json
from collections import defaultdict
from itertools import combinations
from pathlib import Path
from typing import List, Tuple

import numpy as np

from project.machine_learning.model import Model
from project.wfc.grid import Grid, Point, Rect
from project.wfc.judge import Judge
from project.wfc.repository import Repository


class ModelMC(Model, Judge):
    def __init__(self, view: Rect = Rect(3, 3)):
        super().__init__()
        self.view = view
        self.graph = defaultdict(lambda: defaultdict(int))

    def train(self, repository: Repository, grids_path: str):
        grid_files = Path(grids_path).glob("*.dat")

        for file_path in grid_files:
            grid = Grid(patterns=repository.get_all_patterns())
            grid.deserialize(repository, str(file_path.parent), file_path.name)
            for x in range(1, grid.width - 1):
                for y in range(1, grid.height - 1):
                    point = Point(x, y)
                    grid_slice = grid.get_patterns_around_point(p=point, view=self.view)
                    patterns = np.array(
                        [
                            [pattern.uid if pattern else -1 for pattern in row]
                            for row in grid_slice
                        ]
                    )
                    self.generate_paths(patterns)

    def select(self, state):
        serialized_state = state.tostring()
        self.graph[serialized_state]

    def generate_paths(self, state: np.ndarray) -> None:
        view_indices = self.view.indices

        for x, y in view_indices:
            for num_hidden in range(self.view.area):
                hidden_combinations = self._get_hidden_combinations(
                    view_indices, (x, y), num_hidden
                )

                for indices_to_hide in hidden_combinations:
                    state_to = self._apply_hiding(state, indices_to_hide)
                    serialized_state_to = state_to.tostring()

                    state_from = self._apply_hiding(state_to, [(x, y)])
                    serialized_state_from = state_from.tostring()

                    self.graph[serialized_state_from][serialized_state_to] += 1

    def _get_hidden_combinations(
        self,
        view_indices: List[Tuple[int, int]],
        exclude: Tuple[int, int],
        num_hidden: int,
    ) -> combinations:
        """Generate all combinations of indices to hide, excluding the specified position."""
        available_indices = set(view_indices) - {exclude}
        return combinations(available_indices, num_hidden)

    def _apply_hiding(
        self, state: np.ndarray, indices_to_hide: List[Tuple[int, int]]
    ) -> np.ndarray:
        """Create a copy of the state with specified indices hidden (-1)."""
        modified_state = state.copy()
        for hx, hy in indices_to_hide:
            modified_state[hx][hy] = -1
        return modified_state

    def save_weights(self, filename: str) -> None:
        with open(f"{filename}.json", "w") as f:
            json.dump(self.graph, f, default=lambda x: dict(x))

    def load_weights(self, filename: str) -> None:
        with open(f"{filename}.json", "r") as f:
            data = json.load(f)

        graph = defaultdict(lambda: defaultdict(int))
        for key, subdict in data.items():
            graph[key] = defaultdict(int, subdict)
        self.graph = graph
