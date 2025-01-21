import os
from dataclasses import dataclass, field
from typing import Set, Tuple, Union

from project.wfc.wobj import WeightedObject


@dataclass(unsafe_hash=True)
class Pattern(WeightedObject):
    image_path: Union[str, os.PathLike]


@dataclass(unsafe_hash=True)
class MetaPattern(WeightedObject):
    uid: int
    name: str
    is_walkable: int
    tags: Set[str] = field(compare=False, hash=False)
    rules: Union["NeighborRuleSet", None] = field(default=None, repr=False, hash=False)  # type: ignore
    patterns: Tuple[Pattern] = field(default_factory=list, repr=False)
