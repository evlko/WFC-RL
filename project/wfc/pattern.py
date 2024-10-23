import os
from dataclasses import dataclass, field
from typing import List, Set, Union

from project.wfc.rules import NeighborRuleSet
from project.wfc.wobj import WeightedObject


@dataclass
class Pattern(WeightedObject):
    image_path: Union[str, os.PathLike]


@dataclass(unsafe_hash=True)
class MetaPattern(WeightedObject):
    uid: int
    name: str
    tags: Set[str] = field(compare=False, hash=False)
    rules: Union["NeighborRuleSet", None] = field(default=None, repr=False)
    patterns: List[Pattern] = field(default_factory=list, repr=False, hash=False)
