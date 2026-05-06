
import numpy as np
from ...BaseMethod import NumericalMethod

class DirectMethodBase(NumericalMethod):
    """
    Базовый класс для прямых методов решения
    (аналитическое или одношаговое точное решение задачи).
    """

    def __init__(self, name: str):
        super().__init__(name)
        self.method_type = "direct"

    def solve(self, *args, **kwargs):
        """
        Интерфейс решения задачи.
        Должен быть переопределён в наследниках.
        """
        raise NotImplementedError(
            f"Метод solve() не реализован в классе {self.__class__.__name__}"
        )
