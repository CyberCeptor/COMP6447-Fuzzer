import numpy as np
from mutator_base import BaseMutator
from combiner import combine

class RepeatMutator(BaseMutator):
    def get_mutation(self, text: bytes, input: np.ndarray) -> bytes:
        repeat = int.from_bytes(input[0].tobytes()[2:4], "little")
        return text * repeat

    def get_dimension(self) -> "int":
        """
        First element of vector = number to repeat
        """
        return 1

class EmptyMutator(BaseMutator):
    def get_mutation(self, text: bytes, input: np.ndarray) -> bytes:
        return b""

    def get_dimension(self) -> "int":
        """
        No arguments as it's an empty string.
        """
        return 0

class SubstringMutator(BaseMutator):
    def get_mutation(self, text: bytes, input: np.ndarray) -> bytes:
        length = len(text)
        start = int.from_bytes(input[0].tobytes()[2:7], "little") % length
        end = int.from_bytes(input[1].tobytes()[2:7], "little") % length
        start, end = min(start, end), max(start, end)
        return text[start:end]

    def get_dimension(self) -> "int":
        """
        First element of vector = starting index
        Second element of vector = end index
        """
        return 2

class BitFlipMutator(BaseMutator):
    def get_mutation(self, text: bytes, input: np.ndarray) -> bytes:
        byte_idx = int.from_bytes(input[0].tobytes()[2:7], "big") % len(text)
        bit = int.from_bytes(input[1].tobytes()[2:7], "big") % 8
        new = bytearray(text)
        new[byte_idx] = new[byte_idx] ^ (1 << bit)
        return bytes(new)

    def get_dimension(self) -> "int":
        """
        First element of vector = which byte to flip
        Second element of vector = which bit inside that byte to flip
        """
        return 2

class ByteFlipMutator(BaseMutator):
    def get_mutation(self, text: bytes, input: np.ndarray) -> bytes:
        byte_idx = int.from_bytes(input[0].tobytes()[2:7], "big") % len(text)
        new = bytearray(text)
        new[byte_idx] = new[byte_idx] ^ 0xff
        return bytes(new)

    def get_dimension(self) -> "int":
        """
        First element of vector = which byte to flip
        """
        return 1

class PlaintextMutator(BaseMutator):
    """
    Apply the given mutators in sequence.
    """
    def __init__(self, mutators: "list[BaseMutator]"):
        self.mutators = mutators

    def get_mutation(self, text: bytes, input: np.ndarray) -> bytes:
        start = 0
        mutators = []
        for m in self.mutators:
            end = start + m.get_dimension()
            mutators.append((m, input[start:end]))
            start = end
        return combine(text, mutators)

    def get_dimension(self) -> "int":
        """
        Total number of args from each mutator.
        """
        return sum(m.get_dimension() for m in self.mutators)
