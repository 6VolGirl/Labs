import numpy as np
from PDEMethodBase import PDEMethodBase


class HeatDufortFrankel(PDEMethodBase):
    def __init__(self, alpha, name: str = "Метод Дюфорта–Франкела"):
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

        u = np.zeros((nt + 1, nx + 1))
        u[0, :] = np.array([f_init(xi) for xi in self.x])

        # Первый слой j=1 явной FTCS-схемой
        u[0, 0], u[0, -1] = f_bound(self.t[0])
        u[1, 0], u[1, -1] = f_bound(self.t[1])

        for i in range(1, nx):
            laplace0 = u[0, i+1] - 2*u[0, i] + u[0, i-1]
            u[1, i] = u[0, i] + d * laplace0

        # Основной трёхслойный цикл Дюфорта–Франкела
        for j in range(1, nt):
            u[j, 0], u[j, -1] = f_bound(self.t[j])
            u[j+1, 0], u[j+1, -1] = f_bound(self.t[j+1])

            for i in range(1, nx):
                num = (1.0 - 2.0*d) * u[j-1, i] + 2.0*d * (u[j, i+1] + u[j, i-1])
                den = 1.0 + 2.0*d
                u[j+1, i] = num / den

        self.u = u
        self.result = u
        return self.x, self.t, self.u
