import numpy as np
import sys
sys.path.append ("C:\\Users\\6anna\\PycharmProjects\\Labs\\Numerical_methods\\Numerical_methods_classes\\Partial_Differential_Equations(PDE)")

from PDEMethodBase import PDEMethodBase


class ConvectionRichmyer(PDEMethodBase):
    """
    Схема Рихтмайера (двухшаговый метод Лакса–Вендрофа) для уравнения переноса u_t + v u_x = 0.
    """

    def __init__(self, alpha=0.0, v=0.0, name="Рихтмайер"):
        super().__init__(name)
        self.alpha = float(alpha)
        self.v = float(v)

    def solve(self, f_init, f_bound, x_domain, t_domain, nx: int, nt: int):
        x0, xL = x_domain
        t0, tEnd = t_domain

        self.dx = (xL - x0) / nx
        self.dt = (tEnd - t0) / nt

        C = self.v * self.dt / self.dx

        if abs(C) > 1.0:
            print(f"WARNING: |C| = {abs(C):.3f} > 1, схема Рихтмайера может быть неустойчива.")

        self.x = np.linspace(x0, xL, nx + 1)
        self.t = np.linspace(t0, tEnd, nt + 1)

        u = np.zeros((nt + 1, nx + 1))
        u[0, :] = f_init(self.x)

        #периодичность граничных условий
        test_bound = f_bound(self.t[0])
        periodic_mode = (test_bound[0] is None and test_bound[1] is None)

        # вспомогательный массив для полушага (i+1/2)
        u_half = np.zeros(nx)

        for n in range(nt):

            if periodic_mode:
                # Устанавливаем периодичность на текущем временном слое
                u[n, 0] = u[n, nx]
                # 1) полушаг
                for i in range(nx):
                    # периодические индексы
                    i_next = (i + 1) % (nx + 1)

                    ui = u[n, i]
                    ui1 = u[n, i_next]
                    u_half[i] = 0.5 * (ui1 + ui) - 0.5 * C * (ui1 - ui)

                # 2) полный шаг
                for i in range(nx + 1):
                    # Вычисляем индексы
                    i_half_left = (i - 1) % nx  # точка i-1/2
                    i_half_right = i % nx  # точка i+1/2

                    u[n + 1, i] = u[n, i] - C * (u_half[i_half_right] - u_half[i_half_left])

                u[n + 1, nx] = u[n + 1, 0]

            else:
                u_left, u_right = f_bound(self.t[n])
                if u_left is not None:
                    u[n, 0] = u_left
                if u_right is not None:
                    u[n, nx] = u_right

                # 1) полушаг: i+1/2
                for i in range(nx):
                    ui = u[n, i]
                    ui1 = u[n, i + 1]
                    u_half[i] = 0.5 * (ui1 + ui) - 0.5 * C * (ui1 - ui)

                # 2) полный шаг
                for i in range(1, nx):
                    u[n + 1, i] = u[n, i] - C * (u_half[i] - u_half[i - 1])

                u_left_next, u_right_next = f_bound(self.t[n + 1])
                if u_left_next is not None:
                    u[n + 1, 0] = u_left
                if u_right_next is not None:
                    u[n + 1, nx] = u_right

        self.u = u
        return self.x, self.t, self.u
