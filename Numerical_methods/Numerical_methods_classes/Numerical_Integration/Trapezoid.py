import numpy as np
import sys
sys.path.append ("C:\\Users\\6anna\\PycharmProjects\\Labs\\Numerical_methods\\Numerical_methods_classes")
from IntegrationMethodBase import IntegrationMethodBase

class Trapezoid(IntegrationMethodBase):
    """ Метод трапеции для интегрирования определённых интегралов """
    def __init__(self, name: str = "Метод трапеции", order: int = 1):
        super().__init__(name, order)

    def integrate (self, f, a: float, b: float, n: int) -> float:
        self._validate_integration_params(a, b, n)

        h = (b - a) / n
        self.nodes = np.linspace(a, b, n + 1)

        # Веса: [h/2, h, h, ..., h, h/2]
        self.weights = np.full(n + 1, h)
        self.weights[0] = h / 2
        self.weights[-1] = h / 2

        f_values = np.array([f(x) for x in self.nodes])
        integral = np.sum(self.weights * f_values)

        self.n_points = n + 1
        self.result = integral

        return self.result