import numpy as np
from PotentialBase import PotentialBase

class PotentialSinusoidal(PotentialBase):
    """
    Вариант A из задания:
    U(x) = U0 * sin(2π x / L)
    """

    def __init__(self, U0, L):
        self.U0 = U0
        self.L = L

    def __call__(self, x):
        return self.U0 * np.sin(2.0 * np.pi * x / self.L)

    def derivative(self, x):
        return self.U0 * 2.0 * np.pi / self.L * np.cos(2.0 * np.pi * x / self.L)

