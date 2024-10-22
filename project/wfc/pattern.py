import os
from dataclasses import dataclass, field
from typing import Set, Union

from project.wfc.wobj import WeightedObject
from project.wfc.rules import NeighborRuleSet


@dataclass(unsafe_hash=True)
class Pattern(WeightedObject):
    uid: int
    image_path: Union[str, os.PathLike]
    name: str
    tags: Set[str] = field(compare=False, hash=False) 
    rules: Union["NeighborRuleSet", None] = field(default=None, repr=False)
