from dataclasses import dataclass, field


@dataclass(unsafe_hash=True)
class WeightedObject:
    weight: float = field(repr=False)
