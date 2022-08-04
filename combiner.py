from numpy import ndarray
from mutator_base import BaseMutator

def combine(base: bytes, mutators: "list[tuple[BaseMutator, ndarray]]") -> bytes:
    """
    Chain mutators together and produce a single output.
    """
    for mut, vec in mutators:
        base = mut.get_mutation(base, vec)
    return base

def apply(text: bytes, mutators: "list[BaseMutator]", vec: ndarray) -> bytes:
    """
    Chain the given mutators with the overall vector.
    """
    start = 0
    output = []
    for m in mutators:
        end = start + m.get_dimension()
        output.append((m, vec[start:end]))
        start = end
    return combine(text, output)

def get_dim(mutators: "list[BaseMutator]"):
    return sum(m.get_dimension() for m in mutators)