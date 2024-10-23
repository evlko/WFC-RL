from dataclasses import dataclass, field


@dataclass(unsafe_hash=True)
class WeightedObject:
    weight: int = field(repr=False)
