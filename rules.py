from direction import Direction


class NeighborRuleSet:
    def __init__(
        self, allowed_up=None, allowed_down=None, allowed_left=None, allowed_right=None
    ):
        self.allowed_neighbors = {
            Direction.UP: allowed_up or set(),
            Direction.DOWN: allowed_down or set(),
            Direction.LEFT: allowed_left or set(),
            Direction.RIGHT: allowed_right or set(),
        }

    def get_allowed_neighbors(self, direction):
        return self.allowed_neighbors[direction]
