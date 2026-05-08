import numpy as np
import sys
sys.path.append ("C:\\Users\\6anna\\PycharmProjects\\Labs\\Numerical_methods\\Numerical_methods_classes\\Partial_Differential_Equations(PDE)")

from PDEMethodBase import PDEMethodBase


class ConvectionLaxWendroff(PDEMethodBase):
    """
    Схема Лакса–Вендрофа для уравнения переноса: u_t + v u_x = 0
    """

    def __init__(self, v,  alpha=0.0, name="Лакс–Вендроф"):
        super().__init__(name)
        self.alpha = alpha
        self.v = float(v)

    def solve(self, f_init, f_bound, x_domain, t_domain, nx: int, nt: int):
        x0, xL = x_domain
        t0, tEnd = t_domain

        self.dx = (xL - x0) / nx
        self.dt = (tEnd - t0) / nt

        C = self.v * self.dt / self.dx  # число Куранта

        if abs(C) > 1.0:
            print(f"WARNING: |C| = {abs(C):.3f} > 1, схема Лакса–Вендрофа может быть неустойчива.")

        self.x = np.linspace(x0, xL, nx + 1)
        self.t = np.linspace(t0, tEnd, nt + 1)

        u = np.zeros((nt + 1, nx + 1))
        u[0, :] = f_init(self.x)
        #ghjdthrf на периодичность условий
        test_bound = f_bound(self.t[0])
        periodic_mode = (test_bound[0] is None and test_bound[1] is None)

        for n in range(nt):
            #u_left, u_right = f_bound(self.t[n])
            #u[n, 0] = u_left
            #u[n, nx] = u_right

            #u_ext = np.zeros(nx + 3)
            #u_ext[1:nx + 2] = u[n, :]
            #u_ext[0] = u[n, nx - 1]
            #u_ext[nx + 2] = u[n, 1]

            #for i in range(1, nx):
            #    du = u[n, i + 1] - u[n, i - 1]
            #    d2u = u[n, i + 1] - 2*u[n, i] + u[n, i - 1]

            #    u[n + 1, i] = (u[n, i] - 0.5 * C * du + 0.5 * C**2 * d2u)

            #u_left, u_right = f_bound(self.t[n + 1])
            #u[n + 1, 0] = u_left
            #u[n + 1, nx] = u_right
            #u[n + 1, 0] = u[n + 1, nx]

            if periodic_mode:

                # Обрабатываем все точки, включая граничные
                for i in range(nx + 1):
                    # Вычисляем индексы соседей с учетом периодичности
                    i_prev = (i - 1) % (nx + 1)
                    i_next = (i + 1) % (nx + 1)

                    du = u[n, i_next] - u[n, i_prev]
                    d2u = u[n, i_next] - 2 * u[n, i] + u[n, i_prev]
                    u[n + 1, i] = u[n, i] - 0.5 * C * du + 0.5 * C ** 2 * d2u

            else:
                u_left, u_right = f_bound(self.t[n])
                if u_left is not None:
                    u[n, 0] = u_left
                if u_right is not None:
                    u[n, nx] = u_right

                for i in range(1, nx):
                    du = u[n, i + 1] - u[n, i - 1]
                    d2u = u[n, i + 1] - 2 * u[n, i] + u[n, i - 1]
                    u[n + 1, i] = u[n, i] - 0.5 * C * du + 0.5 * C ** 2 * d2u

                u_left_next, u_right_next = f_bound(self.t[n + 1])
                if u_left_next is not None:
                    u[n + 1, 0] = u_left_next
                if u_right_next is not None:
                    u[n + 1, nx] = u_right_next

        self.u = u
        return self.x, self.t, self.u
