import numpy as np
from ..IntegralEquationMethodBase import IntegralEquationMethodBase
from Numerical_Integration.Trapezoid import Trapezoid

class Volterra(IntegralEquationMethodBase):
    """
    Решение интегральных уравнений Вольтерры второго рода:
    x(t) + ∫ₐᵗ K(t,s) x(s) ds = f(t)
    """

    def __init__(self, integration_method=None, lam: float = 0):
        super().__init__("Метод Вольтерра", equation_type="Volterra")
        self.lam = lam


        if integration_method is None:
            self.integration_method = Trapezoid()
            self.method_name = "Трапеции"
        else:
            self.integration_method = integration_method
            self.method_name = integration_method.name if hasattr(integration_method, 'name') else "Пользовательский"

    def solve(self, kernel, f, a: float, b: float, n: int = 100):
        """
         Решение уравнения Вольтерры

         - kernel: функция ядра K(t, s)
         - f: функция правой части f(t)
         - n: число узлов
         """
        self._validate_params(a, b, n)

        h = (b - a) / (n - 1)
        self.t_values = np.linspace(a, b, n)
        self.n_points = n
        self.x_values = np.zeros(n)
        self.x_values[0] = f(self.t_values[0])

        for i in range(1, n):
            t_i = self.t_values[i]

            # ∫ₐᵗⁱ K(t_i, s) x(s) ds
            if isinstance(self.integration_method, Trapezoid):
                integral = self._trapezoid_integral(kernel, t_i, a, i)
            # сюда можно добавлять другие методы интегрирования
            else:
                integral = self._trapezoid_integral(kernel, t_i, a, i)

            self.x_values[i] = self.lam * integral + f(t_i)

        self.result = (self.t_values, self.x_values)
        return self.result

    def _trapezoid_integral(self, kernel, t, a, i_max):
        """
        Универсальный метод интегрирования(использует трапеции)
        """
        h = (self.t_values[-1] - self.t_values[0]) / (self.n_points - 1)

        integral = 0.0
        for j in range(i_max):
            s_j = self.t_values[j]
            K_val = kernel(t, s_j)
            x_val = self.x_values[j]

            # Веса метода трапеций
            if j == 0:
                weight = h / 2
            elif j == i_max - 1:
                weight = h / 2
            else:
                weight = h

            integral += weight * K_val * x_val

        return integral