import numpy as np
import matplotlib.pyplot as plt

import sys
sys.path.append(r"C:\Users\6anna\PycharmProjects\Labs\Numerical_methods\Numerical_methods_classes\Linear_Systems\Direct_Methods")
from TridiagonalMatrixAlgorithm import TridiagonalMatrixAlgorithm


def wave_solver_weights(n, tau, h, c, smax, x0, delta, v0, sigma):
    """
    Решение волнового уравнения схемой с весами.
    """

    x = np.arange(0, l + h/2, h)
    t = np.arange(0, smax * tau + tau/2, tau)
    m = len(x)

    y = np.zeros((smax + 1, m))

    y[0, :] = 0.0

    # y^1_i = tau * psi_i
    psi = np.zeros_like(x)
    mask = (x >= x0 - delta) & (x <= x0 + delta)
    psi[mask] = v0
    y[1, :] = y[0, :] + tau * psi
    y[1, 0] = 0.0
    y[1, -1] = 0.0

    # коэффициенты для матрицы A = E - sigma c^2 tau^2 Λ
    lam2 = (c * tau / h) ** 2
    a = -sigma * lam2
    b = 1 + 2 * sigma * lam2

    # трёхдиагональные коэффициенты A для внутренних узлов i=1..m-2
    A = np.zeros((m - 2, m - 2))
    np.fill_diagonal(A, b)
    np.fill_diagonal(A[:-1, 1:], a)
    np.fill_diagonal(A[1:, :-1], a)

    for s in range(1, smax):
        # RHS = 2 y^s - y^{s-1} + c^2 tau^2 Λ((1-2σ) y^s + σ y^{s-1})
        ys   = y[s, :]
        ys_1 = y[s-1, :]
        combo = (1 - 2*sigma) * ys + sigma * ys_1
        Lap_combo = (combo[2:] - 2*combo[1:-1] + combo[:-2]) / h**2
        RHS_inner = 2*ys[1:-1] - ys_1[1:-1] + (c**2 * tau**2) * Lap_combo

        tma = TridiagonalMatrixAlgorithm()
        y_inner = tma.solve(A, RHS_inner)

        y[s+1, 0]   = 0.0
        y[s+1, -1]  = 0.0
        y[s+1, 1:-1] = y_inner

    return x, t[:smax+1], y
def wave_solver_explicit_weights(n, tau, h, c, smax, x0, delta, v0):
    """
    Явная схема (σ = 0) для волнового уравнения:
    y^{s+1}_i = λ^2 (y^s_{i+1} - 2 y^s_i + y^s_{i-1}) + 2 y^s_i - y^{s-1}_i
    с начальными условиями φ=0, ψ кусочная.
    """
    l = n * h
    x = np.linspace(0, l, n + 1)
    t = np.arange(0, smax * tau + tau/2, tau)
    m = len(x)

    y = np.zeros((smax + 1, m))

    # начальные условия
    psi = np.zeros_like(x)
    mask = (x >= x0 - delta) & (x <= x0 + delta)
    psi[mask] = v0

    y[0, :] = 0.0
    y[1, :] = y[0, :] + tau * psi
    y[1, 0] = 0.0
    y[1, -1] = 0.0

    lam = c * tau / h
    lam2 = lam**2

    for s in range(1, smax):
        for i in range(1, m - 1):
            y[s+1, i] = (lam2 * (y[s, i+1] - 2*y[s, i] + y[s, i-1])
                         + 2*y[s, i] - y[s-1, i])
        y[s+1, 0]  = 0.0
        y[s+1, -1] = 0.0

    return x, t[:smax+1], y

def exact_solution_series(x, t, num_terms=200):
    """
    Точное решение через ряд синусов.
    u(x,t) = sum_{n=1}^infty B_n * sin(pi*n*x/l) * sin(pi*n*c*t/l)
    где B_n = (4*v0)/(c*pi^2*n^2) * sin(pi*n*x0/l) * sin(pi*n*delta/l)
    """
    u = np.zeros_like(x)
    for n in range(1, num_terms + 1):
        psi_x0 = np.sin(np.pi * n * x0 / l)
        psi_delta = np.sin(np.pi * n * delta / l)
        B_n = (4.0 * v0 / (c * np.pi ** 2 * n ** 2)) * psi_x0 * psi_delta

        u += B_n * np.sin(np.pi * n * x / l) * np.sin(np.pi * n * c * t / l)
    return u


