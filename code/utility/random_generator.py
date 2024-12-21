from numpy.random import uniform
from math import log


class RandomGenerator:
    def generate(self) -> float:
        raise NotImplementedError()


class PoissonGenerator(RandomGenerator):
    def __init__(self, lam):
        super().__init__()
        self._lam = float(lam)

    def generate(self):
        r = uniform(0, 1)
        value = -1.0 / self._lam * log(r)
        return min(value, 50.0)


class UniformGenerator(RandomGenerator):
    def __init__(self, a, b):
        super().__init__()
        self._a = a
        self._b = b

    def generate(self):
        return uniform(self._a, self._b)
