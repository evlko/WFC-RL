import json
from collections import defaultdict
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
from typing import List, Tuple

import numpy as np
from tqdm import tqdm

from project.config import HIDDEN_CELL, TARGET_CELL
from project.machine_learning.model import Model
from project.utils.utils import Utils
from project.wfc.grid import Grid, Point, Rect
from project.wfc.judge import Judge
from project.wfc.pattern import MetaPattern
from project.wfc.repository import repository
from project.wfc.wobj import WeightedObject


@dataclass
class State(WeightedObject):
    state: str


class ModelMC(Model, Judge):
    def __init__(self, seed: int | None = None, view: Rect = Rect(3, 3)):
        super().__init__(view=view, seed=seed)
        self.graph = defaultdict(lambda: defaultdict(int))
        self.used_keys = set()

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
        hide_code: int = HIDDEN_CELL,
    ) -> np.ndarray:
        """Create a copy of the state with specified indices hidden."""
        modified_state = state.copy()
        for hx, hy in indices_to_hide:
            modified_state[hx][hy] = hide_code
        return modified_state

    def train(self, grids_path: str, portion: float = 1.0):
        grid_files = list(Path(grids_path).glob("*.dat"))
        files_count = int(len(grid_files) * portion)
        grid_files = grid_files[:files_count]

        for file_path in tqdm(grid_files):
            grid = Grid(patterns=repository.get_all_patterns())
            grid.deserialize(repository, str(file_path.parent), file_path.name)
            for x in range(grid.height):
                for y in range(grid.width):
                    point = Point(x, y)
                    pattenrs = grid.get_patterns_around_point(p=point, view=self.view)
                    pattenrs_uids = grid.get_patterns_property(pattenrs)
                    self.generate_paths(pattenrs_uids)

    def select(
        self, objects: List[WeightedObject], state: np.ndarray
    ) -> MetaPattern | None:
        cx, cy = 1, 1
        state = self._apply_hiding(state, [(cx, cy)], TARGET_CELL)
        serialized_state = Utils.encode_np_array(state)
        self.used_keys.add(serialized_state)

        if serialized_state not in self.graph:
            return None

        states = [
            State(state=key, weight=value)
            for key, value in self.graph[serialized_state].items()
        ]

        next_state = Utils.weighted_choice(states, self.seed)

        next_state = Utils.decode_np_array(
            next_state.state, shape=(self.view.width, self.view.height)
        )

        changed_cells = np.argwhere((state == TARGET_CELL) & (next_state != state))

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

                    state_from = self._apply_hiding(state_to, [(x, y)], TARGET_CELL)
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
