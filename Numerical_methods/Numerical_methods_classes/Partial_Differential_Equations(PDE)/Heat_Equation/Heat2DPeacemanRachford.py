import numpy as np
import sys
sys.path.append ("C:\\Users\\6anna\\PycharmProjects\\Labs\\Numerical_methods\\Numerical_methods_classes\\Partial_Differential_Equations(PDE)")
from PDEMethodBase import PDEMethodBase
import sys
sys.path.append ("C:\\Users\\6anna\\PycharmProjects\\Labs\\Numerical_methods\\Numerical_methods_classes\\\Linear_Systems\Direct_Methods")
from TridiagonalMatrixAlgorithm import TridiagonalMatrixAlgorithm


class Heat2DPeacemanRachford(PDEMethodBase):
    """
    Метод продольно-поперечных прогонок (ADI, схема Писмена-Рекфорда)
    для 2D уравнения теплопроводности: u_t = alpha (u_xx + u_yy)
    """

    def __init__(self, alpha, name: str = "Метод Писмена-Рекфорда"):
        super().__init__(name)
        self.alpha = float(alpha)

    def solve(self, f_init, f_bound, x_domain, y_domain, t_domain,
              nx: int, ny: int, nt: int):

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

        r_x = self.alpha * self.dt / (2 * dx2)
        r_y = self.alpha * self.dt / (2 * dy2)

        u = np.zeros((nt + 1, ny + 1, nx + 1))

        # начальное условие
        for j in range(ny + 1):
            for i in range(nx + 1):
                u[0, j, i] = f_init(self.x[i], self.y[j])

        tma = TridiagonalMatrixAlgorithm()

        for n in range(nt):
            t_curr = self.t[n]
            t_half = t_curr + self.dt / 2
            t_next = self.t[n + 1]

            u_half = np.zeros((ny + 1, nx + 1))

            # границы на полушаге
            for j in range(ny + 1):
                for i in range(nx + 1):
                    if j == 0 or j == ny or i == 0 or i == nx:
                        u_half[j, i] = f_bound(t_half, self.x[i], self.y[j])

            # неявно по x:
            a_x = -r_x * np.ones(nx - 1)
            b_x = (1 + 2 * r_x) * np.ones(nx - 1)
            c_x = -r_x * np.ones(nx - 1)
            A_x = np.diag(b_x) + np.diag(a_x[:-1], -1) + np.diag(c_x[1:], 1)

            for j in range(1, ny):
                rhs = np.zeros(nx - 1)
                for i in range(1, nx):
                    rhs[i - 1] = u[n, j, i] + r_y * (u[n, j + 1, i] - 2 * u[n, j, i] + u[n, j - 1, i])

                rhs[0] += r_x * u_half[j, 0]
                rhs[-1] += r_x * u_half[j, nx]

                sol = tma.solve(A_x, rhs)
                u_half[j, 1:nx] = sol

            # границы на полном шаге
            u[n + 1, :, :] = u_half
            for j in range(ny + 1):
                for i in range(nx + 1):
                    if j == 0 or j == ny or i == 0 or i == nx:
                        u[n + 1, j, i] = f_bound(t_next, self.x[i], self.y[j])

            # неявно по y
            a_y = -r_y * np.ones(ny - 1)
            b_y = (1 + 2 * r_y) * np.ones(ny - 1)
            c_y = -r_y * np.ones(ny - 1)
            A_y = np.diag(b_y) + np.diag(a_y[:-1], -1) + np.diag(c_y[1:], 1)

            for i in range(1, nx):
                rhs = np.zeros(ny - 1)
                for j in range(1, ny):
                    rhs[j - 1] = u_half[j, i] + r_x * (
                        u_half[j, i + 1] - 2 * u_half[j, i] + u_half[j, i - 1]
                    )
                rhs[0] += r_y * u[n + 1, 0, i]
                rhs[-1] += r_y * u[n + 1, ny, i]

                sol = tma.solve(A_y, rhs)
                u[n + 1, 1:ny, i] = sol

        self.u = u
        self.result = u
        return self.x, self.y, self.t, self.u


