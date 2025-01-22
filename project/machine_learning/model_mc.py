import json
from collections import defaultdict
from itertools import combinations
from pathlib import Path
from typing import List, Tuple

import numpy as np

from project.machine_learning.model import Model
from project.utils.utils import Utils
from project.wfc.grid import Grid, Point, Rect
from project.wfc.judge import Judge
from project.wfc.pattern import MetaPattern
from project.wfc.repository import repository
from project.wfc.wobj import WeightedObject


class ModelMC(Model, Judge):
    def __init__(self, view: Rect = Rect(3, 3)):
        super().__init__()
        self.view = view
        self.graph = defaultdict(lambda: defaultdict(int))

    @staticmethod
    def _get_hidden_combinations(
        view_indices: List[Tuple[int, int]],
        exclude: Tuple[int, int],
        num_hidden: int,
    ) -> combinations:
        """Generate all combinations of indices to hide, excluding the specified position."""
        available_indices = set(view_indices) - {exclude}
        return combinations(available_indices, num_hidden)

    @staticmethod
    def _apply_hiding(
        state: np.ndarray,
        indices_to_hide: List[Tuple[int, int]],
        hide_code: int = -1,
    ) -> np.ndarray:
        """Create a copy of the state with specified indices hidden."""
        modified_state = state.copy()
        for hx, hy in indices_to_hide:
            modified_state[hx][hy] = hide_code
        return modified_state

    @staticmethod
    def _get_uid_from_view(patterns: np.ndarray):
        return np.array(
            [[pattern.uid if pattern else -1 for pattern in row] for row in patterns]
        )

    def train(self, grids_path: str):
        grid_files = Path(grids_path).glob("*.dat")

        for file_path in grid_files:
            grid = Grid(patterns=repository.get_all_patterns())
            grid.deserialize(repository, str(file_path.parent), file_path.name)
            for x in range(grid.width):
                for y in range(grid.height):
                    point = Point(x, y)
                    grid_slice = grid.get_patterns_around_point(p=point, view=self.view)
                    patterns = self._get_uid_from_view(grid_slice)
                    self.generate_paths(patterns)

    def select(
        self, objects: List[WeightedObject] = None, view: Rect | None = None
    ) -> MetaPattern:
        state = self._get_uid_from_view(view)
        serialized_state = Utils.encode_np_array(state)
        transitions = self.graph[serialized_state]

        serialized_states = list(transitions.keys())
        weights = list(transitions.values())

        random_gen = np.random.RandomState()
        probabilities = np.array(weights) / np.sum(weights)
        selected_index = random_gen.choice(len(serialized_states), p=probabilities)

        next_state = Utils.decode_np_array(
            serialized_states[selected_index], shape=(self.view.width, self.view.height)
        )

        changed_cells = np.argwhere((state == 0) & (next_state != state))

        if len(changed_cells) != 1:
            raise ValueError(
                "Unexpected number of changed cells. Expected exactly one."
            )

        selected_uid = next_state[tuple(changed_cells[0])]
        selected_pattern = repository.get_pattern_by_uid(selected_uid)
        return selected_pattern

    def generate_paths(self, state: np.ndarray) -> None:
        view_indices = self.view.indices

        for x, y in view_indices:
            for num_hidden in range(self.view.area):
                hidden_combinations = self._get_hidden_combinations(
                    view_indices, (x, y), num_hidden
                )

                for indices_to_hide in hidden_combinations:
                    state_to = self._apply_hiding(state, indices_to_hide)
                    serialized_state_to = Utils.encode_np_array(state_to)

                    state_from = self._apply_hiding(state_to, [(x, y)], 0)
                    serialized_state_from = Utils.encode_np_array(state_from)

                    self.graph[serialized_state_from][serialized_state_to] += 1

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
