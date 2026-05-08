import numpy as np
import sys
sys.path.append ("C:\\Users\\6anna\\PycharmProjects\\Labs\\Numerical_methods\\Numerical_methods_classes")
from IterativeMethodBase import IterativeMethodBase


class SimpleIteration(IterativeMethodBase):
    """
    Метод простой итерации для решения СЛАУ
    """

    def __init__(self):
        super().__init__("Метод простой итерации")

    def _convert_to_iteration_form(self, A: np.ndarray, b: np.ndarray, method='jacobi'):
        """
        Преобразование системы Ax = b к виду x = Cx + d

        - A: матрица системы
        - b: вектор правой части
        - method: способ преобразования
          'jacobi' - C = I - D^(-1)A, d = D^(-1)b (диагональное преобладание)
          'manual' - пользователь сам приводит к итерационному виду
        """
        n = len(b)

        if method == 'jacobi':
            D = np.diag(np.diag(A))
            D_inv = np.linalg.inv(D)

            # C = I - D^(-1) * A
            C = np.eye(n) - np.dot(D_inv, A)

            # d = D^(-1) * b
            d = np.dot(D_inv, b)

            return C, d
        else:
            raise ValueError(f"Неизвестный метод преобразования: {method}")

    def _check_convergence_condition(self, C: np.ndarray) -> tuple:
        """
        Проверка условия сходимости метода

        Метод сходится, если ||C|| < 1 (в какой-либо норме)
        или если спектральный радиус ρ(C) < 1

        - C: матрица итерационной схемы
        """
        # Вычисляем спектральный радиус (максимум модулей собственных значений)
        eigenvalues = np.linalg.eigvals(C)
        spectral_radius = np.max(np.abs(eigenvalues))

        norm_C = np.linalg.norm(C, ord=np.inf)

        converges = spectral_radius < 1.0

        return converges, spectral_radius, norm_C

    def solve(self, A: np.ndarray, b: np.ndarray, x0=None, tol: float = 1e-6, max_iter: int = 1000,
              conversion_method: str = 'jacobi') -> np.ndarray:
        """
        Решение СЛАУ Ax = b методом простой итерации

        - A: матрица системы (n×n)
        - b: вектор правой части (n)
        - x0: начальное приближение
        - tol: требуемая точность ||x^(k+1) - x^(k)|| < tol
        - max_iter: максимальное число итераций
        - conversion_method: метод преобразования к итерационному виду
        """
        self._validate_iterative_system(A, b)

        A = np.array(A, dtype=float)
        f = np.array(b, dtype=float)
        n = len(f)

        # Преобразуем к виду x = Cx + d
        C, d = self._convert_to_iteration_form(A, f, method=conversion_method)

        converges, spec_radius, norm_C = self._check_convergence_condition(C)

        if not converges:
            print(f"Спектральный радиус >= 1, метод может не сойтись!")
        else:
            print(f"Сходится (ρ(C) < 1)")

        x = self._initialize_vector(n, x0)

        self.residuals = []
        self.error_rates = []
        self.is_converged = False

        for k in range(max_iter):
            x_new = np.dot(C, x) + d

            error_rate = self._compute_relative_residual(A, x, f)
            self.error_rates.append(error_rate)

            residual = self._compute_residual_norm(x_new, x)
            self.residuals.append(residual)

            if residual < tol:
                self.result = x_new
                self.iterations_performed = k + 1
                self.is_converged = True
                print(f"Простая итерация сходится за {k + 1} итераций")
                print(f"Финальная невязка ||x^(k+1) - x^(k)||: {residual:.2e}")
                print(f"Финальная относительная невязка ||Ax-f||/||f||: {error_rate:.2e}")
                return self.result

            x = x_new

        # Не достигли требуемой точности
        self.result = x
        self.iterations_performed = max_iter
        print(f"Простая итерация не сошлась, достигнуто максимальное число итераций ({max_iter})")
        print(f"Финальная невязка ||x^(k+1) - x^(k)||: {self.residuals[-1]:.2e}")
        print(f"Финальная относительная невязка ||Ax-f||/||f||: {self.error_rates[-1]:.2e}")

        return self.result

