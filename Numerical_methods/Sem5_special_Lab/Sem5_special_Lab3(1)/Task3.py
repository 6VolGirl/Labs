import numpy as np
import matplotlib.pyplot as plt

import sys
sys.path.append ("C:\\Users\\6anna\\PycharmProjects\\Labs\\Numerical_methods\\Numerical_methods_classes\\Partial_Differential_Equations(PDE)\\Heat_Equation")
from HeatFTCS import HeatFTCS
from HeatBTCS import HeatBTCS



def phi(x, L=1.0):
    return 100.0 * x / L

def boundary_T(t):
    return 0.0, 100.0

def run_and_plot_for_d(method_classes, alpha, u, L, t_end, d_values, times_to_plot, nx=50):

    x0 = 0.0
    x_domain = (x0, L)

    for d in d_values:
        dx = L / nx
        dt = d * dx**2 / alpha
        nt = int(t_end / dt)

        #x_exact = np.linspace(x0, L, nx + 1)

        plt.figure(figsize=(8, 5))

        for t_target in times_to_plot:
            if t_target > t_end:
                continue
            #u_ex = exact_sol(x_exact, t_target, L)   # твоя функция
            #plt.plot(x_exact, u_ex, "k--", linewidth=1,
            #         label=f"exact, t={t_target:g}")

        #errors_for_plot = []

        for MethodClass in method_classes:
            method = MethodClass(alpha=alpha, v=u)
            x, t_grid, u_num = method.solve( f_init=phi, f_bound=boundary_T, x_domain=x_domain, t_domain=(0.0, t_end), nx=nx, nt=nt)

            #err_info = method.compute_error_slice(exact_sol, L)
            #err = err_info["error_field"]
            #errors_for_plot.append((method.name, err))

            for t_target in times_to_plot:
                j = int(round(t_target / dt))
                if j > nt:
                    continue
                plt.plot(x, u_num[j, :],
                         label=f"{method.name}, t={t_grid[j]:.3f}, d={d}")

        plt.title(f"Конвекция–диффузия, сравнение методов при d = {d}")
        plt.xlabel("x")
        plt.ylabel("T(x, t)")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

        # графики ошибок
        #plt.figure(figsize=(8, 5))
        #for (name, err) in errors_for_plot:
        #    for t_target in times_to_plot:
        #        j = int(round(t_target / dt))
        #        if j > nt:
        #            continue
        #        plt.plot(x, err[j, :],
        #                 label=f"{name} error, t={t_grid[j]:.3f}, d={d}")
        #plt.title(f"Ошибки методов при d = {d}")
        #plt.xlabel("x")
        #plt.ylabel("error(x, t)")
        #plt.grid(True)
        #plt.legend()
        #plt.tight_layout()
        #plt.show()

def run_and_plot_for_mu(method_classes, alpha, v, L, t_end, mu_values, times_to_plot, nx=50):

    x0 = 0.0
    x_domain = (x0, L)

    for mu in mu_values:
        dx = L / nx
        dt = 2.0 * mu * dx / v
        nt = int(t_end / dt)

        plt.figure(figsize=(8, 5))

        for MethodClass in method_classes:
            method = MethodClass(alpha=alpha, v=v)
            x, t_grid, u_num = method.solve(
                f_init=phi,
                f_bound=boundary_T,
                x_domain=x_domain,
                t_domain=(0.0, t_end),
                nx=nx,
                nt=nt,
            )

            for t_target in times_to_plot:
                j = int(round(t_target / dt))
                if j > nt:
                    continue
                plt.plot(x, u_num[j, :],
                         label=f"{method.name}, t={t_grid[j]:.3f}, mu={mu:.2f}")

        plt.title(f"Конвекция–диффузия, сравнение методов при mu = {mu}")
        plt.xlabel("x")
        plt.ylabel("T(x, t)")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

