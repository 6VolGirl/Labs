import numpy as np
import matplotlib.pyplot as plt



c = 1.0
l = 1.0
x0 = 0.5
delta = 0.1
v0 = 1.0
n = 200
h = l / n

# Условие устойчивости: lambda = c*tau/h <= 1
lam = 0.1
tau = lam * h / c

tmax = 2.0
smax = int(tmax / tau)

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

def wave_solver_explicit(n, tau, h, c, smax, x0, delta, v0):
    """
    Решает волновое уравнение явной схемой "крест"

    n : число внутренних узлов
    tau : временной шаг
    h : пространственный шаг
    c : скорость волны
    smax : число временных шагов
    x0, delta, v0 : параметры начальной скорости
    """

    x = np.arange(0, l + h / 2, h)
    t = np.arange(0, smax * tau + tau / 2, tau)
    m = len(x)
    y = np.zeros((smax + 1, m))

    lam = c * tau / h
    lam2 = lam ** 2

    y[0, :] = np.zeros_like(x)

    # y^1_i = tau * psi_i
    psi = np.zeros_like(x)
    mask = (x >= x0 - delta) & (x <= x0 + delta)
    psi[mask] = v0
    y[1, :] = y[0, :] + tau * psi
    y[1, 0] = 0
    y[1, -1] = 0

    # y^{s+1}_i = lambda^2 * (y^s_{i+1} - 2*y^s_i + y^s_{i-1}) + 2*y^s_i - y^{s-1}_i
    for s in range(1, smax):
        for i in range(1, m - 1):
            y[s + 1, i] = (lam2 * (y[s, i + 1] - 2 * y[s, i] + y[s, i - 1])
                           + 2 * y[s, i] - y[s - 1, i])

        y[s + 1, 0] = 0
        y[s + 1, -1] = 0

    return x, t[:smax + 1], y



x, t, y_numeric = wave_solver_explicit(n, tau, h, c, smax, x0, delta, v0)

y_exact = np.zeros_like(y_numeric)
for s in range(smax + 1):
    y_exact[s, :] = exact_solution_series(x, t[s], num_terms=200)


error = np.abs(y_numeric - y_exact)
max_error = np.max(error)
mean_error = np.mean(error)


# ============================================================================
# График 1: Решение в различные моменты времени
times_to_plot = [tau*smax]
indices = [int(tp / tau) for tp in times_to_plot if tp <= t[-1]]

idx = indices[0]

plt.figure(figsize=(10, 6))

# 1) точное и численное решение
plt.subplot(2, 1, 1)
plt.plot(x, y_exact[idx, :], '--', label=f'точное, t={t[idx]:.2f}')
plt.plot(x, y_numeric[idx, :], '-',  label=f'численное, t={t[idx]:.2f}')
plt.xlabel('x')
plt.ylabel('u(x,t)')
plt.title('Точное vs численное решение (схема "крест")')
plt.grid(True)
plt.legend()

# 2) погрешность
plt.subplot(2, 1, 2)
error_t = np.abs(y_numeric[idx, :] - y_exact[idx, :])
plt.plot(x, error_t, 'r', label='|числ - точн|')
plt.xlabel('x')
plt.ylabel('погрешность')
plt.title(f'Погрешность при t={t[idx]:.2f}')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()



fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# График 2: Карта решения (x, t)
ax = axes[0]
im1 = ax.contourf(x, t, y_numeric, levels=30, cmap='RdBu_r')
ax.set_xlabel('x', fontsize=11)
ax.set_ylabel('t', fontsize=11)
ax.set_title('Эволюция решения (x, t)', fontsize=12)
plt.colorbar(im1, ax=ax)

# График 3: Логарифм ошибки
ax = axes[1]
error_data = np.maximum(error, 1e-10)  # чтобы не было log(0)
im2 = ax.contourf(x, t, np.log10(error_data), levels=20, cmap='YlOrRd')
ax.set_xlabel('x', fontsize=11)
ax.set_ylabel('t', fontsize=11)
ax.set_title('log₁₀|u_числ - u_точн|', fontsize=12)
cbar = plt.colorbar(im2, ax=ax)
cbar.set_label('log₁₀(ошибка)', fontsize=10)

plt.show()



