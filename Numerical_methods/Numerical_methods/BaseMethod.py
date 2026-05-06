import numpy as np


class NumericalMethod:
    """Базовый класс"""

    def __init__(self, name: str):
        """
        - name: название метода
        """
        self.name = name
        self.result = None
        self.error_info = {}  # Погрешность

    def get_result(self):
        """Возвращает результат вычислений"""
        return self.result

    def get_error_info(self):
        """Возвращает информацию о погрешностях"""
        return self.error_info

    def get_info(self):
        """
        Получение полной информации о вычислениях
        """
        return {
            'method': self.name,
            'result': self.result,
            'error_info': self.error_info
        }