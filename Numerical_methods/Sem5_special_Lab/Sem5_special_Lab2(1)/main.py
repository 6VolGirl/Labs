import numpy as np
import matplotlib.pyplot as plt
import random
import math


M = 500  # Число испытаний
N = 500   # Число временных шагов
dt = 0.01
D = 1   # Коэффициент диффузии (безразмерный)
F = 1   # Внешняя сила
V0 = 0
L = 1
x0 = 0
zeta = 1
v = F/zeta


# #
# def generate_trajectory (M, N, dt, D, x0):
#     t = np.linspace(0, N * dt, N + 1)
#     # x[i,n] = координата i-го испытания в момент n
#     x = np.zeros((M, N + 1))
#     for i in range(M):
#         x[i, 0] = x0
#         for n in range(N):
#             w = np.random.randn()  # нормальное(Гауссовское) распределение
#             x[i, n + 1] = x[i, n] + F * dt + np.sqrt(2 * D * dt) * w
#     return x, t

def generate_trajectory (M, N, dt, D, x0):
    t = np.linspace(0, N * dt, N + 1)
    # x[i,n] = координата i-го испытания в момент n
    x = np.zeros((M, N + 1))
    for i in range(M):
        x[i, 0] = x0
        for n in range(N):
            w = np.random.randn()  # нормальное(Гауссовское) распределение
            x[i, n + 1] = x[i, n] +(2*math.pi * V0 * math.cos(2*math.pi* x[i, n]) - F) * dt + np.sqrt(2 * dt) * w
    return x, t


x, t = generate_trajectory (M, N, dt, D, x0)


# График 1: Семейство траекторий
plt.figure(figsize=(8,4))
for i in range(10):
    plt.plot(t, x[i, :], alpha=0.7)
plt.xlabel('Время')
plt.ylabel('Координата')
plt.title('Семейство броуновских траекторий')
plt.show()

# График 2: <x(t)>
mean_x = np.mean(x, axis=0)
plt.plot(t, mean_x)
plt.xlabel('Время')
plt.ylabel('<x(t)>')
plt.title(f'Средний сдвиг <x(t)> --> x(0)={x0}')
plt.show()

#  <( x(t)-x(0) )^2>
msd = np.mean((x-x0)**2, axis=0)

plt.plot(t, msd, label='Численное <x²>')
plt.plot(t, 2*D*t, 'r--', label='Теор. 2Dt')
plt.xlabel('Время')
plt.ylabel('<x²(t)>')
plt.legend()
plt.title('Среднеквадратичное смещение')
plt.show()



x = t[3:]
y = msd[3:]

x_mean = np.mean(x)
y_mean = np.mean(y)

# y = kx+b
slope = np.sum((x - x_mean) * (y - y_mean)) / np.sum((x - x_mean)**2)  # k
intercept = y_mean - slope * x_mean  # b


D_estimate = slope / 2
print(f'y = kx+b      y = {slope}x +{intercept}')
print(f'D_estimate = {D_estimate}')

#------------------------------------------------------------------------------------------------------------
# Пункт 2
#------------------------------------------------------------------------------------------------------------

def double_factorial(n):
    if n <= 0:
        return 1
    result = 1
    while n > 0:
        result *= n
        n -= 2
    return result

def theoretical_moments(n, t, D):
    if n%2 == 0:
        return double_factorial(n-1) * (2*D*t)**(n/2)
    else:
        return np.zeros_like(t)

def compute_moments(n, x, x0):
    delta = x - x0
    return np.mean(delta**n, axis = 0)

N = 20
M_values = [100, 1000, 5000]


M_result = {}
for M in M_values:
    x, t = generate_trajectory(M, N, dt, D, x0)
    M_theor = []
    M_compute = []
    for i in range(1, 5):
        M_theor.append(theoretical_moments(i, t, D))
        M_compute.append(compute_moments(i, x, x0))
    M_result[M] = {
        'theor':M_theor,
        'compute':M_compute
    }

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

moment_names = ['M₁', 'M₂', 'M₃', 'M₄']
colors_M = {100: 'blue', 1000: 'green', 5000: 'purple'}

