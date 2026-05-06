import numpy as np
from DirectMethodBase import DirectMethodBase

class PeriodicTridiagonalAlgorithm(DirectMethodBase):
    """
    Циклическая (периодическая) прогонка для системы
    a[i]*x[i-1] + b[i]*x[i] + c[i]*x[i+1] = d[i],
    с периодическими ГУ: x[-1] связан с x[0] и x[N-1].
    """

    def __init__(self, tolerance: float = 1e-10, name: str = "Периодическая прогонка"):
        super().__init__(name)
        self.tolerance = tolerance
        self.iterations_count = 0

    def solve(self, a: np.ndarray, b: np.ndarray, c: np.ndarray, d: np.ndarray) -> np.ndarray:
        """
        a, b, c, d: массивы длины N
        a[i] – коэффициент при x[i-1]
        b[i] – при x[i]
        c[i] – при x[i+1]
        d[i] – правая часть
        """
        a = np.asarray(a, dtype=float)
        b = np.asarray(b, dtype=float)
        c = np.asarray(c, dtype=float)
        d = np.asarray(d, dtype=float)

        N = len(d)
        if not (len(a) == len(b) == len(c) == N):
            raise ValueError("Длины a, b, c, d должны совпадать")

        cp = np.zeros(N)
        dp = np.zeros(N)

        if abs(b[0]) < self.tolerance:
            raise ValueError("b[0] слишком мал для стабильного начала прогонки")

        cp[0] = c[0] / b[0]
        dp[0] = d[0] / b[0]

        for i in range(1, N - 1):
            denom = b[i] - a[i] * cp[i - 1]
            if abs(denom) < self.tolerance:
                raise ValueError(f"Деление на малое число на шаге i={i}")
            cp[i] = c[i] / denom
            dp[i] = (d[i] - a[i] * dp[i - 1]) / denom

        # учёт периодичности в последнем уравнении
        denom_last = b[N - 1] - a[N - 1] * cp[N - 2]
        if abs(denom_last) < self.tolerance:
            raise ValueError("Деление на малое число в последнем уравнении")
        dp[N - 1] = (d[N - 1] - a[N - 1] * dp[N - 2]) / denom_last

        x = np.zeros(N)
        x[N - 1] = dp[N - 1]
        for i in range(N - 2, -1, -1):
            x[i] = dp[i] - cp[i] * x[i + 1]

        self.iterations_count = 2 * N
        return x
