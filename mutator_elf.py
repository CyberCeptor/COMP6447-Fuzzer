import numpy as np
from mutator_base import BaseMutator
import random

class ELFInsertMutator(BaseMutator):
    def get_mutation(self, text: bytes, input: np.ndarray) -> bytes:
        index = int.from_bytes(input[0].tobytes()[2:4], "little") % len(text)
        insert = int.from_bytes(input[1].tobytes()[2:7], "little") % len(text)
        return text[:index] + insert.to_bytes(5, "little") + text[index:]

    def get_dimension(self) -> "int":
        """
        First element of vector = index to insert
        First element of vector = byte to insert
        """
        return 2

class ELFReplaceMutator(BaseMutator):
    def get_mutation(self, text: bytes, input: np.ndarray) -> bytes:
        start = int.from_bytes(input[0].tobytes()[2:4], "little") % len(text)
        end = int.from_bytes(input[1].tobytes()[2:4], "little") % len(text)
        insert = int.from_bytes(input[2].tobytes()[2:6], "little") % len(text)
        if end < start:
            return text[:end] + insert.to_bytes(4, "little") + text[start:]
        else:
            return text[:start] + insert.to_bytes(4, "little") + text[end:]

    def get_dimension(self) -> "int":
        """
        First element of vector = index to insert
        First element of vector = byte to insert
        """
        return 3

class ELFAppendMutator(BaseMutator):
    def get_mutation(self, text: bytes, input: np.ndarray) -> bytes:
        start = int.from_bytes(input[0].tobytes()[2:4], "little") % len(text)
        end = int.from_bytes(input[1].tobytes()[2:4], "little") % len(text)

        if end < start:
            return text[:end] + text[start:] + text[end:start]
        else:
            return text[:start] + text[end:] + text[start:end]

    def get_dimension(self) -> "int":
        """
        First element of vector = start index
        First element of vector = end index
        """
        return 2

class ELFShuffleMutator(BaseMutator):
    def get_mutation(self, text: bytes, input: np.ndarray) -> bytes:
        start = int.from_bytes(input[0].tobytes()[2:4], "little") % len(text)
        end = int.from_bytes(input[1].tobytes()[2:4], "little") % len(text)

        if end < start:
            shuffled = bytearray(text[end:start])
            random.shuffle(shuffled)
            return text[:end] + bytes(shuffled) + text[start:]
        else:
            shuffled = bytearray(text[start:end])
            random.shuffle(shuffled)
            return text[:start] + bytes(shuffled) + text[end:]

    def get_dimension(self) -> "int":
        """
        First element of vector = start index
        First element of vector = end index
        """
        return 2
