import numpy as np
import sys
sys.path.append ("C:\\Users\\6anna\\PycharmProjects\\Labs\\Numerical_methods\\Numerical_methods_classes\\Partial_Differential_Equations(PDE)")

from PDEMethodBase import PDEMethodBase


class ConvectionUpwind1(PDEMethodBase):
    """
    Противопотоковый метод первого порядка (upwind) для уравнения переноса u_t + v u_x = 0.
    """

    def __init__(self, alpha=0.0, v=0.0, name="Upwind 1-го порядка"):
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
            print(f"WARNING: |C| = {abs(C):.3f} > 1, upwind-схема может быть неустойчива.")

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
                    for i in range(nx + 1):
                        i_prev = (i - 1) % (nx + 1)
                        u[n + 1, i] = u[n, i] - C * (u[n, i] - u[n, i_prev])
                else:
                    for i in range(nx + 1):
                        i_next = (i + 1) % (nx + 1)
                        u[n + 1, i] = u[n, i] - C * (u[n, i_next] - u[n, i])


                u[n + 1, 0] = u[n + 1, nx]


            else:
                u_left, u_right = f_bound(self.t[n])
                if u_left is not None:
                    u[n, 0] = u_left
                if u_right is not None:
                    u[n, nx] = u_right

                if self.v >= 0:
                    for i in range(1, nx + 1):
                        u[n + 1, i] = u[n, i] - C * (u[n, i] - u[n, i - 1])
                    u[n + 1, 0] = u_left
                else:
                    for i in range(0, nx):
                        u[n + 1, i] = u[n, i] - C * (u[n, i + 1] - u[n, i])
                    u[n + 1, nx] = u_right

                u_left_next, u_right_next = f_bound(self.t[n + 1])
                if u_left_next is not None:
                    u[n + 1, 0] = u_left_next
                if u_right_next is not None:
                    u[n + 1, nx] = u_right_next


        self.u = u
        return self.x, self.t, self.u
