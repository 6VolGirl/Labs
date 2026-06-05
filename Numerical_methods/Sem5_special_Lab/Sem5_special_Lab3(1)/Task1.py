import numpy as np
import matplotlib.pyplot as plt

import sys
sys.path.append ("C:\\Users\\6anna\\PycharmProjects\\Labs\\Numerical_methods\\Numerical_methods_classes\\Partial_Differential_Equations(PDE)\\Heat_Equation")
from HeatFTCS import HeatFTCS
from HeatBTCS import HeatBTCS
from HeatCrankNicolson import HeatCrankNicolson
from HeatRichardson import HeatRichardson
from HeatDufortFrankel import HeatDufortFrankel



def phi(x):
    return np.sin(2 * np.pi * x)

def boundary_zero(t):
    return 0.0, 0.0

import numpy as np

def exact_sol(x, t, L):
    """
    Решение u_t = u_xx при
    u(x,0)=sin(2πx/L), u(0,t)=u(L,t)=0.
    """
    x = np.asarray(x, dtype=float)
    t = np.asarray(t, dtype=float)
    return np.sin(2 * np.pi * x / L) * np.exp(-4 * np.pi**2 * t / L**2)



def run_and_plot_for_d(method_classes, alpha, L, t_end, d_values, times_to_plot, nx=50):
    """
    method_classes: [HeatFTCS, HeatBTCS, ...]
    d_values: список диффузионных чисел d
    """
    x0 = 0.0
    x_domain = (x0, L)

    for d in d_values:
        dx = L / nx
        dt = d * dx**2 / alpha
        nt = int(t_end / dt)

        for t_target in times_to_plot:

            plt.figure(figsize=(8, 5))

            # точное решение
            x_exact = np.linspace(x0, L, nx + 1)
            u_ex = exact_sol(x_exact, t_target, L)
            plt.plot(x_exact, u_ex, 'k--', label=f"exact, t={t_target:g}")

            for method_class in method_classes:
                method = method_class(alpha)

                x, t_grid, u = method.solve( f_init=phi, f_bound=boundary_zero, x_domain=x_domain, t_domain=(0.0, t_end), nx=nx, nt=nt)

                j = int(round(t_target / dt))
                if j > nt:
                    continue

                plt.plot(x, u[j, :],
                         label=f"{method.name}, d={d}, t={t_grid[j]:.3f}")

            plt.title(f"Сравнение методов, d = {d}, t = {t_target:g}")
            plt.xlabel("x")
            plt.ylabel("u(x, t)")
            plt.legend()
            plt.grid(True)
            plt.tight_layout()
            plt.show()

def run_and_plot_for_d_multi(method_classes, alpha, L, t_end, d_values, times_to_plot, nx=50):

    x0 = 0.0
    x_domain = (x0, L)

    for d in d_values:
        dx = L / nx
        dt = d * dx**2 / alpha
        nt = int(t_end / dt)

        plt.figure(figsize=(8, 5))

        x_exact = np.linspace(x0, L, nx + 1)
        for t_target in times_to_plot:
            if t_target > t_end:
                continue
            u_ex = exact_sol(x_exact, t_target, L)
            plt.plot(x_exact, u_ex, 'k--', linewidth=1,
                     label=f"exact, t={t_target:g}" if method_classes[0] is method_classes[0] else None)

        errors_for_plot = []

        for method_class in method_classes:
            method = method_class(alpha)
            x, t, u = method.solve( f_init=phi, f_bound=boundary_zero, x_domain=x_domain, t_domain=(0.0, t_end), nx=nx, nt=nt)
            err_info = method.compute_error_slice(exact_sol, L)
            err = err_info["error_field"]
            errors_for_plot.append(err)

            for t_target in times_to_plot:
                j = int(round(t_target / dt))
                if j > nt:
                    continue
                plt.plot(x, u[j, :], label=f"{method.name}, t={t[j]:.3f}, d={d}")

        plt.title(f"Сравнение методов при d = {d}")
        plt.xlabel("x")
        plt.ylabel("u(x, t)")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

        plt.figure(figsize=(8, 5))

        for method_class, err in zip(method_classes, errors_for_plot):
            method = method_class(alpha)  # только ради имени
            for t_target in times_to_plot:
                j = int(round(t_target / dt))
                if j > nt:
                    continue
                plt.plot(x, err[j, :],
                         label=f"{method.name} error, t={t[j]:.3f}, d={d}")

        plt.title(f"Ошибки методов при d = {d}")
        plt.xlabel("x")
        plt.ylabel("error(x, t)")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()


def run_and_plot_for_d_multi1(method_classes, alpha, L, t_end, d_values, times_to_plot, nx=50):

    x0 = 0.0
    x_domain = (x0, L)

    for d in d_values:
        dx = L / nx
        dt = d * dx**2 / alpha
        nt = int(t_end / dt)

        plt.figure(figsize=(8, 5))

        x_exact = np.linspace(x0, L, nx + 1)
        for t_target in times_to_plot:
            if t_target > t_end:
                continue
            u_ex = exact_sol(x_exact, t_target, L)
            plt.plot(x_exact, u_ex, "k--", linewidth=1,
                     label=f"exact, t={t_target:g}")

        errors_for_plot = []
        names_for_plot = []


        for method_class in method_classes:
            method = method_class(alpha)
            x, t_grid, u = method.solve(
                f_init=phi,
                f_bound=boundary_zero,
                x_domain=x_domain,
                t_domain=(0.0, t_end),
                nx=nx,
                nt=nt,
            )

            err_info = method.compute_error_slice(exact_sol, L)
            errors_for_plot.append(err_info["error_field"])
            names_for_plot.append(method.name)

            for t_target in times_to_plot:
                j = int(round(t_target / dt))
                if j > nt:
                    continue
                plt.plot(x, u[j, :],
                         label=f"{method.name}, t={t_grid[j]:.3f}, d={d}")

        plt.title(f"Сравнение методов при d = {d}")
        plt.xlabel("x")
        plt.ylabel("u(x, t)")
        plt.grid(True)

        # легенда справа от графика
        plt.legend(loc="center left", bbox_to_anchor=(1.02, 0.5), fontsize=8)
        plt.tight_layout()
        plt.show()

        # ---------- ГРАФИК ОШИБОК ----------
        plt.figure(figsize=(8, 5))

        for method_name, err in zip(names_for_plot, errors_for_plot):
            for t_target in times_to_plot:
                j = int(round(t_target / dt))
                if j > nt:
                    continue
                plt.plot(x, err[j, :],
                         label=f"{method_name} error, t={t_grid[j]:.3f}, d={d}")

        plt.title(f"Ошибки методов при d = {d}")
        plt.xlabel("x")
        plt.ylabel("error(x, t)")
        plt.grid(True)
        plt.legend(loc="center left", bbox_to_anchor=(1.02, 0.5), fontsize=8)
        plt.tight_layout()
        plt.show()





alpha = 1.0
L = 1.0
t_end = 0.3

d_values = [0.6]
times_to_plot = [0.3, 1.0, 4.0]
#methods = [HeatFTCS, HeatBTCS, HeatCrankNicolson, HeatRichardson, HeatDufortFrankel]
methods = [HeatBTCS]


#run_and_plot_for_d(methods, alpha, L, t_end, d_values, times_to_plot)
#run_and_plot_for_d(HeatBTCS, alpha, L, t_end, d_values, times_to_plot)


run_and_plot_for_d_multi1(methods, alpha=1.0, L=1.0, t_end=5.0, d_values=d_values, times_to_plot=times_to_plot, nx=50)
