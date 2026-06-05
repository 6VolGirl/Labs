import numpy as np
import matplotlib.pyplot as plt

import sys
sys.path.append ("C:\\Users\\6anna\\PycharmProjects\\Labs\\Numerical_methods\\Numerical_methods_classes\\Partial_Differential_Equations(PDE)\\Heat_Equation")
from HeatFTCS import HeatFTCS
sys.path.append ("C:\\Users\\6anna\\PycharmProjects\\Labs\\Numerical_methods\\Numerical_methods_classes\\Partial_Differential_Equations(PDE)\\Convection_Equation")
from ConvectionLaxWendroff import ConvectionLaxWendroff
from ConvectionRichmyer import ConvectionRichmyer
from ConvectionMacCormack import ConvectionMacCormack
from ConvectionUpwind1 import ConvectionUpwind1
from ConvectionUpwind2 import ConvectionUpwind2




def phi_triangular_var2(x, L=1.0):
    x = np.asarray(x)
    u0 = np.zeros_like(x)

    mask1 = (x >= 0.0) & (x <= 0.2*L)
    u0[mask1] = x[mask1] / (0.2*L)

    mask2 = (x > 0.2*L) & (x <= L)
    u0[mask2] = (L - x[mask2]) / (L - 0.2*L)

    return u0 if u0.shape != () else float(u0)

def boundary_periodic(t):
    return None, None

def exact_sol(x, t, L=1.0, v=1.0):
    x0 = (x - v*t) % L
    return phi_triangular_var2(x0, L)



def run_and_plot_for_convection_d(method_classes, v, L, t_end, d_values, times_to_plot, nx=80):

    x0 = 0.0
    x_domain = (x0, L)

    alpha = 0.0

    for d in d_values:
        dx = L / nx
        dt = d * dx / abs(v)
        nt = int(t_end / dt)

        if nt > 0:
            dt = t_end / nt
        else:
            print(f"Пропускаем d={d}: слишком маленький dt, nt={nt}")
            continue


        x_exact = np.linspace(x0, L, nx + 1)

        plt.figure(figsize=(8, 5))

        for t_target in times_to_plot:
            if t_target > t_end:
                continue
            u_ex = exact_sol(x_exact, t_target, L, v)
            plt.plot(x_exact, u_ex, "k--", linewidth=1,
                     label=f"exact, t={t_target:g}")

        errors_for_plot = []
        names_for_plot = []

        for MethodClass in method_classes:
            method = MethodClass(alpha=alpha, v=v, name=MethodClass.__name__)
            x, t_grid, u_num = method.solve(f_init=lambda x: phi_triangular_var2(x, L), f_bound=boundary_periodic, x_domain=x_domain, t_domain=(0.0, t_end), nx=nx, nt=nt,)


            err_info = method.compute_error_slice( u_exact=lambda X, T, L_loc: exact_sol(X, T, L_loc, v), L=L, axis="y", index=None,)
            errors_for_plot.append(err_info["error_field"])
            names_for_plot.append(method.name)


            for t_target in times_to_plot:
                j = int(round(t_target / dt))
                if j > nt:
                    continue
                plt.plot(x, u_num[j, :],
                         label=f"{method.name}, t={t_grid[j]:.3f}")

        plt.title(f"Конвекция, сравнение методов (d = {d})")
        plt.xlabel("x")
        plt.ylabel("u(x, t)")
        plt.grid(True)
        plt.legend(loc="center left", bbox_to_anchor=(1.02, 0.5), fontsize=8)
        plt.tight_layout()
        plt.show()


        plt.figure(figsize=(8, 5))
        for method_name, err in zip(names_for_plot, errors_for_plot):
            for t_target in times_to_plot:
                j = int(round(t_target / dt))
                if j > nt:
                    continue
                plt.plot(x, err[j, :],
                         label=f"{method_name} error, t={t_grid[j]:.3f}")

        plt.title(f"Ошибки методов ( d = {d})")
        plt.xlabel("x")
        plt.ylabel("error(x, t)")
        plt.grid(True)
        plt.legend(loc="center left", bbox_to_anchor=(1.02, 0.5), fontsize=8)
        plt.tight_layout()
        plt.show()

#methods = [HeatFTCS, ConvectionLaxWendroff, ConvectionRichmyer, ConvectionMacCormack, ConvectionUpwind1, ConvectionUpwind2]
methods = [ConvectionUpwind1]
v = 1.0
L = 1.0
d_values = [0.1]
times_to_plot = [0.1, 0.2, 0.3]

run_and_plot_for_convection_d(method_classes=methods, v=v, L=L, t_end=0.3, d_values=d_values, times_to_plot=times_to_plot, nx=80)
