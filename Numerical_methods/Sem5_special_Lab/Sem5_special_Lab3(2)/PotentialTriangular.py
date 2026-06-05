import numpy as np
from PotentialBase import PotentialBase


class PotentialTriangular(PotentialBase):
    """
    Треугольный периодический потенциал на [0, L]:
    U(x) = 0              при 0 <= x < x0
    U(x) = U0*(x-x0)/(L-x0) при x0 <= x < L
    (и периодическое продолжение)
    """

    def __init__(self, U0, x0, L):
        self.U0 = U0
        self.x0 = x0
        self.L = L

    def __call__(self, x):
        x = np.asarray(x, dtype=float) % self.L   # периодичность
        U = np.zeros_like(x)
        mask = x >= self.x0
        U[mask] = self.U0 * (x[mask] - self.x0) / (self.L - self.x0)
        return U if U.shape != () else float(U)

    def derivative(self, x):
        x = np.asarray(x, dtype=float) % self.L
        dU = np.zeros_like(x)
        mask = x >= self.x0
        dU[mask] = self.U0 / (self.L - self.x0)
        return dU if dU.shape != () else float(dU)