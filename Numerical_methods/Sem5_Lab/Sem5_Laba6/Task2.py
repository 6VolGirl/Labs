import numpy as np
import matplotlib.pyplot as plt

import sys
sys.path.append(r"C:\Users\6anna\PycharmProjects\Labs\Numerical_methods\Numerical_methods_classes\Linear_Systems\Direct_Methods")
from TridiagonalMatrixAlgorithm import TridiagonalMatrixAlgorithm

def exact_sol(x, t):
    return np.exp(-np.pi**2 * t) * np.sin(np.pi * x)

def build_tridiagonal_matrix(n, mu, sigma):
        """
        Строит трёхдиагональную матрицу с параметром σ.

        Схема:
        -σμ * y_{i-1}^{s+1} + (1 + 2σμ) * y_i^{s+1} - σμ * y_{i+1}^{s+1} = RHS

        - n: число внутренних узлов (всего n+2 узла включая границы)
        - mu: μ = τ / h²
        """

        A = np.zeros((n, n))

        np.fill_diagonal(A, 1.0 + 2.0 * sigma * mu)
        np.fill_diagonal(A[:, 1:], -sigma * mu)
        np.fill_diagonal(A[1:, :], -sigma * mu)

        return A


def solve_scheme_all_times(tau, Nt, h, sigma, kappa=None):
    """
    Решает уравнение теплопроводности схемой с параметром σ ∈ [0, 1]
    и сохраняет решение для ВСЕХ времён.
    """

    L = 1.0
    n_nodes = int(L / h) + 1
    x = np.linspace(0, L, n_nodes)
    n = n_nodes - 2

    if kappa is None:
        kappa = lambda x: 1.0

    x_half = np.linspace(h/2, L - h/2, n_nodes - 1)
    kappa_half = np.array([kappa(x) for x in x_half])

    y = np.sin(np.pi * x)
    y[0] = 0.0
    y[-1] = 0.0

    results = {}
    results[0.0] = y.copy()

    mu = tau / (h ** 2)

    A = build_tridiagonal_matrix(n, mu, sigma)

    tma = TridiagonalMatrixAlgorithm()

    for s in range(Nt):
        rhs = np.zeros(n)
        for i in range(n):
            # Индексы включая границы
            idx = i + 1

            # Λ y_i^s = (1/h) * [κ_{i+1/2}*(y_{i+1} - y_i)/h - κ_{i-1/2}*(y_i - y_{i-1})/h]
            #kappa_right = kappa_half[idx]  # κ_{i+1/2}
            #kappa_left = kappa_half[idx - 1]  # κ_{i-1/2}
            #diff_right = (y[idx + 1] - y[idx]) / h
            #diff_left = (y[idx] - y[idx - 1]) / h
            #lambda_y = (kappa_right * diff_right - kappa_left * diff_left) / h
            #rhs[i] = y[idx] + sigma * mu * lambda_y

            # стандартный лапласиан на слое n
            # (как в C++: lap_n = u_{i+1}^n - 2u_i^n + u_{i-1}^n)
            uim1 = y[idx - 1]
            ui = y[idx]
            uip1 = y[idx + 1]
            lap_n = uip1 - 2.0 * ui + uim1
            # правая часть для θ-схемы (без источника f)
            # rhs = u_i^n + (1 - sigma) * mu * lap_n
            val = ui + (1.0 - sigma) * mu * lap_n

            # учёт граничных значений на шаге n+1 (они у нас = 0)
            # как в C++:
            # if (i == 1)     rhs += sigma*mu*u(s+1,0)
            # if (i == nx-2)  rhs += sigma*mu*u(s+1,nx-1)
            # но u(·,0)=u(·,nx-1)=0, поэтому добавлять нечего

            rhs[i] = val

        y_new_inner = tma.solve(A, np.array(rhs))

        y_new = np.zeros_like(y)
        y_new[0] = 0.0
        y_new[-1] = 0.0
        y_new[1:-1] = y_new_inner


        if np.max(np.abs(y_new)) > 1e10:
            print(f"Обнаружена неустойчивость на шаге s={s}, t={(s + 1) * tau:.6e}")
            print(f"   max|y| = {np.max(np.abs(y_new)):.4e}")
            break

        y = y_new
        t_curr = (s + 1) * tau
        results[t_curr] = y.copy()

    times = sorted(results.keys())
    return results, times, x


L = 1.0
t_max = 1.0
h_base = 1.0 / 20
tau = h_base / 20
#tau = 0.5 * h_base**2 * 0.1
Nt = int(t_max / tau)

