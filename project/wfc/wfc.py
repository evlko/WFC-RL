from dataclasses import dataclass
from enum import Enum, auto

from project.wfc.grid import Grid, Point
from project.wfc.judge import Judge
from project.wfc.pattern import MetaPattern


class FailReason(Enum):
    COLLAPSED = auto()
    ZERO_CHOICE = auto()
    ZERO_ENTROPY = auto()


@dataclass
class StepResult:
    """Pessimistic step expectations bring us closer to a bright future."""

    success: bool = False
    chosen_point: Point | None = None
    chosen_pattern: MetaPattern | None = None
    failed_point: Point | None = None
    fail_reason: FailReason | None = None


class WFC:
    def __init__(self, grid: Grid, judge: Judge) -> None:
        self.grid = grid
        self.judge = judge
        self._is_initialized = False

    def _initialize(self) -> None:
        """Initialize the grid for the WFC process."""
        self.grid.initialize()
        self._is_initialized = True

    def step(self, early_stopping: bool = True) -> StepResult:
        """Perform one step in the WFC process: find, collapse, and update neighbors."""
        result = StepResult()
        if not self._is_initialized:
            self._initialize()

        # find point and fail if None
        point = self.grid.find_least_entropy_cell()
        result.chosen_point = point
        if point is None and early_stopping:
            result.fail_reason = FailReason.COLLAPSED
            return result

        # find possible patterns and fail if None
        possible_patterns = self.grid.get_valid_patterns(p=point)
        if not possible_patterns and early_stopping:
            result.fail_reason = FailReason.ZERO_CHOICE
            result.failed_point = point
            return result

        # get random pattern from judge and place it
        chosen_pattern = self.judge.select(objects=possible_patterns, grid=self.grid)
        result.chosen_pattern = chosen_pattern
        self.grid.place_pattern(p=point, pattern=chosen_pattern)

        # find a cell with zero entropy and fail if one such exists
        zero_entropy_cell = self.grid.update_neighbors_entropy(p=point)
        if zero_entropy_cell and early_stopping:
            result.fail_reason = FailReason.ZERO_ENTROPY
            result.failed_point = zero_entropy_cell
            return result

        # otherwise return success
        result.success = True
        return result

    def generate(self) -> bool:
        """Run the generation process until the grid is fully collapsed or fails."""
        self._initialize()
        while not self.is_complete():
            if not self.step().success:
                return False
        return True

    def is_complete(self) -> bool:
        """Check if the grid has been fully collapsed."""
        return self.grid.is_collapsed()
