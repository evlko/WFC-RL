from dataclasses import dataclass, field
from typing import Dict, Set, Union

from project.wfc.direction import Direction
from project.wfc.pattern import MetaPattern


@dataclass
class NeighborRuleSet:
    allowed_up: Set[MetaPattern] = field(default_factory=set)
    allowed_down: Set[MetaPattern] = field(default_factory=set)
    allowed_left: Set[MetaPattern] = field(default_factory=set)
    allowed_right: Set[MetaPattern] = field(default_factory=set)

    def __post_init__(self):
        self.allowed_neighbors: Dict[Direction, Set[MetaPattern]] = {
            Direction.UP: self.allowed_up,
            Direction.RIGHT: self.allowed_right,
            Direction.DOWN: self.allowed_down,
            Direction.LEFT: self.allowed_left,
        }

    def get_allowed_neighbors(
        self, direction: Union[Direction, None] = None
    ) -> Union[Set[MetaPattern], Dict[Direction, Set[MetaPattern]]]:
        """Returns allowed neighbors for a given direction or all directions if none specified."""
        if direction is None:
            return self.allowed_neighbors.values()
        return self.allowed_neighbors.get(direction, set())