sigma_values = [0.1, 0.5, 1.0]

results_list = []
times_dict = []
x_common = None

for sigma in sigma_values:
    results, times, x = solve_scheme_all_times(tau, Nt, h_base, sigma)
    results_list.append(results)
    times_dict.append(times)
    if x_common is None:
        x_common = x


# =====================================================================================
# График 1: распределение температур
fig, axes = plt.subplots(1, 3, figsize=(16, 5))

for idx, (results, sigma) in enumerate(zip(results_list, sigma_values)):
    ax = axes[idx]
    times = sorted(results.keys())
    indices = np.linspace(0, len(times) - 1, 5, dtype=int)

    colors = ['red', 'orange', 'green', 'blue', 'purple']

    for pidx, i in enumerate(indices):
        t = times[i]
        y_num = results[t]
        y_ex = exact_sol(x_common, t)
        err = np.abs(y_num - y_ex)
        max_err = err.max()
        l2_err = np.sqrt((err**2).mean())

        ax.plot(x_common, y_num,
                color=colors[pidx], linewidth=2.0,
                marker='o', markersize=3, alpha=0.7,
                label=f'num t={t:.4f}')
        print (f'num t={t:.4f}, max_err={max_err:.1e}')

        ax.plot(x_common, y_ex,
                color=colors[pidx], linestyle='--', linewidth=1.5, alpha=0.9,
                label=f'exact t={t:.4f}')

    ax.set_xlabel('x', fontsize=11)
    ax.set_ylabel('u(x,t)', fontsize=11)
    ax.set_title(f'σ = {sigma}', fontsize=12, fontweight='bold')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()



# =====================================================================================
# График 1-5: распределение температур
times_all = sorted(results_list[0].keys())
num_time_steps = 5
time_indices = np.linspace(0, len(times_all) - 1, num_time_steps, dtype=int)
selected_times = [times_all[i] for i in time_indices]

times_all = sorted(results_list[0].keys())
num_time_steps = 5
time_indices = np.linspace(0, len(times_all) - 1, num_time_steps, dtype=int)
selected_times = [times_all[i] for i in time_indices]

for time_idx, t_plot in enumerate(selected_times):
    fig, axes = plt.subplots(1, 3, figsize=(16, 5), squeeze=False)  # squeeze=False гарантирует 2D-массив осей
    fig.suptitle(f'Момент времени t = {t_plot:.6f}', fontsize=14, fontweight='bold')

    for sigma_idx, (results, sigma) in enumerate(zip(results_list, sigma_values)):
        ax = axes[0, sigma_idx]  # Используем предварительно созданные оси

        times = sorted(results.keys())
        t_nearest = min(times, key=lambda t: abs(t - t_plot))

        y_num = results[t_nearest]
        U_exact = exact_sol(x_common, t_nearest)
        err = np.abs(y_num - U_exact)

        ax.plot(x_common, y_num, 'r-o', linewidth=2.5, markersize=4, label='Численное', markevery=3, alpha=0.8)
        ax.plot(x_common, U_exact, 'b--', linewidth=2.5, label='Точное', alpha=0.8)
        ax.fill_between(x_common, y_num, U_exact, alpha=0.2, color='gray')

        max_err = err.max()
        l2_err = np.sqrt((err ** 2).mean())
        rel_err = max_err / (np.abs(U_exact).max() + 1e-10)

        y_lim_min = min(y_num.min(), U_exact.min()) * 1.05  # 5% запаса снизу
        y_lim_max = max(y_num.max(), U_exact.max()) * 1.05  # 5% запаса сверху
        ax.set_ylim([y_lim_min, y_lim_max])

        ax.set_xlabel('x', fontsize=10)
        ax.set_ylabel('u(x,t)', fontsize=10)
        ax.set_title(f'σ = {sigma}\nmax_err = {max_err:.2e}', fontsize=11, fontweight='bold')
        ax.legend(fontsize=9)
        ax.grid(True, alpha=0.3)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    #plt.savefig(f'time_{t_plot:.6f}.png', dpi=150)
    #plt.close(fig)
    plt.show()




tau = 1.0 / 20.0
sigma_values = [0.1, 0.3, 0.5, 0.7, 1.0]
h_values = [1 / 10, 1 / 20, 1 / 40, 1 / 80]
errs = []
err_min = np.inf
best_h, best_sigma = None, None

