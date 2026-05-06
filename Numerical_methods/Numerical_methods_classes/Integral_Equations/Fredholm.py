import numpy as np
from ..IntegralEquationMethodBase import IntegralEquationMethodBase
from Numerical_Integration.Trapezoid import Trapezoid
from Numerical_Integration.GaussQuardratute import GaussQuadrature


class Fredholm(IntegralEquationMethodBase):
    """
    Класс для решения интегральных уравнений Фредгольма второго рода:
    x(t) = λ ∫ₐᵇ K(t,s) x(s) ds + f(t)
    """

    def __init__(self, lam: float = 1.0, integration_method=None):
        """
        lam : параметр λ в уравнении
        integration_method метод интегрирования. Может быть:
            - объектом класса (Trapezoid(), GaussQuadrature())
            - None (по умолчанию используется метод трапеций)
        """
        super().__init__("Метод Фредгольма", equation_type="Fredholm")
        self.lam = lam

        # Установка метода интегрирования
        if integration_method is None:
            self.integration_method = Trapezoid()
            self.method_name = "Трапеции"
        else:
            self.integration_method = integration_method
            self.method_name = integration_method.name if hasattr(integration_method, 'name') else "Пользовательский"

    def solve(self, kernel, f, a: float, b: float, n: int = 100):
        """
        Решение уравнения Фредгольма квадратурным методом

        kernel: функция ядра K(t, s)
        f : функция правой части f(t)
        n :число узлов
        """
        self._validate_params(a, b, n)

        nodes, weights = self._get_nodes_and_weights(a, b, n)
        self.t_values = nodes
        self.n_points = len(nodes)

        # Матрица системы (I - λWK)x = f
        A = np.eye(self.n_points) # единичная
        f_vec = np.array([f(t) for t in self.t_values])

        for i in range(self.n_points):
            for j in range(self.n_points):
                K_val = kernel(self.t_values[i], self.t_values[j])
                A[i, j] -= self.lam * weights[j] * K_val

        self.x_values = np.linalg.solve(A, f_vec)   # решает СЛАУ
        self.result = (self.t_values, self.x_values)

        return self.result

    def _get_nodes_and_weights(self, a: float, b: float, n: int):
        """
        Получить узлы и веса от выбранного метода интегрирования
        """
        if isinstance(self.integration_method, Trapezoid):
            h = (b - a) / (n - 1)
            nodes = np.linspace(a, b, n)
            weights = np.full(n, h)
            weights[0] = h / 2
            weights[-1] = h / 2

        elif isinstance(self.integration_method, GaussQuadrature):
            nodes, weights = self._gauss_nodes_weights(a, b, n)
        else:
            # Если метод не определён пытаемся найти аналогичные поля
            dummy_func = lambda x: 1.0
            self.integration_method.integrate(dummy_func, a, b, n)
            nodes = self.integration_method.nodes
            weights = self.integration_method.weights

        return nodes, weights

    def _gauss_nodes_weights(self, a: float, b: float, n: int):
        """ Получить узлы и веса Гаусса на отрезке [a, b] """
        # Узлы и веса на [-1, 1]
        xi, A = self._get_gauss_params(n)
        nodes = (b - a) / 2 * xi + (a + b) / 2
        weights = (b - a) / 2 * A
        return nodes, weights

    def _get_gauss_params(self, n: int):
        """ Таблица узлов и весов Гаусса для отрезка [-1, 1] """
        gaus = GaussQuadrature(n)
        xi, A = gaus._get_gauss_nodes_weights_standard(n)
        return xi, A


#class Fredholm(IntegralEquationMethodBase):
#    """
#    Решение интегральных уравнений Фредгольма второго рода:
#    x(t) + λ ∫ₐᵇ K(t,s) x(s) ds = f(t)
#    """
#
#    def __init__(self, lam: float = 1.0, integration_method=None):
#        """
#        - lam: параметр λ в уравнении
#        """
#        super().__init__("Метод решения уравнений Фредгольма", equation_type="Fredholm")
#        self.lam = lam
#        self.integration_method = Trapezoid()
#
#    def solve(self, kernel, f, a: float, b: float, n: int = 100):
#        """
#        Решение уравнения Фредгольма методом дискретизации
#
#        - kernel: функция ядра K(t, s)
#        - f: функция правой части f(t)
#        - n: число узлов
#        """
#        self._validate_params(a, b, n)
#
#        self.t_values = np.linspace(a, b, n)
#        self.n_points = n
#        h = (b - a) / (n - 1)
#
#        # (I + λ*K) x = f, где K — матрица квадратурных коэффициентов
#        A = np.eye(n)  # единичная матрица
#        f_vec = np.array([f(t) for t in self.t_values])
#
#        for i in range(n):
#            for j in range(n):
#                K_val = kernel(self.t_values[i], self.t_values[j])
#
#                if j == 0 or j == n - 1:
#                    weight = h / 2
#                else:
#                    weight = h
#
#                A[i, j] += self.lam * weight * K_val
#
#        self.x_values = np.linalg.solve(A, f_vec)   #решает систему
#        self.result = (self.t_values, self.x_values)
#
#        return self.result