c = 1
l = 1.0
x0 = 0.5
delta = 0.1
v0 = 1.0
n = 200
h = l / n

lam = 0.1
tau = lam * h / c

tmax = 2.0
smax = int(tmax / tau)

sigma = 0.25
x_w, t_w, y_weight = wave_solver_weights(n, tau, h, c, smax, x0, delta, v0, sigma)
x_e, t_e, y_weight_e = wave_solver_explicit_weights(n, tau, h, c, smax, x0, delta, v0)


y_exact_w = np.zeros_like(y_weight)
for s in range(len(t_w)):
    y_exact_w[s, :] = exact_solution_series(x_w, t_w[s], num_terms=200)
error_w = np.abs(y_weight - y_exact_w)


y_exact_e = np.zeros_like(y_weight_e)
for s in range(len(t_e)):
    y_exact_e[s, :] = exact_solution_series(x_e, t_e[s], num_terms=200)
error_e = np.abs(y_weight_e - y_exact_e)

t_plot = 2.0
idx = min(int(t_plot / tau), len(t_e) - 1)

plt.figure(figsize=(10, 6))

# 1) верхний график: точное и численное
plt.subplot(2, 1, 1)
plt.plot(x_e, y_exact_w[idx, :], '--', label=f'точное, t={t_w[idx]:.2f}')
plt.plot(x_e, y_weight_e[idx, :], '-',  label=f'веса,   t={t_w[idx]:.2f}')
plt.xlabel('x')
plt.ylabel('u(x,t)')
plt.title('Точное vs схема с весами')
plt.grid(True)
plt.legend()

# 2) нижний график: погрешность
plt.subplot(2, 1, 2)
error_t = np.abs(y_weight[idx, :] - y_exact_w[idx, :])
plt.plot(x_w, error_t, 'r', label='|числ - точн|')
plt.xlabel('x')
plt.ylabel('погрешность')
plt.title(f'Погрешность при t={t_w[idx]:.2f}')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 6))

# 1) верхний график: точное и численное
plt.subplot(2, 1, 1)
plt.plot(x_e, y_exact_e[idx, :], '--', label=f'точное, t={t_e[idx]:.2f}')
plt.plot(x_e, y_weight_e[idx, :], '-',  label=f'веса,   t={t_e[idx]:.2f}')
plt.xlabel('x')
plt.ylabel('u(x,t)')
plt.title('Точное vs схема с весами явная')
plt.grid(True)
plt.legend()

# 2) нижний график: погрешность
plt.subplot(2, 1, 2)
error_t = np.abs(y_weight_e[idx, :] - y_exact_e[idx, :])
plt.plot(x_e, error_t, 'r', label='|числ - точн|')
plt.xlabel('x')
plt.ylabel('погрешность')
plt.title(f'Погрешность при t={t_e[idx]:.2f}')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()

# выберем общий момент времени
idx = min(len(t_w), len(t_e)) - 1
t_plot = t_w[idx]

sigma_imp = 0.4    # для неявной
sigma_exp = 0.0    # для явной (σ=0)

plt.figure(figsize=(10, 6))

# 1) Верхний график: решения
plt.subplot(2, 1, 1)
plt.plot(x_w, y_exact_w[idx, :], 'k--', label=f'точное, t={t_plot:.2f}')
plt.plot(x_w, y_weight[idx, :], 'b-',  label=f'неявная, σ={sigma_imp}')
plt.plot(x_e, y_weight_e[idx, :], 'r-.', label=f'явная, σ={sigma_exp}')
plt.xlabel('x')
plt.ylabel('u(x,t)')
plt.title('Сравнение явной и неявной схем с точным решением')
plt.grid(True)
plt.legend()

# 2) Нижний график: погрешности
plt.subplot(2, 1, 2)
err_imp = np.abs(y_weight[idx, :]   - y_exact_w[idx, :])
err_exp = np.abs(y_weight_e[idx, :] - y_exact_e[idx, :])
plt.plot(x_w, err_imp, 'b-',  label=f'|неявная - точн|, σ={sigma_imp}')
plt.plot(x_e, err_exp, 'r-.', label=f'|явная - точн|, σ={sigma_exp}')
plt.xlabel('x')
plt.ylabel('погрешность')
plt.title(f'Погрешности при t={t_plot:.2f}')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()