for h in h_values:
    Nt = int(t_max / tau)
    for sigma in sigma_values:
        results, times, x = solve_scheme_all_times(tau, Nt, h, sigma)

        # считаем err = max_{s,i} |U(x_i,t_s) - y_i^s|
        curr_err = 0.0
        for t in times:
            y_num = results[t]
            y_ex = exact_sol(x, t)
            curr_err = max(curr_err, np.max(np.abs(y_num - y_ex)))

        errs.append((h, sigma, curr_err))

        if curr_err < err_min:
           err_min = curr_err
           best_h, best_sigma = h, sigma

print(f"Минимальная ошибка err = {err_min:.3e} при h = {best_h}, σ = {best_sigma}")

hs = np.array([e[0] for e in errs])
sgs = np.array([e[1] for e in errs])
es = np.array([e[2] for e in errs])

# err(h) для каждого σ
plt.figure(figsize=(7, 5))
for sigma in sigma_values:
    hs_loc = [h for (h, s, e) in errs if s == sigma]
    es_loc = [e for (h, s, e) in errs if s == sigma]
    plt.loglog(hs_loc, es_loc, 'o-', label=f'σ={sigma}')
plt.xlabel('h')
plt.ylabel('err')
plt.grid(True, which='both')
plt.legend()
plt.title('err(h) при разных σ')
plt.show()

# err(σ) для каждого h
plt.figure(figsize=(7, 5))
for h in h_values:
    sgs_loc = [s for (hh, s, e) in errs if hh == h]
    es_loc = [e for (hh, s, e) in errs if hh == h]
    plt.semilogy(sgs_loc, es_loc, 'o-', label=f'h={h:.3f}')
plt.xlabel('σ')
plt.ylabel('err')
plt.grid(True, which='both')
plt.legend()
plt.title('err(σ) при разных h')
plt.show()

from matplotlib.colors import LogNorm


t_max = 1.0
tau = 1.0 / 20.0
Nt = int(np.ceil(t_max / tau))

sigma_vals = np.linspace(0.1, 1, 11)
h_vals = np.array([1 / 10, 1 / 15, 1 / 20, 1 / 30, 1 / 40, 1 / 50, 1 / 60, 1 / 80])
err_matrix = np.zeros((len(sigma_vals), len(h_vals)))

print("Начинаю расчет сетки параметров...")

for i, sigma in enumerate(sigma_vals):
    for j, h in enumerate(h_vals):
        results, times, x = solve_scheme_all_times(tau, Nt, h, sigma)
        curr_err = 0.0

        if len(results) < Nt:
            curr_err = np.inf
        else:
            for t in times:
                if t == 0: continue
                y_num = results[t]
                y_ex = exact_sol(x, t)

                if not np.all(np.isfinite(y_num)):
                    curr_err = np.inf
                    break

                err_t = np.max(np.abs(y_num - y_ex))
                curr_err = max(curr_err, err_t)

        err_matrix[i, j] = curr_err

max_val_for_plot = 1e2
err_matrix_plot = np.minimum(err_matrix, max_val_for_plot)
err_matrix_plot[err_matrix > 1e10] = max_val_for_plot  # явно помечаем взрывы

# =====================================================================================
# ПОСТРОЕНИЕ DENSITY PLOT
fig, ax = plt.subplots(figsize=(10, 7))

# Используем pcolormesh, чтобы оси были правильными
# Создаем 2D сетки координат для pcolormesh
H, S = np.meshgrid(h_vals, sigma_vals)

# Рисуем
# norm=LogNorm() включает логарифмическую шкалу цвета
c = ax.pcolormesh(H, S, err_matrix_plot, shading='nearest', cmap='viridis', norm=LogNorm())

plt.colorbar(c, ax=ax, label='Максимальная ошибка (log scale)')

# Настройка осей
ax.set_xlabel('Шаг по пространству h', fontsize=12)
ax.set_ylabel('Вес схемы σ', fontsize=12)
ax.set_title(f'Density plot ошибки при τ = {tau}', fontsize=14, fontweight='bold')

# Инвертируем ось X, чтобы уменьшение h шло вправо (или влево, как удобнее)
# Обычно density plot рисуют с 0 слева. Оставим стандартно: слева малые h?
# Нет, h_vals у нас идут от больших к малым (1/10 -> 1/80).
ax.invert_xaxis()

# Добавим текстовые метки (опционально, если нужно видеть числа)
# Но для density plot лучше видеть общую картину.

# Линия теоретической устойчивости (примерно)
# mu <= 1 / (2(1-2sigma))  =>  sigma >= 0.5 * (1 - 1/mu)
# Это сложная кривая, можно не рисовать, цвета сами покажут границу.

plt.tight_layout()
plt.show()
