from dataclasses import dataclass, field


@dataclass()
class WeightedObject:
    weight: float = field(repr=False)
