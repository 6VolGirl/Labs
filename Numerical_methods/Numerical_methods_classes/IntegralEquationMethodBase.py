import numpy as np
from BaseMethod import NumericalMethod


class IntegralEquationMethodBase(NumericalMethod):
    """ Базовый класс для методов решения интегральных уравнений """

    def __init__(self, name: str, equation_type):
        super().__init__(name)
        self.equation_type = equation_type
        self.t_values = None
        self.x_values = None
        self.n_points = 0
        self.integration_method = None  # метод для вычисления интегралов

    def set_integration_method(self, method):
        """Установить метод численного интегрирования"""
        self.integration_method = method
        return self

    def compute_error(self, exact_solution):
        """
        Вычисление погрешности решения
        """
        if self.t_values is None or self.x_values is None:
            raise ValueError("Сначала решите уравнение методом solve()")

        x_exact = np.array([exact_solution(t) for t in self.t_values])

        abs_errors = np.abs(self.x_values - x_exact)
        rel_errors = abs_errors / np.abs(x_exact)

        self.error_info = {
            'max_absolute': np.max(abs_errors),
            'mean_absolute': np.mean(abs_errors),
            'max_relative': np.max(rel_errors),
            'mean_relative': np.mean(rel_errors),
            'n_points': self.n_points
        }
        return self.error_info

    def _validate_params(self, a: float, b: float, n: int):
        """Проверка корректности параметров"""
        if a >= b:
            raise ValueError(f"Нижняя граница a={a} должна быть меньше верхней b={b}")
        if n <= 1:
            raise ValueError(f"Число узлов n={n} должно быть больше 1")

    def get_solution(self):
        """Возвращает решение"""
        if self.t_values is None or self.x_values is None:
            raise ValueError("Решение ещё не вычислено")
        return self.t_values, self.x_values

    def get_info(self):
        """Получение полной информации о вычислениях"""
        info = super().get_info()
        info.update({
            'equation_type': self.equation_type,
            'n_points': self.n_points,
            't_range': (self.t_values[0], self.t_values[-1]) if self.t_values is not None else None
        })
        return info
