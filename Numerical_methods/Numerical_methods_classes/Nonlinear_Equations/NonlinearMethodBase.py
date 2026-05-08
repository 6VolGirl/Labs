import numpy as np
import sys
sys.path.append ("C:\\Users\\6anna\\PycharmProjects\\Labs\\Numerical_methods\\Numerical_methods_classes")
from BaseMethod import NumericalMethod

class NonlinearMethodBase(NumericalMethod):
    """Базовый класс для методов решения нелинейных уравнений"""

    def __init__(self, name: str):
        super().__init__(name)
        self.is_converged = False  # Сходимость


