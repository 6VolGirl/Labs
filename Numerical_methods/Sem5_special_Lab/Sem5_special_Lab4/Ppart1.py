import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append ("C:\\Users\\6anna\\PycharmProjects\\Numerical_methods\\Numerical_methods_classes\\Integral_Equations")
from Fredholm import Fredholm
sys.path.append ("C:\\Users\\6anna\\PycharmProjects\\Numerical_methods\\Numerical_methods_classes\\Numerical_Integration")
from Trapezoid import Trapezoid
from GaussQuardratute import GaussQuadrature


def exact_sol(t):
    return t**2 - 5/3

def f(t):
    return t** 2 + t / 6 - 7 / 3

def kernel(t, s):
    return t / s ** 2 - 1


a, b = 1, 2
lambda_param = -1

all_solutions = {}

trap = Trapezoid()

solver_trap_3 = Fredholm(lam=lambda_param, integration_method=trap)
t_trap_3, x_trap_3 = solver_trap_3.solve(kernel, f, a, b, n=3)
all_solutions['Трапеции (3)'] = (t_trap_3, x_trap_3, solver_trap_3)

solver_trap_10 = Fredholm(lam=lambda_param, integration_method=trap)
t_trap_10, x_trap_10 = solver_trap_10.solve(kernel, f, a, b, n=10)
all_solutions['Трапеции (10)'] = (t_trap_10, x_trap_10, solver_trap_10)

gauss = GaussQuadrature()

solver_gauss_3 = Fredholm(lam=lambda_param, integration_method=gauss)
t_gauss_3, x_gauss_3 = solver_gauss_3.solve(kernel, f, a, b, n=3)
all_solutions['Гаусс (3)'] = (t_gauss_3, x_gauss_3, solver_gauss_3)

solver_gauss_10 = Fredholm(lam=lambda_param, integration_method=gauss)
t_gauss_10, x_gauss_10 = solver_gauss_10.solve(kernel, f, a, b, n=10)
all_solutions['Гаусс (10)'] = (t_gauss_10, x_gauss_10, solver_gauss_10)



t_exact = np.linspace(a, b, 100)
x_exact = [exact_sol(t) for t in t_exact]



# ГРАФИК 1: Все методы на одном графике
fig1 = plt.figure(figsize=(15, 9))

plt.plot(t_exact, x_exact, 'k-', linewidth=2, alpha=0.6, label='Точное решение', zorder=1)
plt.plot(t_trap_3, x_trap_3, 'ro-', markersize=13, linewidth=2.5,
         label='Трапеции (3 узла)', zorder=4)
plt.plot(t_trap_10, x_trap_10, 'r^-', markersize=8, linewidth=1.5, alpha=0.8,
         label='Трапеции (10 узлов)', zorder=2)
plt.plot(t_gauss_3, x_gauss_3, 'bs-', markersize=13, linewidth=2.5,
         label='Гаусс (3 узла)', zorder=4)
plt.plot(t_gauss_10, x_gauss_10, 'bv-', markersize=8, linewidth=1.5, alpha=0.8,
         label='Гаусс (10 узлов)', zorder=2)


plt.xlabel('t', fontsize=14, fontweight='bold')
plt.ylabel('x(t)', fontsize=14, fontweight='bold')
plt.title('Решение интегрального уравнения Фредгольма\n'
           'Сравнение методов трапеций и Гаусса',
           fontsize=16, fontweight='bold')
plt.legend(fontsize=12, loc='best', framealpha=0.95)
plt.grid(True, alpha=0.3, linestyle=':')
plt.tight_layout()

plt.show()

control_points = {
    't₁': 1.0,
    't₂': 1.5,
    't₃': 2.0
}

print(f"name    t_val      exact          trap3           trap10           gauss3          gauss10")

for name, t_val in zip(control_points.keys(), control_points.values()):
    exact = exact_sol(t_val)

    idx_trap3 = np.argmin(np.abs(t_trap_3 - t_val))
    idx_trap10 = np.argmin(np.abs(t_trap_10 - t_val))
    idx_gauss3 = np.argmin(np.abs(t_gauss_3 - t_val))
    idx_gauss10 = np.argmin(np.abs(t_gauss_10 - t_val))

    trap3 = x_trap_3[idx_trap3]
    trap10 = x_trap_10[idx_trap10]
    gauss3 = x_gauss_3[idx_gauss3]
    gauss10 = x_gauss_10[idx_gauss10]

    print(f"{name}     {t_val:<8.4f} {exact:<15.10f} {trap3:<15.10f} {trap10:<15.10f} {gauss3:<15.10f} {gauss10:<15.10f}")

for name, t_val in zip(control_points.keys(), control_points.values()):
    exact = exact_sol(t_val)

    idx_trap3 = np.argmin(np.abs(t_trap_3 - t_val))
    idx_trap10 = np.argmin(np.abs(t_trap_10 - t_val))
    idx_gauss3 = np.argmin(np.abs(t_gauss_3 - t_val))
    idx_gauss10 = np.argmin(np.abs(t_gauss_10 - t_val))

    trap3 = x_trap_3[idx_trap3]
    trap10 = x_trap_10[idx_trap10]
    gauss3 = x_gauss_3[idx_gauss3]
    gauss10 = x_gauss_10[idx_gauss10]

    print(f"{name:<6} {t_val:<8.4f} {'—':<15} {abs(trap3 - exact):<15.2e} {abs(trap10 - exact):<15.2e} {abs(gauss3 - exact):<15.2e} {abs(gauss10 - exact):<15.2e}")
