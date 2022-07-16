
import random

class ByteFlipMutator():
    def __init__(self, sample:bytes):
        self.sample = bytearray(sample)
        self.attempts = list(range(0, len(self.sample)))
        random.shuffle(self.attempts)

    def __next__(self) -> bytearray:
        if len(self.attempts) == 0:
            raise StopIteration()
        flip = self.attempts.pop()
        new = bytearray(self.sample)
        new[flip] = new[flip] ^ 0xff
        return new

class BitFlipMutator():
    def __init__(self, sample:bytes):
        self.sample = bytearray(sample)
        self.attempts = [(byte, bit) for byte in range(0, len(self.sample)) for bit in range(8)]
        random.shuffle(self.attempts)

    def __next__(self) -> bytearray:
        if len(self.attempts) == 0:
            raise StopIteration()
        flip = self.attempts.pop()
        new = bytearray(self.sample)
        new[flip[0]] = new[flip[0]] ^ (1 << flip[1])
        return new

class EmptyMutator():
    def __init__(self, sample:bytes=b""):
        self.done = False

    def __next__(self) -> bytearray:
        if self.done:
            raise StopIteration()
        self.done = True
        return b""

class LongMutator():
    def __init__(self, sample:bytes):
        self.sample = bytearray(sample)
        self.choices = list(range(1, 10))
        random.shuffle(self.choices)

    def __next__(self) -> bytearray:
        if len(self.choices) == 0:
            raise StopIteration()
        return self.sample * (self.choices.pop() * 1000)

class BasicMutator():
    def __init__(self, sample:bytes):
        self.sample = sample
        self.mutators = [
            ByteFlipMutator(sample), BitFlipMutator(sample),
            EmptyMutator(sample), LongMutator(sample)]
        self.tried = {"empty":0, "long":0}

    def __iter__(self):
        return self

    def __next__(self) -> bytearray:
        if len(self.mutators) == 0:
            raise StopIteration()
        choice = random.choice(self.mutators)
        try:
            return next(choice)
        except StopIteration:
            self.mutators.remove(choice)
            return self.__next__()

def get_gen(sample_text:bytes):
    return BasicMutator(sample_text)

def main():
    # Simple testing.
    print("Testing \"hi\"")
    g = get_gen(b"hi")
    for i, _ in enumerate(g):
        pass
    print(f"\"hi\" had {i} tests")

if __name__ == "__main__":
    main()
