from dataclasses import dataclass
from typing import List, Optional

import numpy as np

from project.wfc.direction import Direction
from project.wfc.pattern import MetaPattern


@dataclass
class Point:
    x: int
    y: int


@dataclass
class Rect:
    width: int
    height: int


class Grid:
    def __init__(self, rect: Rect, patterns: List[MetaPattern]):
        self.width = rect.width
        self.height = rect.height
        self.patterns = patterns
        self.initialize()

    def initialize(self) -> None:
        """Initialize or reset the grid with full entropy in all cells."""
        self.grid = np.full((self.height, self.width), None)
        self.entropy = np.full((self.height, self.width), len(self.patterns))

    def get_patterns_around_point(
        self, p: Point, view: Rect = Rect(width=3, height=3), is_extended: bool = True
    ) -> List[Optional[MetaPattern]]:
        """Get patterns within a rectangular region around a specified point (x, y)."""
        half_width, half_height = view.width // 2, view.height // 2

        if is_extended:
            proxy_grid = np.full(
                (self.height + 2 * half_height, self.width + 2 * half_width),
                None,
                dtype=object,
            )
            proxy_grid[
                half_height : half_height + self.height,
                half_width : half_width + self.width,
            ] = self.grid
            x_min, y_min = (
                p.x + half_width - half_height,
                p.y + half_width - half_height,
            )
            return proxy_grid[y_min : y_min + view.width, x_min : x_min + view.height]

        x_min, x_max = max(0, p.x - half_height), min(
            self.height, p.x + half_height + 1
        )
        y_min, y_max = max(0, p.y - half_width), min(self.width, p.y + half_width + 1)
        return self.grid[y_min:y_max, x_min:x_max]

    def find_least_entropy_cell(self) -> Point | None:
        """Find the cell with the lowest entropy. If multiple, choose closest to center."""
        candidates = self.entropy[self.entropy > 0]
        if len(candidates) == 0:
            return None
        min_entropy = np.min(candidates)
        candidates = np.argwhere(self.entropy == min_entropy)
        center = np.array([self.height // 2, self.width // 2])
        distances = np.linalg.norm(candidates - center, axis=1)
        closest_index = np.argmin(distances)
        candidate_y, candidate_x = candidates[closest_index]
        return Point(x=candidate_y, y=candidate_x)

    def get_neighbors(self, p: Point) -> List[MetaPattern]:
        """Get neighbors and their directions for the cell (x, y)."""
        neighbors = []
        if p.x > 0:
            neighbors.append((p.x - 1, p.y, Direction.DOWN))
        if p.x < self.height - 1:
            neighbors.append((p.x + 1, p.y, Direction.UP))
        if p.y > 0:
            neighbors.append((p.x, p.y - 1, Direction.RIGHT))
        if p.y < self.width - 1:
            neighbors.append((p.x, p.y + 1, Direction.LEFT))
        return neighbors

    def get_valid_patterns(self, p: Point) -> List[MetaPattern]:
        """Get all valid patterns for the cell (x, y) based on neighbors' constraints."""
        possible_patterns = set(self.patterns)

        for nx, ny, direction in self.get_neighbors(p):
            neighbor_pattern = self.grid[nx, ny]
            if neighbor_pattern is not None:
                allowed_patterns = neighbor_pattern.rules.get_allowed_neighbors(
                    direction
                )
                possible_patterns = possible_patterns.intersection(allowed_patterns)

        return list(possible_patterns)

    def place_pattern(self, p: Point, pattern: MetaPattern) -> None:
        """Place a pattern in the grid at the specified position."""
        self.grid[p.x, p.y] = pattern
        self.entropy[p.x, p.y] = 0

    def update_neighbors_entropy(self, p: Point) -> Point | None:
        """Recalculate the entropy of neighboring cells after placing a pattern."""
        for x, y, _ in self.get_neighbors(p):
            np = Point(x=x, y=y)
            if self.grid[np.x, np.y] is None:
                possible_patterns = self.get_valid_patterns(np)
                entropy = len(possible_patterns)
                self.entropy[np.x, np.y] = len(possible_patterns)
                if entropy == 0:
                    return np
        return None

    def is_collapsed(self) -> bool:
        """Check if the entire grid has been filled."""
        return np.all(self.grid != None)

    def __str__(self) -> str:
        """Custom string representation of the grid showing uids or 'None'."""
        grid_str = ""
        for row in self.grid:
            row_str = []
            for cell in row:
                cell_str = (lambda c: f"{c.uid:02}" if c else "None")(cell)
                row_str.append(cell_str)
            grid_str += " | ".join(row_str) + "\n"
        return grid_str
