import os
from dataclasses import dataclass, field
from typing import Set

from project.wfc.rules import NeighborRuleSet


@dataclass
class Pattern:
    uid: int
    image_path: str | os.PathLike
    name: str
    tags: Set[str]
    weight: int = field(repr=False)
    rules: NeighborRuleSet | None = field(default=None, repr=False)
