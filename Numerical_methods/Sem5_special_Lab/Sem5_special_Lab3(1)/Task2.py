import numpy as np
import matplotlib.pyplot as plt

import sys
sys.path.append ("C:\\Users\\6anna\\PycharmProjects\\Labs\\Numerical_methods\\Numerical_methods_classes\\Partial_Differential_Equations(PDE)\\Heat_Equation")
from Heat2DFTCS import Heat2DFTCS
from Heat2DPeacemanRachford import Heat2DPeacemanRachford


def f_init_2d(x, y):
    return np.sin(np.pi * x) * np.sin(np.pi * y)

def f_bound_2d(t, x, y):
    return 0.0


def exact_2d_solution(x, y, t, alpha=0.01):
    return np.exp(-2 * alpha * np.pi ** 2 * t) * np.sin(np.pi * x) * np.sin(np.pi * y)



def run_2d_plots(method_classes, alpha, L, t_end, d_values, times_to_plot, nx=40, ny=40):

    x0 = 0.0
    y0 = 0.0
    x_domain = (x0, L)
    y_domain = (y0, L)


    for d in d_values:
        dx = L / nx
        dy = L / ny
        dt = d * dx ** 2 / alpha
        nt = int(t_end / dt)

        x_grid = np.linspace(x0, L, nx + 1)
        y_grid = np.linspace(y0, L, ny + 1)
        t_grid_calc = np.linspace(0, t_end, nt + 1)

        # График 1: Срезы по середине по y для разных времён
        plt.figure(figsize=(12, 6))

        j_mid = ny // 2
        y_mid = y_grid[j_mid]

        for t_target in times_to_plot:
            if t_target > t_end:
                continue
            u_ex = exact_2d_solution(x_grid, y_mid, t_target, alpha)
            plt.plot(x_grid, u_ex, "k--", linewidth=2, alpha=0.7,
                     label=f"Exact, t={t_target:.3f}")

        for method_class in method_classes:
            method = method_class(alpha)
            x, y, t_array, u = method.solve( f_init=f_init_2d, f_bound=f_bound_2d, x_domain=x_domain, y_domain=y_domain, t_domain=(0.0, t_end), nx=nx, ny=ny, nt=nt)

            for t_target in times_to_plot:
                n = int(round(t_target / dt))
                if n > nt:
                    continue
                plt.plot(x, u[n, j_mid, :], 'o-', markersize=4, alpha=0.7,
                         label=f"{method.name}, t={t_array[n]:.3f}, d={d}")

        plt.title(f"2D решение: срез при y={y_mid:.2f}, d={d}")
        plt.xlabel("x")
        plt.ylabel(r"$u(x, y_{mid}, t)$")
        plt.grid(True, alpha=0.3)
        plt.legend(loc="best", fontsize=9)
        plt.tight_layout()
        plt.show()

        # График 2: Срезы по середине по x для разных времён
        plt.figure(figsize=(12, 6))

        i_mid = nx // 2
        x_mid = x_grid[i_mid]

        for t_target in times_to_plot:
            if t_target > t_end:
                continue
            u_ex = exact_2d_solution(x_mid, y_grid, t_target, alpha)
            plt.plot(y_grid, u_ex, "k--", linewidth=2, alpha=0.7,
                     label=f"Exact, t={t_target:.3f}")

        for method_class in method_classes:
            method = method_class(alpha)
            x, y, t_array, u = method.solve(f_init=f_init_2d, f_bound=f_bound_2d, x_domain=x_domain, y_domain=y_domain, t_domain=(0.0, t_end), nx=nx, ny=ny, nt=nt)

            for t_target in times_to_plot:
                n = int(round(t_target / dt))
                if n > nt:
                    continue
                plt.plot(y, u[n, :, i_mid], 'o-', markersize=4, alpha=0.7,
                         label=f"{method.name}, t={t_array[n]:.3f}, d={d}")

        plt.title(f"2D решение: срез при x={x_mid:.2f}, d={d}")
        plt.xlabel("y")
        plt.ylabel(r"$u(x_{mid}, y, t)$")
        plt.grid(True, alpha=0.3)
        plt.legend(loc="best", fontsize=9)
        plt.tight_layout()
        plt.show()


        # График 3: Графики ошибки вдоль x для фиксированного y
        for method_class in method_classes:
            method = method_class(alpha)
            x, y, t_array, u = method.solve(f_init=f_init_2d, f_bound=f_bound_2d, x_domain=x_domain, y_domain=y_domain, t_domain=(0.0, t_end), nx=nx, ny=ny, nt=nt)

            fig, axes = plt.subplots(1, len(times_to_plot), figsize=(14, 4))
            if len(times_to_plot) == 1:
                axes = [axes]

            for idx, t_target in enumerate(times_to_plot):
                n = int(round(t_target / dt))
                if n > nt:
                    continue

                u_exact = exact_2d_solution(x, y_mid, t_target, alpha)
                u_numerical = u[n, j_mid, :]
                error = np.abs(u_numerical - u_exact)

                axes[idx].semilogy(x, error, 'b-o', markersize=5)
                axes[idx].set_title(f"t={t_target:.3f}, max_err={np.max(error):.2e}")
                axes[idx].set_xlabel("x")
                axes[idx].set_ylabel("$|u_{num} - u_{exact}|$")
                axes[idx].grid(True, alpha=0.3, which='both')

            fig.suptitle(f"{method.name}: Ошибка по x (срез y={y_mid:.2f}), d={d}")
            plt.tight_layout()
            plt.show()


        for method_class in method_classes:
            method = method_class(alpha)
            x, y, t_array, u = method.solve( f_init=f_init_2d, f_bound=f_bound_2d, x_domain=x_domain, y_domain=y_domain, t_domain=(0.0, t_end), nx=nx, ny=ny, nt=nt)

            fig, axes = plt.subplots(1, len(times_to_plot), figsize=(14, 4))
            if len(times_to_plot) == 1:
                axes = [axes]

            for idx, t_target in enumerate(times_to_plot):
                n = int(round(t_target / dt))
                if n > nt:
                    continue

                u_exact = exact_2d_solution(x_mid, y, t_target, alpha)
                u_numerical = u[n, :, i_mid]
                error = np.abs(u_numerical - u_exact)

                axes[idx].semilogy(y, error, 'r-o', markersize=5)
                axes[idx].set_title(f"t={t_target:.3f}, max_err={np.max(error):.2e}")
                axes[idx].set_xlabel("y")
                axes[idx].set_ylabel("$|u_{num} - u_{exact}|$")
                axes[idx].grid(True, alpha=0.3, which='both')

            fig.suptitle(f"{method.name}: Ошибка по y (срез x={x_mid:.2f}), d={d}")
            plt.tight_layout()
            plt.show()

        X, Y = np.meshgrid(x_grid, y_grid)

        fig = plt.figure(figsize=(15, 4))

        for idx, t_target in enumerate(times_to_plot[:3]):  # Максимум 3 графика
            if t_target > t_end:
                continue

            ax = fig.add_subplot(1, 3, idx + 1, projection='3d')
            Z_exact = exact_2d_solution(X, Y, t_target, alpha)

            surf = ax.plot_surface(X, Y, Z_exact, cmap='viridis', alpha=0.8)
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_zlabel('u(x,y,t)')
            ax.set_title(f"Exact solution, t={t_target:.3f}")
            fig.colorbar(surf, ax=ax, shrink=0.5)

        plt.suptitle(f"3D точное решение, d={d}")
        plt.tight_layout()
        plt.show()

        for method_class in method_classes:
            method = method_class(alpha)
            x, y, t_array, u = method.solve(f_init=f_init_2d, f_bound=f_bound_2d, x_domain=x_domain, y_domain=y_domain, t_domain=(0.0, t_end), nx=nx, ny=ny, nt=nt)

            fig = plt.figure(figsize=(15, 4))
            X, Y = np.meshgrid(x, y)

            for idx, t_target in enumerate(times_to_plot[:3]):
                n = int(round(t_target / dt))
                if n > nt:
                    continue

                ax = fig.add_subplot(1, 3, idx + 1, projection='3d')
                Z_num = u[n, :, :]

                surf = ax.plot_surface(X, Y, Z_num, cmap='viridis', alpha=0.8)
                ax.set_xlabel('x')
                ax.set_ylabel('y')
                ax.set_zlabel('u(x,y,t)')
                ax.set_title(f"{method.name}, t={t_array[n]:.3f}")
                fig.colorbar(surf, ax=ax, shrink=0.5)

            plt.suptitle(f"{method.name}: Численное решение, d={d}")
            plt.tight_layout()
            plt.show()


