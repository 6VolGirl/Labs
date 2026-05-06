import numpy as np
from DirectMethodBase import DirectMethodBase

class TridiagonalMatrixAlgorithm(DirectMethodBase):
    """
        Алгоритм решения трёхдиагональной системы методом прогонки
        Решает систему Ax = b, где A имеет вид:
        | a1  c1   0   0  ...  0  |
        | b1  a2  c2   0  ...  0  |
        | 0   b2  a3  c3  ...  0  |
        | ... ... ... ... ... ... |
        | 0   0  ... b(n-1) an |
        """

    def __init__(self, tolerance: float = 1e-10, name: str = "Прогонка"):
        super().__init__(name)
        self.tolerance = tolerance
        self.iterations_count = 0
        self.is_tridiagonal = False

#    def solve(self, a: np.ndarray, c: np.ndarray, b: np.ndarray, f: np.ndarray) -> np.ndarray:
#        """
#            a: поддиагональ,
#            c: главная диагональ,
#            b: наддиагональ,
#            f: вектор правых частей
#        """
#        n = len(f)
#        a = np.asarray(a, dtype=float)
#        b = np.asarray(b, dtype=float)
#        c = np.asarray(c, dtype=float)
#        f = np.asarray(f, dtype=float)
#
#        if c.size != n or a.size != n - 1 or b.size != n - 1:
#            raise ValueError("Размеры диагоналей/вектора f не согласованы")
#
#        alpha, beta = self._forward_pass(c, a, b, f, n)
#        x = self._backward_pass(alpha, beta, n)
#
#        self.iterations_count = 2 * n
#        return x


    def solve(self, A: np.ndarray, f: np.ndarray) -> np.ndarray:
        """
        A: трёхдиагональная матрица
        f: вектор правых частей
        """

        def solve(self, A: np.ndarray, f: np.ndarray) -> np.ndarray:
            """
            A: трёхдиагональная матрица
            f: вектор правых частей
            """

        n = len(f)
        A = np.asarray(A, dtype=float)
        f = np.asarray(f, dtype=float)

        # Валидация входных данных
        if A.shape != (n, n):
            raise ValueError(
                f"Матрица должна быть квадратной (n × n). "
                f"Получена форма {A.shape}"
            )

        if len(f) != n:
            raise ValueError(
                f"Размер вектора f ({len(f)}) не совпадает с размером матрицы ({n})"
            )
        self._validate_tridiagonal(A, n)
        c, a, b = self._extract_diagonals(A, n)

        alpha, beta = self._forward_pass(c, a, b, f, n)

        x = self._backward_pass(alpha, beta, n)

        self.iterations_count = 2 * n
        return x

    def _extract_diagonals(self, A: np.ndarray, n: int):
        """
        Извлечь три диагонали матрицы согласно классической форме
        Матрица A имеет вид:
        ┌                    ┐
        │ c₀  -b₀   0  ...  │
        │ -a₁  c₁ -b₁ ...  │
        │  0  -a₂  c₂ ...  │
        │  ...  ...  ...    │
        └                    ┘
        """
        c = np.diag(A)
        a = np.zeros(n)
        b = np.zeros(n)

        for i in range(1, n):
            a[i] = -A[i, i - 1]
        for i in range(n - 1):
            b[i] = -A[i, i + 1]
        return c, a, b

    def _forward_pass(self, c: np.ndarray, a: np.ndarray, b: np.ndarray, f: np.ndarray, n: int) :
        """
        Прямой ход метода прогонки
        αᵢ₊₁ = bᵢ / (cᵢ - aᵢ·αᵢ),         i = 1, ..., n-1
        βᵢ₊₁ = (fᵢ + aᵢ·βᵢ) / (cᵢ - aᵢ·αᵢ), i = 1, ..., n-1

        - c: главная диагональ
        - a: поддиагональ
        - b: наддиагональ
        - f: вектор правых частей
        - n: размер системы
        """
        alpha = np.zeros(n + 1)
        beta = np.zeros(n + 1)

        if abs(c[0]) < self.tolerance:
            raise ValueError(
                f"Начальный диагональный элемент c[0] = {c[0]:.6e} "
                f"близок к нулю (допуск: {self.tolerance})"
            )

        alpha[1] = b[0] / c[0]
        beta[1] = f[0] / c[0]

        for i in range(1, n):
            denominator = c[i] - a[i] * alpha[i]

            if abs(denominator) < self.tolerance:
                raise ValueError(
                    f"На итерации i={i}: знаменатель = {denominator:.6e} "
                    f"близок к нулю. "
                )

            if i < n - 1:
                alpha[i + 1] = b[i] / denominator

            beta[i + 1] = (f[i] + a[i] * beta[i]) / denominator

        return alpha, beta

    def _backward_pass(self, alpha: np.ndarray, beta: np.ndarray, n: int) -> np.ndarray:
        """
        Обратный ход метода прогонки (восстановление решения)
        xₙ = βₙ₊₁
        xᵢ = αᵢ₊₁·xᵢ₊₁ + βᵢ₊₁,   i = n-1, n-2, ..., 0

        - alpha: прогоночные коэффициенты α
        - beta: прогоночные коэффициенты β
        - n: размер системы
        """
        x = np.zeros(n)
        x[n - 1] = beta[n]

        for i in range(n - 2, -1, -1):
            x[i] = alpha[i + 1] * x[i + 1] + beta[i + 1]

        return x


    def _validate_tridiagonal(self, A: np.ndarray, n: int) -> None:
        """
        Проверить, что матрица строго трёхдиагональна
        """
        non_tridiagonal_elements = []

        for i in range(n):
            for j in range(n):
                if abs(i - j) > 1:
                    if abs(A[i, j]) > self.tolerance:
                        non_tridiagonal_elements.append({
                            'position': (i, j),
                            'value': A[i, j]
                        })

        if non_tridiagonal_elements:
            error_msg = "ОШИБКА: Матрица НЕ является трёхдиагональной!\n"
            error_msg += " Найдены ненулевые элементы вне трёх диагоналей:\n"
            for elem in non_tridiagonal_elements[:5]:
                i, j = elem['position']
                error_msg += f"    A[{i},{j}] = {elem['value']:.6e} (допуск: {self.tolerance})\n"

            if len(non_tridiagonal_elements) > 5:
                error_msg += f"    ... и ещё {len(non_tridiagonal_elements) - 5} элементов\n"

            raise ValueError(error_msg)

        self.is_tridiagonal = True


