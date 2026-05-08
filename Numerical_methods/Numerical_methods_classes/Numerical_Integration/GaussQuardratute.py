import numpy as np
import sys
sys.path.append ("C:\\Users\\6anna\\PycharmProjects\\Labs\\Numerical_methods\\Numerical_methods_classes")
from IntegrationMethodBase import IntegrationMethodBase


class GaussQuadrature(IntegrationMethodBase):
    """ Квадратурная формула Гаусса для численного интегрирования """

    def __init__(self, name: str = "Квадратура Гаусса", order: int = None):
        super().__init__(name, order if order is not None else 3)

    def integrate(self, f, a: float, b: float, n: int) -> float:
        """ Вычисление определенного интеграла методом Гаусса """
        self._validate_integration_params(a, b, n)

        xi, A = self._get_gauss_nodes_weights_standard(n)

        # s = (b-a)/2 * ξ + (a+b)/2
        self.nodes = (b - a) / 2 * xi + (a + b) / 2
        self.weights = (b - a) / 2 * A

        # ∫f(s)ds ≈ Σ w_j * f(s_j)
        f_values = np.array([f(x) for x in self.nodes])
        integral = np.sum(self.weights * f_values)

        self.n_points = n
        self.result = integral

        return self.result

    def _get_gauss_nodes_weights_standard(self, n: int):
        """ Получить узлы и веса Гаусса на стандартном отрезке [-1, 1] """
        if n == 1:
            xi = np.array([0.0])
            A = np.array([2.0])

        elif n == 2:
            xi = np.array([-1.0 / np.sqrt(3), 1.0 / np.sqrt(3)])
            A = np.array([1.0, 1.0])

        elif n == 3:
            xi = np.array([-np.sqrt(3.0 / 5.0), 0.0, np.sqrt(3.0 / 5.0)])
            A = np.array([5.0 / 9.0, 8.0 / 9.0, 5.0 / 9.0])

        elif n == 4:
            xi = np.array([
                -0.861136311594053,
                -0.339981043584856,
                0.339981043584856,
                0.861136311594053
            ])
            A = np.array([
                0.347854845137454,
                0.652145154862546,
                0.652145154862546,
                0.347854845137454
            ])

        elif n == 5:
            xi = np.array([
                -0.906179845938664,
                -0.538469310105683,
                0.0,
                0.538469310105683,
                0.906179845938664
            ])
            A = np.array([
                0.236926885056189,
                0.478628670499366,
                0.568888888888889,
                0.478628670499366,
                0.236926885056189
            ])

        elif n == 10:
            xi = np.array([
                -0.973906528517172,
                -0.865063366688985,
                -0.679409568299024,
                -0.433395394129247,
                -0.148874338981631,
                0.148874338981631,
                0.433395394129247,
                0.679409568299024,
                0.865063366688985,
                0.973906528517172
            ])
            A = np.array([
                0.066671344308688,
                0.149451349150581,
                0.219086362515982,
                0.269266719309996,
                0.295524224714753,
                0.295524224714753,
                0.269266719309996,
                0.219086362515982,
                0.149451349150581,
                0.066671344308688
            ])

        else:
            raise ValueError(
                f"Узлы и веса Гаусса для n={n} не реализованы.\n"
                f"Доступные значения: 1, 2, 3, 4, 5, 10.\n"
                f"Для других n используйте scipy.special.roots_legendre(n)"
            )

        return xi, A