def run_plot_vs_v(method_classes, alpha, v_values, L, t_target, mu, nx=80):
    x0 = 0.0
    x_domain = (x0, L)
    dx = L / nx
    x = np.linspace(x0, L, nx + 1)

    plt.figure(figsize=(8, 5))

    for v in v_values:
        dt = 2.0 * mu * dx / v
        nt = int(t_target / dt)
        dt = t_target / nt

        # сначала считаем эталонный метод (например, первый в списке)
        ref_class = method_classes[0]
        ref_method = ref_class(alpha=alpha, v=v, name=ref_class.__name__)
        _, t_grid, u_ref = ref_method.solve( f_init=phi, f_bound=boundary_T, x_domain=x_domain, t_domain=(0.0, t_target), nx=nx, nt=nt)
        u_ref_t = u_ref[nt, :]

        # рисуем и считаем отличия для всех методов
        for MethodClass in method_classes:
            method = MethodClass(alpha=alpha, v=v, name=MethodClass.__name__)
            _, _, u_num = method.solve( f_init=phi, f_bound=boundary_T, x_domain=x_domain, t_domain=(0.0, t_target), nx=nx, nt=nt)
            u_num_t = u_num[nt, :]

            diff = u_num_t - u_ref_t
            max_diff = np.max(np.abs(diff))
            l2_diff = np.sqrt(np.mean(diff**2))

            plt.plot(x, u_num_t,
                     label=f"{method.name}, v={v:.2f}, "
                           f"maxΔ={max_diff:.2e}, L2Δ={l2_diff:.2e}")

    plt.title(f"Конвекция–диффузия, t = {t_target}, mu = {mu} (без exact)")
    plt.xlabel("x")
    plt.ylabel("T(x, t)")
    plt.grid(True)
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.show()




methods = [HeatBTCS, HeatFTCS]
alpha = 1.0
v = 1.0
L = 1.0
d_values = [0.5]
mu_values = [0.01, 0.05, 0.6]
v_values = [0.5, 1.0, 2.0]
times_to_plot = [0.05, 0.1, 0.2, 0.5, 1]
mu = 0.25

#run_and_plot_for_d(methods, alpha, v, L, t_end = 1, d_values=d_values, times_to_plot=times_to_plot, nx=50)
#run_and_plot_for_mu(methods, alpha, v, L, t_end = 1, mu_values=mu_values, times_to_plot=times_to_plot, nx=50)
#run_plot_vs_v(methods, alpha, v_values, L, 1, mu, nx=80)


def boundary_T_func(t, x):
    """Граничное условие как функция от x"""
    if x == 0.0:
        return 0.0
    elif x == 1.0:
        return 100.0
    else:
        return None


d_values = [0.3]
times_to_plot = [0.25]

x0 = 0.0
x_domain = (x0, L)
nx = 80
dx = L / nx
d = d_values[0]
dt = d * dx**2 / alpha
nt = int(0.3 / dt)

# считаем отдельно
ftcs = HeatFTCS(alpha=alpha, v=v)
btcs = HeatBTCS(alpha=alpha, v=v)

x_f, t_f, u_ftcs = ftcs.solve(phi, boundary_T, x_domain, (0.0, 0.3), nx, nt)
x_b, t_b, u_btcs = btcs.solve(phi, boundary_T, x_domain, (0.0, 0.3), nx, nt)

j = int(round(0.2 / dt))
diff = np.max(np.abs(u_ftcs[j, :] - u_btcs[j, :]))
print("max |FTCS - BTCS| at t≈0.2 =", diff)
#max |FTCS - BTCS| at t≈0.2 = 0.001625193919714718


def compare_d_for_fixed_time(method_class, alpha, u, L, t_target, d_values, c, nx=80):
    x0 = 0.0
    x_domain = (x0, L)
    dx = L / nx
    x = np.linspace(x0, L, nx + 1)

    plt.figure(figsize=(10, 6))

    for d in d_values:
        # шаг по времени из d и c
        dt_d = d * dx**2 / alpha
        dt_c = c * dx / u
        dt = min(dt_d, dt_c)

        max_t = t_target
        nt = int(max_t / dt) + 1
        dt_actual = max_t / nt

        method = method_class(alpha=alpha, v=u, name=method_class.__name__)
        x_num, t_grid, u_num = method.solve(
            f_init=phi,
            f_bound=boundary_T,
            x_domain=x_domain,
            t_domain=(0.0, max_t),
            nx=nx,
            nt=nt
        )

        j = np.argmin(np.abs(t_grid - t_target))
        plt.plot(x_num, u_num[j, :],
                 label=f"d={alpha*dt_actual/dx**2:.3f}, t≈{t_grid[j]:.3f}")

    plt.plot(x, phi(x), 'k--', alpha=0.5, label="Начальное (t=0)")
    plt.title(f"{method_class.__name__}: влияние d при t≈{t_target}")
    plt.xlabel("x")
    plt.ylabel("T(x,t)")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()


compare_d_for_fixed_time(HeatBTCS, alpha=alpha, u=v, L=L, t_target=2.0, d_values=[0.1, 0.5, 2.0], c=0.5, nx=80)
