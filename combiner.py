from numpy import ndarray
from mutator_base import BaseMutator

def combine(base: bytes, mutators: "list[tuple[BaseMutator, ndarray]]") -> bytes:
    """
    Chain mutators together and produce a single output.
    """
    for mut, vec in mutators:
        base = mut.get_mutation(base, vec)
    return base
