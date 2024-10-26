from dataclasses import dataclass

from project.wfc.grid import Grid
from project.wfc.judge import Judge


@dataclass
class StepResult:
    """Pessimistic step expectations bring us closer to a bright future."""

    success: bool = False


class WFC:
    def __init__(self, grid: Grid, judge: Judge):
        self.grid = grid
        self.judge = judge
        self._is_initialized = False

    def initialize(self):
        """Initialize the grid for the WFC process."""
        self.grid.initialize()
        self._is_initialized = True

    def step(self, early_stopping: bool = True) -> StepResult:
        """Perform one step in the WFC process: find, collapse, and update neighbors."""
        result = StepResult()

        if not self._is_initialized:
            self.initialize()

        point = self.grid.find_least_entropy_cell()
        if point is None and early_stopping:
            return result

        possible_patterns = self.grid.get_valid_patterns(point)
        if not possible_patterns and early_stopping:
            return result

        chosen_pattern = self.judge.select(possible_patterns)
        self.grid.place_pattern(point, chosen_pattern)

        zero_entropy_cell = self.grid.update_neighbors_entropy(point)
        if zero_entropy_cell and early_stopping:
            return result

        result.success = True
        return result

    def generate(self) -> bool:
        """Run the generation process until the grid is fully collapsed or fails."""
        self.initialize()
        while not self.is_complete():
            if not self.step().success:
                return False
        return True

    def is_complete(self) -> bool:
        """Check if the grid has been fully collapsed."""
        return self.grid.is_collapsed()
