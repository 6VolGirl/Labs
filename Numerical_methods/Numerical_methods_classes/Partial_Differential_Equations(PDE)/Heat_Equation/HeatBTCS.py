import numpy as np

from PDEMethodBase import PDEMethodBase
from TridiagonalMatrixAlgorithm import TridiagonalMatrixAlgorithm

class HeatBTCS(PDEMethodBase):
    """
    Неявная двухслойная схема решающая T_t +vT_x =αT_xx
    """
    def __init__(self, alpha, v = 0.0, name: str ="Неявная схема BTCS"):
        super().__init__(name)
        self.alpha = alpha
        self.v = v

    def solve(self, f_init, f_bound, x_domain, t_domain, nx: int, nt: int, source=None):
        """
        f_init(x): u(x, 0)
        f_bound(t): возвращает (u_left(t), u_right(t))
        x_domain = (x0, xL)
        t_domain = (t0, tEnd)
        """
        x0, xL = x_domain
        t0, tEnd = t_domain

        self.x = np.linspace(x0, xL, nx + 1)
        self.t = np.linspace(t0, tEnd, nt + 1)
        self.dx = (xL - x0) / nx
        self.dt = (tEnd - t0) / nt

        d = self.alpha * self.dt / self.dx ** 2

        self.u = np.zeros((nt + 1, nx + 1))
        self.u[0, :] = np.array([f_init(xi) for xi in self.x])

        tma = TridiagonalMatrixAlgorithm()

        for j in range(nt):
            t_next = self.t[j + 1]

            u_left, u_right = f_bound(t_next)
            self.u[j + 1, 0] = u_left
            self.u[j + 1, -1] = u_right

            n = nx - 1  # число внутренних узлов

            v_val = 0.0
            if self.v is not None:
                if callable(self.v):
                    v_val = self.v(self.x[1], t_next)
                else:
                    v_val = float(self.v)

            mu = v_val * self.dt / (2.0 * self.dx)

            a = -(d + mu) * np.ones(n - 1)  # поддиагональ
            b = (1.0 + 2.0 * d) * np.ones(n)  # главная
            c = -(d - mu) * np.ones(n - 1)  # наддиагональ

            A = np.diag(b) + np.diag(c, k=1) + np.diag(a, k=-1)
            rhs = self.u[j, 1:-1].copy()

            if source is not None:
                for i in range(1, nx):
                    rhs[i - 1] += self.dt * source(self.x[i], t_next)

            rhs[0] += (d + mu) * u_left
            rhs[-1] += (d - mu) * u_right

            u_inner = tma.solve(A, rhs)
            self.u[j + 1, 1:-1] = u_inner

        self.result = self.u
        return self.x, self.t, self.u



