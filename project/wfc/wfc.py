from project.utils.utils import Utils
from project.wfc.grid import Grid


class WFC:
    def __init__(self, grid: Grid):
        self.grid = grid
        self._is_initialized = False

    def initialize(self):
        """Initialize the grid for the WFC process."""
        self.grid.initialize()
        self._is_initialized = True

    def step(self) -> bool:
        """Perform one step in the WFC process: find, collapse, and update neighbors."""
        if not self._is_initialized:
            self.initialize()

        cell = self.grid.find_least_entropy_cell()
        if cell is None:
            return False

        x, y = cell
        possible_patterns = self.grid.get_valid_patterns(x, y)
        if not possible_patterns:
            return False

        chosen_pattern = Utils.weighted_choice(possible_patterns)
        self.grid.place_pattern(x, y, chosen_pattern)

        is_early_stopping = self.grid.update_neighbors_entropy(x, y)

        if is_early_stopping:
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
