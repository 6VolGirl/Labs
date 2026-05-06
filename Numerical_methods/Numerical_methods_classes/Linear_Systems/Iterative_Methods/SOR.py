import numpy as np
from Numerical_methods_classes.IterativeMethodBase import IterativeMethodBase


class SOR(IterativeMethodBase):
    """
    Метод последовательной верхней релаксации для решения СЛАУ
    """

    def __init__(self, omega: float = 1.0):
        """
        Инициализация метода SOR

        - omega: параметр релаксации
        """
        super().__init__(f"Метод SOR (ω={omega})")
        self.omega = omega

        if not (0 < omega <= 2):
            raise ValueError("Параметр релаксации omega должен быть в интервале (0, 2)")

    def solve(self, A: np.ndarray, b: np.ndarray, x0: [np.ndarray] = None,
              tol: float = 1e-6, max_iter: int = 10000) -> np.ndarray:
        """
        Решение СЛАУ Ax = b методом SOR

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
                s1 = np.dot(A[i, :i], x[:i])

                s2 = np.dot(A[i, i + 1:], x_prev[i + 1:])

                x[i] = (1 - self.omega) * x_prev[i] + self.omega * (f[i] - s1 - s2) / A[i, i]

            error_rate = self._compute_relative_residual(A, x_prev, f)
            self.error_rates.append(error_rate)

            residual = self._compute_residual_norm(x, x_prev)
            self.residuals.append(residual)

            if residual < tol:
                self.result = x
                self.iterations_performed = k + 1
                self.is_converged = True
                print(f"Метод SOR сошёлся за {k + 1} итераций")
                print(f"Финальная невязка ||x^(k+1) - x^(k)||: {residual:.2e}")
                print(f"Финальная относительная невязка ||Ax-f||/||f||: {error_rate:.2e}")
                return self.result

        # Не достигли требуемой точности
        self.result = x
        self.iterations_performed = max_iter
        #print(f"Метод SOR не сошёлся, достигнуто максимальное число итераций ({max_iter})")
        #print(f"Финальная невязка ||x^(k+1) - x^(k)||: {self.residuals[-1]:.2e}")
        #print(f"Финальная относительная невязка ||Ax-f||/||f||: {self.error_rates[-1]:.2e}")

        return self.result

    def find_optimal_omega(self, A: np.ndarray, b: np.ndarray, x0: [np.ndarray] = None,
                           omega_range: tuple = (1.0, 1.99), n_trials: int = 20,
                           tol: float = 1e-6, max_iter: int = 10000) -> float:
        """
        Эмпирический подбор оптимального параметра релаксации omega

        - A, b: матрица системы и вектор правой части
        - x0: начальное приближение
        - omega_range: диапазон поиска параметра (min, max)
        - n_trials: число пробных значений omega
        - tol, max_iter: параметры решения
        """
        omega_values = np.linspace(omega_range[0], omega_range[1], n_trials)
        min_iterations = float('inf')
        best_omega = 1.0

        print(f"\nПоиск оптимального omega в диапазоне {omega_range}...")

        for omega_test in omega_values:
            sor_test = SOR(omega=omega_test)
            try:
                sor_test.solve(A, b, x0=x0, tol=tol, max_iter=max_iter)
                #converged_str = "Да" if sor_test.is_converged else "Нет"
                #print(f"{omega_test:<10.4f} {sor_test.iterations_performed:<12} {converged_str:<15}")

                if sor_test.is_converged and sor_test.iterations_performed < min_iterations:
                    min_iterations = sor_test.iterations_performed
                    best_omega = omega_test
            except Exception as e:
                print(f"{omega_test:<10.4f} {'Ошибка':<12} {str(e)[:15]:<15}")
                continue

        print("-" * 40)
        print(f"\nОптимальное omega: {best_omega:.4f}")
        print(f"Минимальное число итераций: {min_iterations}")

        return best_omega
