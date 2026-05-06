# IntegrationMethodBase.py
import numpy as np
from BaseMethod import NumericalMethod


class IntegrationMethodBase(NumericalMethod):
    """ Базовый класс для методов численного интегрирования """

    def __init__(self, name: str, order: int = 1):
        super().__init__(name)
        self.order = order
        self.n_points = 0  # узлы (число)
        self.nodes = None  # узлы квадратуры
        self.weights = None  # веса квадратуры

    def compute_error(self, exact_value: float, integral_value):
        """
        Вычисление погрешности интегрирования
        """
        if integral_value is None:
            raise ValueError("Сначала выполните интегрирование методом integrate()")

        abs_error = abs(integral_value - exact_value)
        rel_error = abs_error / abs(exact_value) if exact_value != 0 else float('inf')

        self.error_info = {
            'absolute': abs_error,
            'relative': rel_error,
        }

        return self.error_info

    def _validate_integration_params(self, a: float, b: float, n: int):
        """Проверка корректности параметров интегрирования"""
        if a >= b:
            raise ValueError(f"Нижний предел a={a} должен быть меньше верхнего предела b={b}")
        if n <= 0:
            raise ValueError(f"Число узлов n={n} должно быть положительным")
        if not isinstance(n, int):
            raise TypeError(f"Число узлов n должно быть целым числом, получено {type(n)}")

    def get_nodes_and_weights(self):
        """
        Возвращает узлы и веса квадратурной формулы
        """
        if self.nodes is None or self.weights is None:
            raise ValueError("Узлы и веса не вычислены. Выполните интегрирование.")
        return self.nodes, self.weights

    def get_info(self):
        """Получение полной информации о вычислениях"""
        info = super().get_info()
        info.update({
            'order': self.order,
            'integral_value': self.integral_value,
            'n_points': self.n_points
        })
        return info
