import numpy as np
import sys
sys.path.append ("C:\\Users\\6anna\\PycharmProjects\\Labs\\Numerical_methods\\Numerical_methods_classes\\Partial_Differential_Equations(PDE)")
from PDEMethodBase import PDEMethodBase

class HeatFTCS(PDEMethodBase):
    """
    Явная двухслойная схема решающая T_t +vT_x =αT_xx
    """

    def __init__(self, alpha, v=0.0, name = "Явная схема"):
        super().__init__(name)
        self.alpha = float(alpha)
        self.v = float(v)

    def solve(self, f_init, f_bound, x_domain, t_domain, nx:int, nt:int):
        """
        f_init(x): u(x, 0)
        f_bound(t): возвращает (u_left(t), u_right(t))
        x_domain = (x0, xL)
        t_domain = (t0, tEnd)
        """
        x0, xl = x_domain
        t0, tEnd = t_domain

        self.dx = (xl - x0) / nx
        self.dt = (tEnd - t0) / nt

        d = self.alpha * self.dt / self.dx**2
        mu = self.v * self.dt / (2*self.dx) #конвекция

        # Число Куранта для конвекции
        C = abs(self.v) * self.dt / self.dx

        if d > 0.5:
            print(f"ВНИМАНИЕ: d = {d:.3f} > 0.5, "
                  f"диффузионная часть может быть неустойчивой.")

        if C > 1:
            print(f"ВНИМАНИЕ: Число Куранта C = {C:.3f} > 1, "
                  f"конвективная часть может быть неустойчивой.")

        self.x = np.linspace(x0, xl, nx+1)
        self.t = np.linspace(t0, tEnd, nt+1)

        test_bound = f_bound(self.t[0])
        periodic_mode = (test_bound[0] is None and test_bound[1] is None)

        u = np.zeros((nt+1, nx+1))
        u[0, :] = f_init(self.x)

        for n in range(nt):

            if periodic_mode:
                for i in range(0, nx + 1):
                    # Индексы соседних точек с учетом периодичности
                    i_prev = i - 1 if i > 0 else nx - 1
                    i_next = i + 1 if i < nx else 1

                    uxx = u[n, i_next] - 2 * u[n, i] + u[n, i_prev]
                    ux = u[n, i_next] - u[n, i_prev]
                    u[n + 1, i] = u[n, i] + d * uxx - mu * ux

                u[n + 1, nx] = u[n + 1, 0]

            else:
                for i in range(1, nx):
                    uxx = u[n, i + 1] - 2 * u[n, i] + u[n, i - 1]
                    ux = u[n, i + 1] - u[n, i - 1]
                    u[n + 1, i] = u[n, i] + d * uxx - mu * ux

                if f_bound is not None:
                    u_left, u_right = f_bound(self.t[n + 1])
                    u[n + 1, 0] = u_left
                    u[n + 1, nx] = u_right
                else:
                    u[n + 1, 0] = u[0, 0]
                    u[n + 1, nx] = u[0, nx]


        self.u = u
        return self.x, self.t, self.u
