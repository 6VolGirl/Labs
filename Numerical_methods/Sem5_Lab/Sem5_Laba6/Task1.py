import numpy as np
#import matplotlib as plt
import matplotlib.pyplot as plt

import sys
sys.path.append(r"C:\Users\6anna\PycharmProjects\Labs\Numerical_methods\Numerical_methods_classes\Linear_Systems\Direct_Methods")
from TridiagonalMatrixAlgorithm import TridiagonalMatrixAlgorithm



import numpy as np
import matplotlib.pyplot as plt


def solve_explicit_all_times(tau, Nt, kappa):
    """
    Решает уравнение теплопроводности явной схемой и сохраняет решение
    ДЛЯ ВСЕХ шагов по времени.
    """

    y = np.sin(np.pi * x)
    y[0] = 0.0
    y[-1] = 0.0

    results = {}
    results[0.0] = y.copy()

    for s in range(Nt):
        y_new = y.copy()

        for i in range(1, n):
            lambda_y = (1.0 / h) * (kappa * (y[i + 1] - y[i]) / h - kappa * (y[i] - y[i - 1]) / h)
            phi_i = 0.0
            y_new[i] = y[i] + tau * (lambda_y + phi_i)

        y_new[0] = 0.0
        y_new[-1] = 0.0

        if np.max(np.abs(y_new)) > 1e10:
            print(f"Обнаружена неустойчивость на шаге s={s}, t={(s + 1) * tau:.6e}")
            print(f"   max|y| = {np.max(np.abs(y_new)):.4e}")
            break

        y = y_new
        t_curr = (s + 1) * tau
        results[t_curr] = y.copy()
        times = sorted(results.keys())

    return results, times

L = 1.0
t_max = 1.0
kappa = 1.0
n = 50
h = L / n
tau = 0.5 * h**2 * 0.9   # берем τ < h^2/2 для устойчивости
Nt = int(t_max / tau)

x = np.linspace(0, L, n+1)
y = np.sin(np.pi * x)
y[0] = 0.0
y[-1] = 0.0

def exact_sol(x, t):
    return np.exp(-np.pi**2 * t) * np.sin(np.pi * x)

results_stable, times_stable  = solve_explicit_all_times(tau, Nt, kappa)

times_to_plot = [0.0, tau*80]#[0.0, tau*100, tau*500, tau*1000, tau*3000, tau*Nt]


plt.figure(figsize=(12, 7))

colors = ['red', 'green', 'blue', 'purple', 'orange', 'brown']
errors_data = []

for idx, t_plot in enumerate(times_to_plot):
    t_nearest = min(times_stable, key=lambda t: abs(t - t_plot))

    y_num = results_stable[t_nearest]
    U_exact = exact_sol(x, t_nearest)

    err = np.abs(y_num - U_exact)
    max_err = err.max()
    l2_err = np.sqrt((err ** 2).mean())
    rel_err = max_err / (np.abs(U_exact).max() + 1e-10)

    errors_data.append({
        't': t_nearest,
        'max_err': max_err,
        'L2_err': l2_err,
        'rel_err': rel_err
    })

    # Рисуем на графике
    plt.plot(x, y_num, color=colors[idx], linewidth=2.5,
             label=f't={t_nearest:.4f} (max_err={max_err:.2e})', marker='o', markersize=3)


plt.xlabel('x', fontsize=12)
plt.ylabel('u(x,t)', fontsize=12)
plt.title('Распределение температуры в различные моменты времени', fontsize=13)
plt.legend(fontsize=10, loc='best')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()



