import numpy as np
import matplotlib.pyplot as plt


import sys
sys.path.append ("C:\\Users\\6anna\\PycharmProjects\\Labs\\Numerical_methods\\Numerical_methods_classes\\Linear_Systems\\Direct_Methods")
from TridiagonalMatrixAlgorithm import TridiagonalMatrixAlgorithm


def build_thermal_conductivity_tridiagonal_matrix(L: float = 1, N: int = 100 , B2: float = 1):
    """
    Строим матрицу A и вектор f для задачи:
         θ'' - B^2 θ = 0,  x ∈ [a, b]
        θ(0) = 1, θ'(L) = 0
    """
    h = L / N
    x = np.linspace(0, L, N + 1)
    A = np.zeros((N + 1, N + 1))
    f = np.zeros(N + 1)

    A[0, 0] = 1.0
    A[0, 1] = 0.0
    f[0] = 1.0

    for i in range(1, N):
        A[i, i - 1] = -1.0
        A[i, i] = 2.0 + (h**2) * B2
        A[i, i + 1] = -1.0
        f[i] = 0.0

        A[N, N - 1] = -2.0
        A[N, N] = 2.0 + (h**2) * B2
        f[N] = 0.0

    return A, f, x


a = 1
b = 15
L_real = 0.1
N = 100
u_a = 1
u_b = 0

L = 1
T_base = 420
T_inf = 290
hPkA1 = 22
hPkA2 = 70
B2_1 = hPkA1 * (L_real**2)
B2_2 = hPkA2 * (L_real**2)

tma = TridiagonalMatrixAlgorithm()
Delta_T = T_base - T_inf

A1, f1, x1 = build_thermal_conductivity_tridiagonal_matrix(L, N, B2_1)
theta1 = tma.solve(A1, f1)
T1 = T_inf + Delta_T * theta1

A2, f2, x2 = build_thermal_conductivity_tridiagonal_matrix(L, N, B2_2)
theta2 = tma.solve(A2, f2)
T2 = T_inf + Delta_T * theta2

u = np.zeros(N + 1)
u[0] = 420


x1_m = x1 * L_real
x2_m = x1 * L_real


fig, axes = plt.subplots(2, 1, figsize=(12, 10))

# График 1: Физические температуры (оба случая)
ax = axes[0]
ax.plot(x1_m * 1000, T1, "r-o", ms=3, label=f"hP/kA = {hPkA1} (B² = {B2_1})")
ax.plot(x2_m * 1000, T2, "b-s", ms=3, label=f"hP/kA = {hPkA2} (B² = {B2_2})")
ax.grid(True, alpha=0.3)
ax.set_xlabel("x, мм", fontsize=12)
ax.set_ylabel("Температура T(x), К", fontsize=12)
ax.set_title("Распределение физической температуры", fontsize=14, fontweight='bold')
ax.legend(fontsize=11)

# График 2: Безразмерная температура (оба случая)
ax = axes[1]
ax.plot(x1, theta1, "r-o", ms=3, label=f"hP/kA = {hPkA1}")
ax.plot(x2, theta2, "b-s", ms=3, label=f"hP/kA = {hPkA2}")
ax.grid(True, alpha=0.3)
ax.set_xlabel("ξ = x/L", fontsize=12)
ax.set_ylabel("θ(ξ)", fontsize=12)
ax.set_title("Безразмерная температура", fontsize=14, fontweight='bold')
ax.legend(fontsize=11)

plt.tight_layout()
plt.show()

tma = TridiagonalMatrixAlgorithm()

N_values = [3, 10, 100, 500]
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']


fig, ax = plt.subplots(figsize=(12, 7))

for idx, N in enumerate(N_values):
    A, f, x = build_thermal_conductivity_tridiagonal_matrix(L, N, B2_1)
    theta = tma.solve(A, f)
    T = T_inf + Delta_T * theta
    x_m = x * L_real

    ax.plot(x_m, T, "-o", linewidth=2.5, markersize=5,
            label=f"N = {N}, B = {B2_1:.6f}", color=colors[idx], alpha=0.8)

ax.grid(True, alpha=0.3)
ax.set_xlabel("x, м", fontsize=13, fontweight='bold')
ax.set_ylabel("T(x), К", fontsize=13, fontweight='bold')
ax.set_title(f"Распределение температуры для разных размеров сетки (αP/kS = {hPkA1})",
             fontsize=14, fontweight='bold')
ax.legend(fontsize=12, loc='best')
ax.set_xlim(0, L_real)

plt.tight_layout()
plt.show()
