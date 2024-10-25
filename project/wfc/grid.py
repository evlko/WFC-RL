from typing import List, Tuple

import numpy as np

from project.wfc.direction import Direction
from project.wfc.pattern import MetaPattern


class Grid:
    def __init__(self, width: int, height: int, patterns: List[MetaPattern]):
        self.width = width
        self.height = height
        self.patterns = patterns
        self.initialize()

    def initialize(self) -> None:
        """Initialize or reset the grid with full entropy in all cells."""
        self.grid = np.full((self.height, self.width), None)
        self.entropy = np.full((self.height, self.width), len(self.patterns))

    def find_least_entropy_cell(self) -> Tuple[int, int]:
        """Find the cell with the lowest entropy. If multiple, choose closest to center."""
        min_entropy = np.min(self.entropy[self.entropy > 0])
        candidates = np.argwhere(self.entropy == min_entropy)
        center = np.array([self.height // 2, self.width // 2])
        distances = np.linalg.norm(candidates - center, axis=1)
        closest_index = np.argmin(distances)
        return tuple(candidates[closest_index])

    def get_neighbors(self, x: int, y: int) -> List[MetaPattern]:
        """Get neighbors and their directions for the cell (x, y)."""
        neighbors = []
        if x > 0:
            neighbors.append((x - 1, y, Direction.DOWN))
        if x < self.height - 1:
            neighbors.append((x + 1, y, Direction.UP))
        if y > 0:
            neighbors.append((x, y - 1, Direction.RIGHT))
        if y < self.width - 1:
            neighbors.append((x, y + 1, Direction.LEFT))
        return neighbors

    def get_valid_patterns(self, x: int, y: int) -> List[MetaPattern]:
        """Get all valid patterns for the cell (x, y) based on neighbors' constraints."""
        possible_patterns = set(self.patterns)

        for nx, ny, direction in self.get_neighbors(x, y):
            neighbor_pattern = self.grid[nx, ny]
            if neighbor_pattern is not None:
                allowed_patterns = neighbor_pattern.rules.get_allowed_neighbors(
                    direction
                )
                possible_patterns = possible_patterns.intersection(allowed_patterns)

        return list(possible_patterns)

    def place_pattern(self, x: int, y: int, pattern: MetaPattern) -> None:
        """Place a pattern in the grid at the specified position."""
        self.grid[x, y] = pattern
        self.entropy[x, y] = 0

    def update_neighbors_entropy(self, x: int, y: int) -> bool:
        """Recalculate the entropy of neighboring cells after placing a pattern."""
        for nx, ny, _ in self.get_neighbors(x, y):
            if self.grid[nx, ny] is None:
                possible_patterns = self.get_valid_patterns(nx, ny)
                entropy = len(possible_patterns)
                self.entropy[nx, ny] = len(possible_patterns)
                if entropy == 0:
                    return True
        return False

    def is_collapsed(self) -> bool:
        """Check if the entire grid has been filled."""
        return np.all(self.grid != None)

    def __str__(self) -> str:
        """Custom string representation of the grid showing uids or 'None'."""
        grid_str = ""
        for row in self.grid:
            row_str = []
            for cell in row:
                cell_str = (lambda c: str(c.uid) if c else "None")(cell)
                row_str.append(cell_str)
            grid_str += " | ".join(row_str) + "\n"
        return grid_str
