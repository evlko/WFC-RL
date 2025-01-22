from abc import ABC, abstractmethod
from enum import Enum, auto


class ModelMode(Enum):
    TRAINIG = auto()
    EVALUATION = auto()


class Model(ABC):
    @abstractmethod
    def save_weights(filename: str):
        pass

    @abstractmethod
    def load_weights(filename: str):
        pass