for i in range(4):
    row = i // 2
    col = i % 2
    n = i + 1  # Номер момента (1, 2, 3, 4)

    ax = axes[row, col]

    # Теоретическая линия (одна для всех M)
    M_theor_plot = M_result[M_values[0]]['theor'][i]
    ax.plot(t, M_theor_plot, '--', linewidth=2.5, color='red',
            label='Теория', zorder=10)

    # Численные линии для разных M
    for M in M_values:
        M_compute_plot = M_result[M]['compute'][i]
        ax.plot(t, M_compute_plot, 'o-', linewidth=2, markersize=4,
                color=colors_M[M], alpha=0.8,
                label=f'Численное (M={M})')

    # Горизонтальная линия для нечетных моментов
    if n % 2 == 1:
        ax.axhline(0, color='gray', linestyle=':', linewidth=1, alpha=0.5)

    ax.set_xlabel('Время t', fontsize=11)
    ax.set_ylabel(f'{moment_names[i]}(t)', fontsize=11)
    ax.set_title(f'{moment_names[i]} - момент {n}-го порядка',
                 fontsize=12, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(alpha=0.3)

plt.tight_layout()
plt.savefig('moments_comparison_M.png', dpi=150)
plt.show()



#------------------------------------------------------------------------------------------------------------
# Пункт 3
#------------------------------------------------------------------------------------------------------------

def theoretical_solution_Smolyx(x, t, D, x0):
    """
        Аналитическое решение уравнения Смолуховского:
        Если F = 0:  ρ(x,t) = (1/√(4πDt)) × exp(-(x-x₀)²/(4Dt))
        Если F != 0: ρ(x,t) = (1/√(4πDt)) × exp(-(x-vt)²/(4Dt))
    """
    coef = 1/ np.sqrt(4*math.pi*D*t)
    if F==0:
        return coef * np.exp(-(x-x0)**2/(4*D*t))
    else:
        return coef * np.exp(-(x-v*t)**2/(4*D*t))


N = 200
M = 1000

time_analysis = [0.1, 0.5, 1, 1.5]

x, t = generate_trajectory(M, N, dt, D, x0)

t_actual = []
idx_actual = []

for t_i in time_analysis:
    diffs = np.abs(t - t_i)
    min_val = np.min(diffs)
    idx = np.where(diffs == min_val)[0][0]   # индекс ближайшего времени к интересующему нас

    idx_actual.append(idx)
    t_actual.append(t[idx])

fig, axes = plt.subplots(2, 2, figsize=(15, 12))
axes = axes.flatten()

# Параметры гистограммы
n_bins = 60  # Число бинов
colors_hist = ['blue', 'green', 'orange', 'red']

for plot_idx, (idx, t_actual) in enumerate(zip(idx_actual, t_actual)):
    ax = axes[plot_idx]
    x_at_t = x[:, idx]

    # Построение гистограммы с нормализацией (чтобы площадь = 1)
    counts, bins, patches = ax.hist(x_at_t, bins=n_bins, density=True, alpha=0.6, color=colors_hist[plot_idx],
                                    edgecolor='black', linewidth=0.7, label='Численная гистограмма')
    x_theory = np.linspace(np.min(x_at_t) - 1, np.max(x_at_t) + 1, 500)
    pdf_theory = theoretical_solution_Smolyx(x_theory, t_actual, D, x0)

    ax.plot(x_theory, pdf_theory, 'r-', linewidth=3, label='Теория ρ(x,t)')

    mean_numerical = np.mean(x_at_t)
    std_numerical = np.std(x_at_t)

    std_theory = np.sqrt(2 * D * t_actual)

    # Оформление графика
    ax.set_xlabel('Координата x', fontsize=12)
    ax.set_ylabel('Плотность вероятности ρ(x,t)', fontsize=12)
    ax.set_title(f't = {t_actual:.3f}',
                 fontsize=13, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(alpha=0.3)
    ax.axvline(x0, color='gray', linestyle='--', linewidth=2, alpha=0.5, label='x₀')

plt.show()