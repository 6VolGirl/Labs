import numpy as np
from PDEMethodBase import PDEMethodBase


class ConvectionUpwind2(PDEMethodBase):
    """
    Противопотоковый метод второго порядка (linear upwind) для уравнения переноса u_t + v u_x = 0.
    """

    def __init__(self, alpha=0.0, v=0.0, name="Upwind 2-го порядка"):
        super().__init__(name)
        self.alpha = float(alpha)
        self.v = float(v)

    def solve(self, f_init, f_bound, x_domain, t_domain, nx: int, nt: int):
        x0, xL = x_domain
        t0, tEnd = t_domain

        self.dx = (xL - x0) / nx
        self.dt = (tEnd - t0) / nt

        C = self.v * self.dt / self.dx
        print(f"C = {C}")

        if abs(C) > 1.0:
            print(f"WARNING: |C| = {abs(C):.3f} > 1, upwind-2 схема может быть неустойчива.")

        self.x = np.linspace(x0, xL, nx + 1)
        self.t = np.linspace(t0, tEnd, nt + 1)

        u = np.zeros((nt + 1, nx + 1))
        u[0, :] = f_init(self.x)

        test_bound = f_bound(self.t[0])
        periodic_mode = (test_bound[0] is None and test_bound[1] is None)

        for n in range(nt):

            if periodic_mode:
                u[n, 0] = u[n, nx]

                if self.v >= 0:
                    #используем u_i, u_{i-1}, u_{i-2}
                    for i in range(nx + 1):
                        i_prev1 = (i - 1) % (nx + 1)
                        i_prev2 = (i - 2) % (nx + 1)

                        # Вторая разностная производная назад
                        dudx = (3 * u[n, i] - 4 * u[n, i_prev1] + u[n, i_prev2]) / (2.0 * self.dx)
                        u[n + 1, i] = u[n, i] - self.v * self.dt * dudx

                else:
                    # используем u_i, u_{i+1}, u_{i+2}
                    for i in range(nx + 1):

                        i_next1 = (i + 1) % (nx + 1)
                        i_next2 = (i + 2) % (nx + 1)

                        # Вторая разностная производная вперёд
                        dudx = (-3 * u[n, i] + 4 * u[n, i_next1] - u[n, i_next2]) / (2.0 * self.dx)
                        u[n + 1, i] = u[n, i] - self.v * self.dt * dudx

                u[n + 1, 0] = u[n + 1, nx]


            else:
                u_left, u_right = f_bound(self.t[n])
                if u_left is not None:
                    u[n, 0] = u_left
                if u_right is not None:
                    u[n, nx] = u_right

                if self.v >= 0:
                    # используем u_i, u_{i-1}, u_{i-2} обеспечим значения на первых двух узлах
                    for i in range(nx + 1):
                        if i >= 2:
                            # вторая разностная производная назад
                            dudx = (3 * u[n, i] - 4 * u[n, i - 1] + u[n, i - 2]) / (2.0 * self.dx)
                        elif i == 1:
                            # первая разностная производная назад
                            dudx = (u[n, i] - u[n, i - 1]) / self.dx
                        else:
                            dudx = 0.0

                        u[n + 1, i] = u[n, i] - self.v * self.dt * dudx

                else:
                    # используем u_i, u_{i+1}, u_{i+2}
                    for i in range(nx + 1):
                        if i <= nx - 2:
                            # вторая разностная производная вперёд
                            dudx = (-3 * u[n, i] + 4 * u[n, i + 1] - u[n, i + 2]) / (2.0 * self.dx)
                        elif i == nx - 1:
                            # первая разностная производная вперёд
                            dudx = (u[n, i + 1] - u[n, i]) / self.dx
                        else:
                            dudx = 0.0

                        u[n + 1, i] = u[n, i] - self.v * self.dt * dudx

                u_left_next, u_right_next = f_bound(self.t[n + 1])
                if u_left_next is not None:
                    u[n + 1, 0] = u_left_next
                if u_right_next is not None:
                    u[n + 1, nx] = u_right_next


        self.u = u
        return self.x, self.t, self.u
