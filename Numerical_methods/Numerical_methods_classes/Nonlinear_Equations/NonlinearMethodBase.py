import numpy as np
from ..BaseMethod import NumericalMethod

class NonlinearMethodBase(NumericalMethod):
    """Базовый класс для методов решения нелинейных уравнений"""

    def __init__(self, name: str):
        super().__init__(name)
        self.is_converged = False  # Сходимость


