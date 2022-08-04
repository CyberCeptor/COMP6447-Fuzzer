from abc import abstractmethod, ABCMeta
from numpy import ndarray

"""
The base mutator class. Only exists for typing information.
"""

class BaseMutator(metaclass=ABCMeta):
    @abstractmethod
    def get_mutation(self, text: bytes, vector: ndarray) -> bytes:
        """
        Convert text to mutated output using vector.
        """
        raise NotImplementedError("Implement this")

    @abstractmethod
    def get_dimension(self) -> "int":
        """
        Get the input format for this mutator.
        Should be an integer saying how many dimensions are required.
        """
        raise NotImplementedError("Implement this")
