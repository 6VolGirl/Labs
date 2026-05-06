import numpy as np
from Numerical_methods_classes.IterativeMethodBase import IterativeMethodBase


class Jacobi(IterativeMethodBase):
    """Итерационный метод Якоби"""

    def __init__(self):
        super().__init__("Метод Якоби")

    def solve(self, A, b, x0: [np.ndarray] = None,
              tol: float = 1e-6, max_iter: int = 1000) -> np.ndarray:
        """
            - A: матрица системы (n×n)
            - f: вектор правой части (n)
            - x0: начальное приближение (если None, используется нулевой вектор)
            - max_iter: максимальное число итераций
            - tol: требуемая точность ||x^(k+1) - x^(k)|| < tol
        """

        self._validate_iterative_system(A, b)

        A = np.array(A, dtype=float)
        f = np.array(b, dtype=float)

        n = len(b)
        x = self._initialize_vector(n, x0)


        self.residuals = []
        self.error_rates = []
        self.is_converged = False

        for k in range(max_iter):
            x_new = np.zeros_like(x)  #массив нулей

            for i in range(n):
                s = np.dot(A[i, :], x) - A[i, i] * x[i]
                x_new[i] = (f[i] - s) / A[i, i]

                if np.isnan(x_new[i]):
                    raise ValueError(f"Получено NaN на итерации {k + 1}, строка {i}. "
                                     f"Проверьте диагональный элемент A[{i},{i}] = {A[i, i]}")

            residual = self._compute_residual_norm(x_new, x)
            self.residuals.append(residual)

            error_rate = self._compute_relative_residual(A, x, f)
            self.error_rates.append(error_rate)

            if residual < tol:
                self.result = x_new
                self.iterations_performed = k + 1
                self.is_converged = True
                print(f"Метод Якоби сошёлся за {k + 1} итераций")
                print(f"Финальная невязка ||x^(k+1) - x^(k)||: {residual:.2e}")
                print(f"Финальная относительная невязка ||Ax-f||/||f||: {error_rate:.2e}")
                return self.result

            x = x_new

        # Не достигли требуемой точности
        self.result = x
        self.iterations_performed = max_iter
        print(f"Метод Якоби не сошёлся, достигнуто максимальное число итераций ({max_iter})")
        print(f"Финальная невязка ||x^(k+1) - x^(k)||: {self.residuals[-1]:.2e}")
        print(f"Финальная относительная невязка ||Ax-f||/||f||: {self.error_rates[-1]:.2e}")

        return self.result