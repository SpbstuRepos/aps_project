from numpy.random import poisson, uniform


class RandomGenerator:
    def generate(self) -> float:
        raise NotImplementedError()


class PoissonGenerator(RandomGenerator):
    def __init__(self, lam):
        super().__init__()
        self._lam = lam

    def generate(self):
        return float(poisson(self._lam))


class UniformGenerator(RandomGenerator):
    def __init__(self, a, b):
        super().__init__()
        self._a = a
        self._b = b

    def generate(self):
        return uniform(self._a, self._b)
