import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

import sys

sys.path.append(r"C:\Users\6anna\PycharmProjects\Labs\Numerical_methods\Numerical_methods_classes\Linear_Systems\Direct_Methods")
from TridiagonalMatrixAlgorithm import TridiagonalMatrixAlgorithm



def build_matrix_neumann(N, mu, h):
    """
    Строит матрицу для неявной схемы с граничными условиями Неймана.

    N : число узлов (всего N+1 узлов)
    mu : μ = α * k / h²
    h : шаг по пространству

    """

    n = N + 1
    A = np.zeros((n, n))

    coeff_left = 1.0 / (2.0 * h)

    A[0, 0] = 3.0 * coeff_left
    A[0, 1] = -4.0 * coeff_left
    A[0, 2] = 1.0 * coeff_left

    for i in range(1, N):
        A[i, i - 1] = -mu
        A[i, i] = 1.0 + 2.0 * mu
        A[i, i + 1] = -mu

    A[N, N - 2] = 1.0 * coeff_left
    A[N, N - 1] = -4.0 * coeff_left
    A[N, N] = 3.0 * coeff_left

    return A


def build_rhs(theta_old, N, h, beta, tau_s):
    """
    Строит правую часть системы.

    theta_old : решение на предыдущем слое θ^s
    N : число узлов
    h : шаг по пространству
    beta : параметр граничного условия
    tau_s : время τ^{s+1}
    """

    n = N + 1
    b = np.zeros(n)

    b[0] = - beta * tau_s * np.exp(-tau_s)

    for i in range(1, N):
        b[i] = theta_old[i]

    b[N] = 0.0

    return b

def solve_problem (alpha, beta, L, N, h, k, M):
    mu = alpha * k / (h ** 2)

    xi = np.linspace(0, L, N + 1)
    theta = np.zeros(N + 1)

    results = {}
    results[0.0] = theta.copy()

    tma = TridiagonalMatrixAlgorithm()

    for s in range(M):
        tau_s1 = (s + 1) * k
        A = build_matrix_neumann(N, mu, h)
        b = build_rhs(theta, N, h, beta, tau_s1)
        theta_new = tma.solve(A, b)

        if np.max(np.abs(theta_new)) > 1e6:
            print(f"Обнаружена неустойчивость на шаге s={s}, τ={tau_s1:.6e}")
            print(f"max|θ| = {np.max(np.abs(theta_new)):.4e}")
            break

        theta = theta_new
        results[tau_s1] = theta.copy()

        if (s + 1) % 100 == 0:
            print(f"Шаг {s + 1}/{M}, τ = {tau_s1:.4f}, max(θ) = {np.max(theta):.6f}")

    times = sorted(results.keys())

    return results, times, xi

alpha = 2.0
beta = 2.0
L = 1.0
t_max = 2.0
N = 50
h = L / N
k = 0.01
M = int(t_max / k)

results, times, xi = solve_problem(alpha, beta, L, N, h, k, M)
results1, times1, xi = solve_problem(alpha, beta-1, L, N, h, k, M)
results2, times2, xi = solve_problem(alpha, beta+1, L, N, h, k, M)


#===================================================================================
# График 1: Распределение температуры вдоль стержня в разные моменты времени
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
axes = axes.flatten()

# выберем 4 характерных момента времени
time_indices = np.linspace(0, len(times) - 1, 4, dtype=int)
selected_times = [times[i] for i in time_indices]

for idx, t_plot in enumerate(selected_times):
    ax = axes[idx]
    theta_sol = results[t_plot]

    ax.plot(xi, theta_sol, 'b-o', linewidth=2, markersize=3, markevery=3)
    ax.set_xlabel('x', fontsize=11)
    ax.set_ylabel('θ(x,t)', fontsize=11)
    ax.set_title(f't = {t_plot:.4f}', fontsize=12)
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# График 2: Зависимость температуры от времени в точке x = 0
fig, ax = plt.subplots(figsize=(8, 5))
theta_at_0 = [results[t][0] for t in times]
ax.plot(times, theta_at_0, 'r-o', linewidth=2, markersize=4, markevery=max(1, len(times)//30))
ax.set_xlabel('t', fontsize=11)
ax.set_ylabel('θ(0,t)', fontsize=11)
ax.set_title('Зависимость температуры от времени в точке x = 0', fontsize=12)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()


# График 3: Температура в фиксированных точках
fig, ax = plt.subplots(figsize=(10, 6))
xi_track = [0.25, 0.5, 0.75]
colors_track = ['red', 'green', 'blue']
for xi_val, color in zip(xi_track, colors_track):
    idx = int(xi_val / h)
    theta_at_xi = [results[t][idx] for t in times]
    ax.plot(times, theta_at_xi, color=color, linewidth=2.5,
            label=f'θ(ξ={xi_val:.2f},τ)', marker='o', markersize=4, markevery=max(1, len(times) // 20))

ax.set_xlabel('τ', fontsize=11)
ax.set_ylabel('θ', fontsize=11)
ax.set_title('Температура в фиксированных точках по времени', fontsize=12, fontweight='bold')
ax.grid(True, alpha=0.3)
ax.legend(fontsize=10)
plt.tight_layout()
plt.show()

fig, ax = plt.subplots(figsize=(10, 6))

xi_track = [0.25, 0.5, 0.75]
colors_track = ['red', 'green', 'blue']

for xi_val, color in zip(xi_track, colors_track):
    idx = int(xi_val / h)

    theta1 = [results1[t][idx] for t in times1]
    theta = [results[t][idx] for t in times]
    theta2 = [results2[t][idx] for t in times2]

    ax.plot(times, theta1, color=color, linestyle='--', linewidth=1.8,
            label=f'ξ={xi_val:.2f}, β={alpha-1}')
    ax.plot(times, theta, color=color, linestyle='-', linewidth=2.2,
            label=f'ξ={xi_val:.2f}, β={alpha}')
    ax.plot(times, theta2, color=color, linestyle=':',
            linewidth=2.0, label=f'ξ={xi_val:.2f}, β={alpha+1}')

ax.set_xlabel('τ', fontsize=11)
ax.set_ylabel('θ', fontsize=11)
ax.set_title('Температура в фиксированных точках по времени\nдля разных β', fontsize=12, fontweight='bold')
ax.grid(True, alpha=0.3)
ax.legend(fontsize=9, ncol=2)
plt.tight_layout()
plt.show()

