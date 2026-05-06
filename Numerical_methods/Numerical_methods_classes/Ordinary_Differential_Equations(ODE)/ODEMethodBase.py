import numpy as np
from ..BaseMethod import NumericalMethod


class ODEMethodBase(NumericalMethod):
    """Базовый класс для методов решения обыкновенных дифференциальных уравнений"""

    def __init__(self, name: str, order: int):
        super().__init__(name)
        self.order = order

    def _validate_ode_params(self, t0: float, t_end: float, y0: np.ndarray, h: float) -> None:
        """
        Проверка параметров задачи Коши

        - t0: начальное время
        - t_end: конечное время
        - y0: начальное условие
        - h: шаг интегрирования
        """
        if t0 >= t_end + 1e-10:
            raise ValueError(f"Начальное время ({t0}) должно быть меньше конечного ({t_end})")

        if h <= 0:
            raise ValueError(f"Шаг интегрирования должен быть положительным: {h}")

        if h > (t_end - t0) + 1e-10:
            raise ValueError(f"Шаг ({h}) больше интервала интегрирования ({t_end - t0})")


    def _initialize_vector(self, dim, y0=None):
        """Инициализация вектора"""
        if y0 is None:
            return np.zeros(dim)
        return np.atleast_1d(y0).astype(float).copy()

    def compute_error(self, y_exact_func, t_values, y_numerical):
        """ Вычисление погрешности численного решения """
        if t_values is None or y_numerical is None:
            raise ValueError("Сначала необходимо решить задачу (вызвать solve)")

        t_values = np.atleast_1d(t_values)
        y_numerical = np.atleast_1d(y_numerical)

        if callable(y_exact_func):   # проверка можно ли вызвать этот объект или это просто значение
            y_exact = np.array([y_exact_func(t) for t in t_values])
        else:
            y_exact = np.atleast_1d(y_exact_func)
            y_exact = np.atleast_1d(y_exact)

        is_scalar = (y_numerical.ndim == 1) or (y_numerical.shape[-1] == 1 if y_numerical.ndim == 2 else False)

        # Приведение массивов к одинаковой форме
        if is_scalar:
            y_numerical = y_numerical.flatten()
            y_exact = y_exact.flatten()
        else:
            if y_exact.ndim == 1 and y_numerical.ndim == 2:
                raise ValueError(f"Несовпадение размерностей: y_exact {y_exact.shape}, y_numerical {y_numerical.shape}")

            if y_numerical.ndim == 1:
                y_numerical = y_numerical.reshape(-1, 1)
            if y_exact.ndim == 1:
                y_exact = y_exact.reshape(-1, 1)

        if y_numerical.shape != y_exact.shape:
            raise ValueError(
                f"Размеры численного ({y_numerical.shape}) и точного ({y_exact.shape}) решений не совпадают"
            )

        error_absolute = np.abs(y_numerical - y_exact)

        error_relative = np.zeros_like(error_absolute)
        mask = np.abs(y_exact) > 1e-14
        error_relative[mask] = error_absolute[mask] / np.abs(y_exact[mask])

        max_error = np.max(error_absolute)

        if is_scalar:
            norm_error = error_absolute
        else:
            norm_error = np.linalg.norm(y_numerical - y_exact, axis=1)

        self.error_info = {
            'absolute': error_absolute,
            'relative': error_relative,
            'max': max_error,
            'norm': norm_error,
            'y_exact': y_exact
        }
        return self.error_info

    def get_solution(self):
        """Возвращает решение"""
        return self.t_values, self.y_values
