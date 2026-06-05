import numpy as np
from PDEMethodBase import PDEMethodBase
from PeriodicTridiagonalAlgorithm import PeriodicTridiagonalAlgorithm

class SmoluchowskiBTCS(PDEMethodBase):
    """
    Неявная схема для уравнения Смолуховского
    ρ_t = ρ_xx + (U'(x) ρ)_x   на [0, L] с периодическими ГУ
    """

    def __init__(self, potential, D=1.0, beta=1.0,  F=0.0, L=1.0, name="Smoluchowski BTCS"):
        super().__init__(name)
        self.potential = potential  # объект с методами U(x) и U'(x)
        self.D = D  # диффузия
        self.beta = beta  # обратная температура (1/kT)
        self.F = F
        self.L = L

    def solve(self, rho_init, x_domain, t_domain, nx: int, nt: int):
        x0, xL = x_domain
        t0, tEnd = t_domain

        self.x = np.linspace(x0, xL, nx, endpoint=False)
        self.dx = (xL - x0) / nx
        self.t = np.linspace(t0, tEnd, nt + 1)
        self.dt = (tEnd - t0) / nt

        if self.dt > self.dx ** 2 / (2 * self.D):
            print(f"Предупреждение: dt={self.dt} может быть слишком большим для устойчивости")
            print(f"Рекомендуется dt < {self.dx ** 2 / (2 * self.D):.6f}")

        rho = np.zeros((nt + 1, nx))
        rho[0, :] = rho_init(self.x)

        Uprime = self.potential.derivative(self.x) - self.F

        alpha = self.dt / self.dx**2
        gamma = self.beta * self.D * self.dt / (2 * self.dx)

        period_tma = PeriodicTridiagonalAlgorithm()

        for n in range(nt):
            f = rho[n, :].copy()

            a = np.zeros(nx)   # при ρ_{i-1}^{n+1}
            b = np.zeros(nx)   # при ρ_i^{n+1}
            c = np.zeros(nx)   # при ρ_{i+1}^{n+1}

            for i in range(nx):
                # Индексы соседних точек с учетом периодичности
                im1 = (i - 1) % nx
                ip1 = (i + 1) % nx

                a[i] = -alpha - gamma * Uprime[im1]
                b[i] = 1.0 + 2.0 * alpha
                c[i] = -alpha + gamma * Uprime[ip1]

            rho[n + 1, :] = period_tma.solve(a, b, c, f)

            mass = np.sum(rho[n + 1, :]) * self.dx
            if mass != 0.0:
                rho[n + 1, :] /= mass

        self.u = rho
        return self.x, self.t, self.u


    def boltzmann_distribution(self):
        """
        Болцмановское равновесное распределение:
        rho_eq(x) = Z^{-1} * exp(-beta * U(x)),
        нормированное так, чтобы сумма rho_eq * dx = 1.
        """
        Ux = self.potential(self.x)
        rho_eq = np.exp(-self.beta * Ux)
        Z = np.sum(rho_eq) * self.dx
        if Z != 0.0:
            rho_eq /= Z
        return rho_eq
