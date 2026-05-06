import numpy as np
from BaseMethod import NumericalMethod


class LinearSystemMethodBase(NumericalMethod):
    """Базовый класс для методов решения СЛАУ (прямых и итерационных)"""

    def __init__(self, name: str):
        super().__init__(name)
        self.iterations_performed = 0 # Число итераций
        self.residuals = []  # Невязки |x(k+1) - x(k)|
        self.error_rates = [] # Относительная невязка |Ax-f|/|f|

    def _validate_system(self, A: np.ndarray, b: np.ndarray) -> None:
        """
        Проверка корректности СЛАУ

        - A: матрица системы
        - b: вектор правой части
        """

        if A.shape[0] != A.shape[1]:
            raise ValueError(f"Матрица должна быть квадратной, размерность: {A.shape}")

        if A.shape[0] != len(b):
            raise ValueError(f"Разные размерности: A {A.shape}, b {len(b)}")

    def _compute_solution_residual(self, A: np.ndarray, x: np.ndarray, b: np.ndarray) -> float:
        """
        Невязка решения = |Ax - b| для СЛАУ
        """
        return np.linalg.norm(np.dot(A, x) - b)

    def _compute_relative_residual(self, A: np.ndarray, x: np.ndarray, b: np.ndarray) -> float:
        """
        Вычисление относительной невязки решения ||Ax - b|| / ||b||

        Возвращает:
        - относительную невязку (если ||b|| ≈ 0, возвращает абсолютную невязку)
        """
        absolute_residual = self._compute_solution_residual(A, x, b)
        norm_b = np.linalg.norm(b)

        if norm_b < 1e-14:
            return absolute_residual

        return absolute_residual / norm_b
