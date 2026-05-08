import numpy as np
import sys
sys.path.append ("C:\\Users\\6anna\\PycharmProjects\\Labs\\Numerical_methods\\Numerical_methods_classes\\Partial_Differential_Equations(PDE)")

from PDEMethodBase import PDEMethodBase


class Heat2DFTCS(PDEMethodBase):
    """
    2D уравнение теплопроводности: u_t = alpha (u_xx + u_yy)
    Явная двухслойная схема (FTCS).
    """

    def __init__(self, alpha, name: str = "2D явная схема FTCS"):
        super().__init__(name)
        self.alpha = float(alpha)

    def solve(self, f_init, f_bound, x_domain, y_domain, t_domain, nx: int, ny: int, nt: int):
        """
        f_init(x, y): начальное условие u(x, y, 0)
        f_bound(t, x, y): граничное условие u(x, y, t) на периметре
        x_domain = (x0, xL)
        y_domain = (y0, yL)
        t_domain = (t0, tEnd)
        """
        x0, xL = x_domain
        y0, yL = y_domain
        t0, tEnd = t_domain

        self.x = np.linspace(x0, xL, nx + 1)
        self.y = np.linspace(y0, yL, ny + 1)
        self.t = np.linspace(t0, tEnd, nt + 1)

        self.dx = (xL - x0) / nx
        self.dy = (yL - y0) / ny
        self.dt = (tEnd - t0) / nt

        dx2 = self.dx ** 2
        dy2 = self.dy ** 2

        d_x = self.alpha * self.dt / dx2
        d_y = self.alpha * self.dt / dy2

        if d_x + d_y > 0.25:
            print(f"WARNING: d_x + d_y = {d_x + d_y:.3f} > 0.5, "
                  f"явная схема может быть неустойчивой.")

        u = np.zeros((nt + 1, ny + 1, nx + 1))
        # начальное условие
        for j in range(ny + 1):
            for i in range(nx + 1):
                u[0, j, i] = f_init(self.x[i], self.y[j])

        # основной цикл по времени
        for n in range(nt):
            t_next = self.t[n + 1]
            u_next = u[n].copy()

            # внутренние узлы
            for j in range(1, ny):
                for i in range(1, nx):
                    uxx = u[n, j, i + 1] - 2.0 * u[n, j, i] + u[n, j, i - 1]
                    uyy = u[n, j + 1, i] - 2.0 * u[n, j, i] + u[n, j - 1, i]

                    u[n + 1, j, i] = (u[n, j, i] + d_x * uxx + d_y * uyy)

            for j in range(ny + 1):
                u[n + 1, j, 0] = f_bound(t_next, self.x[0], self.y[j])
                u[n + 1, j, nx] = f_bound(t_next, self.x[nx], self.y[j])
            for i in range(nx + 1):
                u[n + 1, 0, i] = f_bound(t_next, self.x[i], self.y[0])
                u[n + 1, ny, i] = f_bound(t_next, self.x[i], self.y[ny])


        self.u = u
        self.result = u
        return self.x, self.y, self.t, self.u


