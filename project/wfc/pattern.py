from dataclasses import dataclass, field
from typing import Set

from project.wfc.rules import NeighborRuleSet


@dataclass
class Pattern:
    uid: int
    image_path: str
    name: str
    tags: Set[str]
    weight: int = field(repr=False)
    rules: NeighborRuleSet = field(default=None, repr=False)
