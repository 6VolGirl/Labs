import numpy as np
from LinearSystemMethodBase import LinearSystemMethodBase


class IterativeMethodBase(LinearSystemMethodBase):
    """Базовый класс для итерационных методов решения СЛАУ"""

    def __init__(self, name: str):
        super().__init__(name)
        #self.convergence_rate = None
        self.is_converged = False # Сходимость

    def _validate_iterative_system(self, A: np.ndarray, b: np.ndarray) -> None:
        """
        Проверка диагонального преобладания (ненулевая диагональ)
        """
        self._validate_system(A, b)

        if np.any(np.diag(A) == 0):
            raise ValueError("Диагональные элементы матрицы не равны нулю")

    def _initialize_vector(self, n: int, x0: [np.ndarray]) -> np.ndarray:
        """Инициализация начального приближения"""
        if x0 is None:
            return np.zeros(n)
        else:
            if len(x0) != n:
                raise ValueError(f"Размерность x0 ({len(x0)}) не совпадает с размерностью системы ({n})")
            return x0.copy()

    def _compute_residual_norm(self, x_new: np.ndarray, x_old: np.ndarray) -> np.floating:
        """Вычисление невязки между итерациями"""
        return np.linalg.norm(x_new - x_old)   #Норма вектора или матрицы

#    def _estimate_convergence_rate(self) -> float:
#        """Оценка скорости сходимости"""
#        if len(self.residuals) < 2:
#            return None
#
#        n_samples = min(5, len(self.residuals) - 1)
#        rates = []
#
#        for i in range(len(self.residuals) - n_samples, len(self.residuals) - 1):
#            if self.residuals[i] > 0:
#                rate = self.residuals[i + 1] / self.residuals[i]
#                rates.append(rate)
#
#        return np.mean(rates) if rates else None