# def run_2d_plots(method_classes, alpha, L, t_end, d_values, times_to_plot, nx=40, ny=40):
#
#     x0 = 0.0
#     y0 = 0.0
#     x_domain = (x0, L)
#     y_domain = (y0, L)
#
#     for d in d_values:
#         dx = L / nx
#         dy = L / ny
#         dt = d * dx**2 / alpha
#         nt = int(t_end / dt)
#
#         x_grid = np.linspace(x0, L, nx + 1)
#         y_grid = np.linspace(y0, L, ny + 1)
#         t_grid_calc = np.linspace(0, t_end, nt + 1)
#
#         x_exact = np.linspace(x0, L, nx + 1)
#
#         plt.figure(figsize=(8, 5))
#
#         for t_target in times_to_plot:
#             if t_target > t_end:
#                 continue
#             u_ex = exact_sol(x_exact, t_target)
#             plt.plot(x_exact, u_ex, "k--", linewidth=1,
#                      label=f"exact 1D, t={t_target:g}")
#
#         for method_class in method_classes:
#             method = method_class(alpha)
#             x, y, t_grid, u = method.solve(f_init=f_init_2d, f_bound=f_bound_2d, x_domain=x_domain, y_domain=y_domain, t_domain=(0.0, t_end), nx=nx, ny=ny, nt=nt)
#             err_info = method.compute_error_slice(exact_1d_var2, L)
#             err = err_info["error_field"]
#
#             j_mid = ny // 2  # срез по середине по y
#             y_mid = y_grid[j_mid]
#
#             for t_target in times_to_plot:
#                 n = int(round(t_target / dt))
#                 if n > nt:
#                     continue
#                 plt.plot(x, u[n, j_mid, :],
#                          label=f"{method.name}, t={t_grid[n]:.3f}, d={d}")
#                 n = int(round(t_target / dt))
#                 if n > nt:
#                     continue
#                 plt.plot(x, u[n, j_mid, :],
#                          label=f"{method.name}, t={t_grid[n]:.3f}, d={d}")
#
#         plt.title(f"2D, срез y={y[j_mid]:.2f}, d={d}")
#         plt.xlabel("x")
#         plt.ylabel("u(x, y_mid, t)")
#         plt.grid(True)
#         plt.legend(loc="center left", bbox_to_anchor=(1.02, 0.5), fontsize=8)
#         plt.tight_layout()
#         plt.show()
#
#         # --- графики ошибки по x для каждого t_target ---
#         for t_target in times_to_plot:
#             n = int(round(t_target / dt))
#             if n > nt:
#                 continue
#
#             plt.figure(figsize=(8, 5))
#             plt.plot(x, err[n, :],
#                      label=f"error, t={t_grid[n]:.3f}, d={d}")
#             plt.title(f"Ошибка {method.name} при d={d}, t={t_grid[n]:.3f}")
#             plt.xlabel("x")
#             plt.ylabel("error(x, t)")
#             plt.grid(True)
#             plt.legend()
#             plt.tight_layout()
#             plt.show()


methods_2d = [Heat2DPeacemanRachford]
d_values = [0.1]
times_to_plot = [0.1, 0.125, 0.15]

run_2d_plots(methods_2d, alpha=1.0, L=1.0, t_end=0.2, d_values=d_values, times_to_plot=times_to_plot, nx=50, ny=50)