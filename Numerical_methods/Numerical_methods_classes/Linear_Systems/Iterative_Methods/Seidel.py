import numpy as np
from Numerical_methods_classes.IterativeMethodBase import IterativeMethodBase


class GaussSeidel(IterativeMethodBase):
    """Итерационный метод Гаусса-Зейделя для решения СЛАУ"""

    def __init__(self):
        super().__init__("Метод Гаусса-Зейделя")

    def solve(self, A: np.ndarray, b: np.ndarray, x0: [np.ndarray] = None,
              tol: float = 1e-6, max_iter: int = 10000) -> np.ndarray:
        """
        Решение СЛАУ Ax = b методом Гаусса-Зейделя

        - A: матрица системы (n×n)
        - b: вектор правой части (n)
        - x0: начальное приближение (если None, используется нулевой вектор)
        - tol: требуемая точность ||x^(k+1) - x^(k)|| < tol
        - max_iter: максимальное число итераций
        """
        self._validate_iterative_system(A, b)

        A = np.array(A, dtype=float)
        f = np.array(b, dtype=float)
        n = len(f)

        x = self._initialize_vector(n, x0)

        self.residuals = []
        self.error_rates = []
        self.is_converged = False

        for k in range(max_iter):
            x_prev = np.copy(x)

            for i in range(n):
                # s1 = sum(A_ij * x_j^(k+1), j < i) - обновленные значения
                s1 = np.dot(A[i, :i], x[:i])

                # s2 = sum(A_ij * x_j^(k), j > i) - старые значения
                s2 = np.dot(A[i, i + 1:], x_prev[i + 1:])

                x[i] = (f[i] - s1 - s2) / A[i, i]

            error_rate = self._compute_relative_residual(A, x_prev, f)
            self.error_rates.append(error_rate)

            residual = self._compute_residual_norm(x, x_prev)
            self.residuals.append(residual)

            if residual < tol:
                self.result = x
                self.iterations_performed = k + 1
                self.is_converged = True
                print(f"Метод Зейделя сходится за {k + 1} итераций")
                print(f"Финальная невязка ||x^(k+1) - x^(k)||: {residual:.2e}")
                print(f"Финальная относительная невязка ||Ax-f||/||f||: {error_rate:.2e}")
                return self.result

        # Не достигли требуемой точности
        self.result = x
        self.iterations_performed = max_iter
        print(f"Метод Зейделя не сошёлся, достигнуто максимальное число итераций ({max_iter})")
        print(f"Финальная невязка ||x^(k+1) - x^(k)||: {self.residuals[-1]:.2e}")
        print(f"Финальная относительная невязка ||Ax-f||/||f||: {self.error_rates[-1]:.2e}")

        return self.result
