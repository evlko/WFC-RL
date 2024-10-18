import numpy as np

from direction import Direction


class Grid:
    def __init__(self, width, height, patterns):
        self.width = width
        self.height = height
        self.patterns = patterns
        self.grid = np.full((width, height), None)
        self.entropy = np.full((width, height), len(patterns))

    def initialize(self):
        """Initialize or reset the grid with full entropy in all cells."""
        self.grid = np.full((self.width, self.height), None)
        self.entropy = np.full((self.width, self.height), len(self.patterns))

    def find_least_entropy_cell(self):
        """Find the cell with the lowest entropy. If multiple, choose closest to center."""
        min_entropy = np.min(self.entropy[self.entropy > 0])
        candidates = np.argwhere(self.entropy == min_entropy)
        center = np.array([self.width // 2, self.height // 2])
        distances = np.linalg.norm(candidates - center, axis=1)
        closest_index = np.argmin(distances)
        return tuple(candidates[closest_index])

    def get_neighbors(self, x, y):
        """Get neighbors and their directions for the cell (x, y)."""
        neighbors = []
        if x > 0:
            neighbors.append((x - 1, y, Direction.LEFT))
        if x < self.width - 1:
            neighbors.append((x + 1, y, Direction.RIGHT))
        if y > 0:
            neighbors.append((x, y - 1, Direction.UP))
        if y < self.height - 1:
            neighbors.append((x, y + 1, Direction.DOWN))
        return neighbors

    def get_valid_patterns(self, x, y):
        """Get all valid patterns for the cell (x, y) based on neighbors' constraints."""
        possible_patterns = set(self.patterns)

        for nx, ny, direction in self.get_neighbors(x, y):
            neighbor_pattern = self.grid[nx, ny]
            if neighbor_pattern is not None:
                allowed_patterns = neighbor_pattern.rule_set.get_allowed_neighbors(
                    direction
                )
                possible_patterns = possible_patterns.intersection(allowed_patterns)

        return list(possible_patterns)

    def collapse(self, x, y):
        """Collapse the wave function at (x, y) by choosing a valid pattern."""
        possible_patterns = self.get_valid_patterns(x, y)

        if not possible_patterns:
            return False

        chosen_pattern = np.random.choice(possible_patterns)
        self.grid[x, y] = chosen_pattern
        self.entropy[x, y] = 0
        return True

    def update_neighbors_entropy(self, x, y):
        """Recalculate the entropy of neighboring cells after placing a pattern."""
        for nx, ny, _ in self.get_neighbors(x, y):
            if self.grid[nx, ny] is None:
                possible_patterns = self.get_valid_patterns(nx, ny)
                self.entropy[nx, ny] = len(possible_patterns)

    def step(self):
        """Perform one step in the WFC process: find, collapse, and update neighbors."""
        cell = self.find_least_entropy_cell()
        if cell is None:
            return False

        x, y = cell
        success = self.collapse(x, y)
        if not success:
            print(f"Generation failed at cell ({x}, {y}).")
            return False

        self.update_neighbors_entropy(x, y)
        return True

    def generate(self):
        """Run the generation process until the grid is fully collapsed or fails."""
        self.initialize()
        while not self.is_collapsed():
            if not self.step():
                print("Generation failed.")
                return False
        print("Generation succeeded!")
        return True

    def is_collapsed(self):
        """Check if the entire grid has been filled."""
        return np.all(self.grid != None)
