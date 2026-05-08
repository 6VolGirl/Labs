import numpy as np
import sys
sys.path.append ("C:\\Users\\6anna\\PycharmProjects\\Labs\\Numerical_methods\\Numerical_methods_classes\\Partial_Differential_Equations(PDE)")
from PDEMethodBase import PDEMethodBase
sys.path.append ("C:\\Users\\6anna\\PycharmProjects\\Labs\\Numerical_methods\\Numerical_methods_classes\\\Linear_Systems\Direct_Methods")
from TridiagonalMatrixAlgorithm import TridiagonalMatrixAlgorithm


class HeatRichardson(PDEMethodBase):
    def __init__(self, alpha, name: str = "Метод Ричардсона (перешагивания)"):
        super().__init__(name)
        self.alpha = float(alpha)

    def solve(self, f_init, f_bound, x_domain, t_domain,
              nx: int, nt: int, source=None):
        x0, xL = x_domain
        t0, tEnd = t_domain

        self.x = np.linspace(x0, xL, nx + 1)
        self.t = np.linspace(t0, tEnd, nt + 1)
        self.dx = (xL - x0) / nx
        self.dt = (tEnd - t0) / nt

        d = self.alpha * self.dt / self.dx**2

        u = np.zeros((nt + 1, nx + 1))
        u[0, :] = np.array([f_init(xi) for xi in self.x])

        # слой j=1 можно получить шагом FTCS (как стартовый)
        for i in range(1, nx):
            u[0, 0], u[0, -1] = f_bound(self.t[0])
            u[1, 0], u[1, -1] = f_bound(self.t[1])
            u[1, i] = (u[0, i] + d * (u[0, i+1] - 2*u[0, i] + u[0, i-1]))

        # трёхслойная схема Ричардсона
        for j in range(1, nt):
            u[j, 0], u[j, -1] = f_bound(self.t[j])

            for i in range(1, nx):
                laplace = u[j, i+1] - 2*u[j, i] + u[j, i-1]
                u[j+1, i] = u[j-1, i] + 2*d * laplace

        self.u = u
        self.result = u
        return self.x, self.t, self.u


