import numpy as np

import sys
sys.path.append ("C:\\Users\\6anna\\PycharmProjects\\Labs\\Numerical_methods\\Numerical_methods_classes\\Partial_Differential_Equations(PDE)")
from PDEMethodBase import PDEMethodBase
sys.path.append ("C:\\Users\\6anna\\PycharmProjects\\Labs\\Numerical_methods\\Numerical_methods_classes\\\Linear_Systems\Direct_Methods")
from TridiagonalMatrixAlgorithm import TridiagonalMatrixAlgorithm


class HeatCrankNicolson(PDEMethodBase):
    def __init__(self, alpha, name: str = "Схема Кранка–Николсон"):
        super().__init__(name)
        self.alpha = float(alpha)

    def solve(self, f_init, f_bound, x_domain, t_domain,
              nx: int, nt: int, source=None):
        """
        f_init(x): u(x, 0)
        f_bound(t): (u_left(t), u_right(t))
        x_domain = (x0, xL)
        t_domain = (t0, tEnd)
        """
        x0, xL = x_domain
        t0, tEnd = t_domain

        self.x = np.linspace(x0, xL, nx + 1)
        self.t = np.linspace(t0, tEnd, nt + 1)
        self.dx = (xL - x0) / nx
        self.dt = (tEnd - t0) / nt

        d = self.alpha * self.dt / self.dx**2

        self.u = np.zeros((nt + 1, nx + 1))
        self.u[0, :] = np.array([f_init(xi) for xi in self.x])

        n = nx - 1
        # левая часть: (1 + d) u_i^{j+1} - (d/2)(u_{i-1}^{j+1} + u_{i+1}^{j+1})
        a = (1.0 + d) * np.ones(n)       # главная диагональ
        b = -0.5 * d * np.ones(n - 1)   # поддиагональ
        c = -0.5 * d * np.ones(n - 1)   # наддиагональ
        A = np.diag(a) + np.diag(b, -1) + np.diag(c, 1)

        tma = TridiagonalMatrixAlgorithm()

        for j in range(nt):
            t_next = self.t[j + 1]

            u_left, u_right = f_bound(t_next)
            self.u[j + 1, 0] = u_left
            self.u[j + 1, -1] = u_right

            # правая часть: (1 - d)u_i^j + (d/2)(u_{i-1}^j + u_{i+1}^j)
            rhs = np.zeros(n)
            for i in range(1, nx):
                rhs[i - 1] = ((1.0 - d) * self.u[j, i] + 0.5 * d * (self.u[j, i - 1] + self.u[j, i + 1]))

            # источник
            if source is not None:
                for i in range(1, nx):
                    x_i = self.x[i]
                    rhs[i - 1] += 0.5 * self.dt * (
                        source(x_i, self.t[j]) + source(x_i, t_next)
                    )

            rhs[0]   += 0.5 * d * (self.u[j, 0]   + u_left)
            rhs[-1]  += 0.5 * d * (self.u[j, -1]  + u_right)

            u_inner = tma.solve(A, rhs)
            self.u[j + 1, 1:-1] = u_inner

        self.result = self.u
        return self.get_solution()
