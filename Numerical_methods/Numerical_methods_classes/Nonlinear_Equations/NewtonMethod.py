import numpy as np
from NonlinearMethodBase import NonlinearMethodBase

class NewtonMethod(NonlinearMethodBase):
    """Решение нелинейных уравнений методом Ньютона"""
    def __init__(self, name: str = "Newton"):
        super().__init__(name)
        self.iterations  = 0
        self.x_values = []
        self.f_values = []
        self.result = None
        self.abs_error = []
        self.rel_error = []
        self.is_scalar = True

    def solve(self, x0, f, df, tol=1e-8, max_iter=100):
        """
        Решает уравнение f(x) = 0 методом Ньютона.

        - x0: начальное приближение (скаляр или вектор)
        - f: функция f(x) -> скаляр или вектор
        - df: производная/Якоби df(x) -> скаляр, число или матрица
        - tol: точность
        - max_iter: максимум итераций
        """
        x0_arr = np.asarray(x0, dtype=float)
        self.is_scalar = (x0_arr.ndim == 0 or x0_arr.size == 1)

        if self.is_scalar:
            return self._solve_scalar(x0_arr.item(), f, df, tol, max_iter)
        else:
            return self._solve_vector(x0_arr, f, df, tol, max_iter)

    def _solve_scalar(self, x0, f, df, tol, max_iter):
        self.x_values = [x0]
        self.f_values = [abs(f(x0))]
        self.abs_error = []
        self.rel_error = []
        x = x0

        for k in range(max_iter):
            f_val = f(x)
            df_val = float(np.asarray(df(x)))

            if abs(df_val) < 1e-10:
                raise ZeroDivisionError(
                    f"Производная f'(x) ≈ 0 в точке x = {x}. "
                    f"Метод Ньютона невозможен."
                )

            x_new = x - f_val / df_val

            self.x_values.append(x_new)
            self.f_values.append(abs(f(x_new)))

            absolute_err = abs(x_new - x)
            self.abs_error.append(absolute_err)

            rel_err = absolute_err / max(abs(x_new), 1e-14)
            self.rel_error.append(rel_err)

            if absolute_err < tol:
                self.result = x_new
                self.iterations = k + 1
                return x_new

            x = x_new
            self.iterations = k

        raise RuntimeError(
            f"Метод не сошёлся за {max_iter} итераций. "
            f"Последняя ошибка: {absolute_err:.2e}"
        )

    def _solve_vector(self, x0, f, df, tol, max_iter):
        self.x_values = [x0.copy()]
        f_val_0 = np.asarray(f(x0))
        self.f_values = [np.linalg.norm(f_val_0)]
        self.abs_error = []
        self.rel_error = []
        x = x0.copy()
        n = len(x0)

        for k in range(max_iter):
            f_val = np.asarray(f(x))

            # Якобиан
            J = np.zeros((n, n))
            eps = 1e-8
            f_x = f_val

            for j in range(n):
                x_pert = x.copy()
                x_pert[j] += eps
                f_pert = np.asarray(f(x_pert))
                J[:, j] = (f_pert - f_x) / eps

            # Решаем J * delta = -f
            try:
                delta = np.linalg.solve(J, -f_val)
            except np.linalg.LinAlgError:
                raise ValueError("Матрица Якоби вырождена")

            x_new = x + delta

            self.x_values.append(x_new.copy())
            f_new = np.asarray(f(x_new))
            self.f_values.append(np.linalg.norm(f_new))

            absolute_err = np.linalg.norm(x_new - x)
            self.abs_error.append(absolute_err)

            rel_err = absolute_err / max(np.linalg.norm(x_new), 1e-12)
            self.rel_error.append(rel_err)

            if absolute_err < tol:
                self.result = x_new
                self.iterations = k + 1
                return x_new

            x = x_new
            self.iterations = k

        raise RuntimeError(f"Не сошлось за {max_iter} итераций")