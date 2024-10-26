from project.wfc.grid import Grid
from project.wfc.judge import Judge


class WFC:
    def __init__(self, grid: Grid, judge: Judge):
        self.grid = grid
        self.judge = judge
        self._is_initialized = False

    def initialize(self):
        """Initialize the grid for the WFC process."""
        self.grid.initialize()
        self._is_initialized = True

    def step(self, early_stopping: bool = True) -> bool:
        """Perform one step in the WFC process: find, collapse, and update neighbors."""
        if not self._is_initialized:
            self.initialize()

        point = self.grid.find_least_entropy_cell()
        if point is None and early_stopping:
            return False

        possible_patterns = self.grid.get_valid_patterns(point)
        if not possible_patterns and early_stopping:
            return False

        chosen_pattern = self.judge.select(possible_patterns)
        self.grid.place_pattern(point, chosen_pattern)

        is_zero_entropy = self.grid.update_neighbors_entropy(point)
        if is_zero_entropy and early_stopping:
            return False

        return True

    def generate(self) -> bool:
        """Run the generation process until the grid is fully collapsed or fails."""
        self.initialize()
        while not self.is_complete():
            if not self.step():
                return False
        return True

    def is_complete(self) -> bool:
        """Check if the grid has been fully collapsed."""
        return self.grid.is_collapsed()
