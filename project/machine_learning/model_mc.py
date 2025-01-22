import json
from collections import defaultdict
from pathlib import Path
from typing import List

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

    def select():
        pass

    def generate_paths(self, state: List[int]) -> None:
        serialized_state_to = state.tostring()

        for x in range(self.view.width):
            for y in range(self.view.height):
                state_from = state.copy()
                state_from[x][y] = -1
                serialized_state_from = state_from.tostring()
                print("###")
                print(np.fromstring(serialized_state_from, dtype=int))
                print("-->")
                print(np.fromstring(serialized_state_to, dtype=int))
                print("###")
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