def max_norm(y):
    return np.max(np.abs(y))

lams = [0.1, 0.5, 1.0, 1.9]
T_end = 10.0
results = []

#for lam in lams:
#    tau = lam * h / c
#    smax = int(T_end / tau)
#    x_w, t_w, y_w = wave_solver_weights(n, tau, h, c, smax, x0, delta, v0, sigma)
#    # возьмём максимум нормы по времени
#    norms = [max_norm(y_w[s,:]) for s in range(len(t_w))]
#    results.append((lam, max(norms)))
#
#for lam, M in results:
#    print(f"λ={lam:.2f}, max||y||={M:.3e}")




i0 = np.argmin(np.abs(x_w - x0))
u_t = y_weight[:, i0]
dt = tau
N = len(t_w)

# скорость и энергия в точке
v_t = np.gradient(u_t, dt)
E_t = 0.5 * v_t**2  # кинетическая энергия (локальная)

# спектры через FFT
freqs = np.fft.rfftfreq(N, d=dt)
U_f = np.fft.rfft(u_t)
V_f = np.fft.rfft(v_t)
E_f = np.fft.rfft(E_t)

# --------- улучшенные спектрограммы (одна δ) ---------
plt.figure(figsize=(10, 8))

# 1) спектр отклонения
plt.subplot(3, 1, 1)
plt.semilogy(freqs, np.abs(U_f))
plt.xlim(0, 50)                 # ограничиваем частоты
plt.ylabel('|U(f)|')
plt.title('Спектр отклонения в точке x0 (логарифмический масштаб)')
plt.grid(True, alpha=0.3)

# 2) спектр скорости
plt.subplot(3, 1, 2)
plt.semilogy(freqs, np.abs(V_f))
plt.xlim(0, 50)
plt.ylabel('|V(f)|')
plt.title('Спектр скорости в точке x0')
plt.grid(True, alpha=0.3)

# 3) спектр энергии (нормированный)
E_norm = np.abs(E_f) / np.max(np.abs(E_f))
plt.subplot(3, 1, 3)
plt.semilogy(freqs, E_norm)
plt.xlim(0, 50)
plt.xlabel('f')
plt.ylabel('|E(f)| / max')
plt.title('Нормированный спектр энергии в точке x0')
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# --------- энергетический спектр для разных δ ---------
deltas = [0.05, 0.1, 0.2]

plt.figure(figsize=(8, 5))

for delta_val in deltas:
    # пересчитываем решение для каждой δ
    x_w, t_w, y_w = wave_solver_weights(n, tau, h, c, smax, x0, delta_val, v0, sigma)
    i0 = np.argmin(np.abs(x_w - x0))
    u_t = y_w[:, i0]
    v_t = np.gradient(u_t, dt)
    E_t = 0.5 * v_t**2

    E_f = np.fft.rfft(E_t)
    freqs = np.fft.rfftfreq(len(t_w), d=dt)
    E_norm = np.abs(E_f) / np.max(np.abs(E_f))

    plt.semilogy(freqs, E_norm, label=f'δ={delta_val}')

plt.xlim(0, 50)
plt.xlabel('f')
plt.ylabel('нормированный |E(f)|')
plt.title('Нормированный энергетический спектр при разных δ (в точке x0)')
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.show()



deltas = [0.05, 0.1, 0.2]
plt.figure(figsize=(8, 5))

for delta in deltas:
    # пересчёт решения для каждого delta
    x_w, t_w, y_w = wave_solver_weights(n, tau, h, c, smax, x0, delta, v0, sigma)
    i0 = np.argmin(np.abs(x_w - x0))
    u_t = y_w[:, i0]
    v_t = np.gradient(u_t, tau)
    E_t = 0.5 * v_t**2
    E_f = np.fft.rfft(E_t)
    freqs = np.fft.rfftfreq(len(t_w), d=tau)

    plt.plot(freqs, np.abs(E_f), label=f'δ={delta}')

plt.xlim(0, freqs.max())
plt.xlabel('f')
plt.ylabel('|E(f)|')
plt.title('Энергетический спектр при разных δ')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

