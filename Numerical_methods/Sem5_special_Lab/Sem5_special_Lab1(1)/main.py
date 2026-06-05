import numpy as np
import sys
import os
import matplotlib.pyplot as plt

sys.path.append ("C:\\Users\\6anna\PycharmProjects\\Labs\\Numerical_methods\\Numerical_methods_classes\\Ordinary_Differential_Equations(ODE)")
from EulerExplicit import EulerExplicit
from EulerImplicit import EulerImplicit
from ImprovedEuler import ImprovedEuler
from GearMethod import GearMethod


def f_system(t, Y):
    y, z = Y
    dydt = 998 * y + 1998 * z
    dzdt = -999 * y - 1999 * z
    return np.array([dydt, dzdt])

t0 = 0.0
t_end = 0.1
Y0 = np.array([1.0, 1.0])  # y(0) = 1, z(0) = 1


# б) Явный метод Эйлера

h_values_explicit = [0.0001, 0.001, 0.002, 0.003]
results_explicit = {}
print("Явный метод Эйлера")

for h in h_values_explicit:
    print(f"\nШаг h = {h}")

    euler_exp = EulerExplicit()
    t_exp, Y_exp = euler_exp.solve(f_system, t0, t_end, Y0, h)

    print(f"  Y(0.1) = [{Y_exp[-1, 0]:.4e}, {Y_exp[-1, 1]:.4e}]")

    results_explicit[h] = {
        't': t_exp,
        'Y': Y_exp,
        'method': euler_exp
    }


# в) Неявный метод Эйлера

h_values_implicit = [0.01, 0.02, 0.025]
results_implicit = {}
print("Неявный метод Эйлера")

for h in h_values_implicit:
    print(f"\nШаг h = {h}")

    euler_imp = EulerImplicit()
    t_imp, Y_imp = euler_imp.solve(f_system, t0, t_end, Y0, h)

    print(f"  Y(0.1) = [{Y_imp[-1, 0]:.4e}, {Y_imp[-1, 1]:.4e}]")

    results_implicit[h] = {
        't': t_imp,
        'Y': Y_imp,
        'method': euler_imp
    }


# г) Усовершенствованный метод Эйлера 2 порядка

h_values_improved = [0.001, 0.002, 0.0025]
results_improved = {}
print("Усовершенствованный метод Эйлера")

for h in h_values_improved:
    print(f"\nШаг h = {h}")

    euler_improv = ImprovedEuler()
    t_improv, Y_improv = euler_improv.solve(f_system, t0, t_end, Y0, h)

    print(f"  Y(0.1) = [{Y_improv[-1, 0]:.4e}, {Y_improv[-1, 1]:.4e}]")

    results_improved[h] = {
        't': t_improv,
        'Y': Y_improv,
        'method': euler_improv
    }




# =============================================================================
# ПОСТРОЕНИЕ ГРАФИКОВ
# =============================================================================
#
def exact_solution(t):
#     """
#     Точное решение:
#     y(t) = 4exp(-t) - 3exp(-1000*t)
#     z(t) = -2exp(-t) + 3exp(-1000*t)
#     """
     y_exact = 4 * np.exp(-t) - 3 * np.exp(-1000 * t)
     z_exact = -2 * np.exp(-t) + 3* np.exp(-1000 * t)
     return np.array([y_exact, z_exact])

t_exact_fine = np.linspace(t0, t_end, 1000)
Y_exact_fine = np.array([exact_solution(t) for t in t_exact_fine])


# # График 1: ЯВНЫЙ МЕТОД - устойчивость
# fig = plt.figure(figsize=(18, 5))
# fig.suptitle('Б) ЯВНЫЙ МЕТОД ЭЙЛЕРА: Влияние шага на устойчивость',
#              fontsize=14, fontweight='bold')
#
# n_plots = len(h_values_explicit)
#
# for idx, h in enumerate(h_values_explicit):
#     res = results_explicit[h]
#     t = res['t']
#     Y = res['Y']
#     y = Y[:, 0]
#     z = Y[:, 1]
#
#     ax = plt.subplot(1, n_plots, idx + 1)
#
#     plt.plot(t_exact_fine, Y_exact_fine[:, 0], 'k--', alpha=0.5, linewidth=1, label='Точное y(t)')
#     plt.plot(t_exact_fine, Y_exact_fine[:, 1], 'k:', alpha=0.5, linewidth=1, label='Точное z(t)')
#     plt.plot(t, y, 'r-', linewidth=2, label='y(t)')
#     plt.plot(t, z, 'b-', linewidth=2, label='z(t)')
#
#     plt.xlabel('t', fontsize=11)
#     plt.ylabel('y, z', fontsize=11)
#     plt.title(f'h = {h}', fontsize=12, fontweight='bold')
#     plt.legend(fontsize=9)
#     plt.grid(True, alpha=0.3)
#
# plt.tight_layout()
# plt.savefig('явный_эйлер.png', dpi=150, bbox_inches='tight')
# plt.show()
#
# # =============================================================================
#
# # График 2: НЕЯВНЫЙ МЕТОД - устойчивость
# fig2 = plt.figure(figsize=(14, 5))
# fig2.suptitle('В) НЕЯВНЫЙ МЕТОД ЭЙЛЕРА: Сравнение шагов h = 0.01, 0.02, 0.025',
#               fontsize=13, fontweight='bold')
#
# # y(t)
# ax1 = plt.subplot(1, 2, 1)
# plt.plot(t_exact_fine, Y_exact_fine[:, 0], 'k-', linewidth=2.5, label='Точное y(t)')
# for h in h_values_implicit:
#     res = results_implicit[h]
#     plt.plot(res['t'], res['Y'][:, 0], '-o', linewidth=2, markersize=5, label=f'h = {h}')
# plt.xlabel('t', fontsize=11)
# plt.ylabel('y(t)', fontsize=11)
# plt.title('Компонента y(t)', fontsize=12)
# plt.legend()
# plt.grid(True, alpha=0.3)
#
# # z(t)
# ax2 = plt.subplot(1, 2, 2)
# plt.plot(t_exact_fine, Y_exact_fine[:, 1], 'k-', linewidth=2.5, label='Точное z(t)')
# for h in h_values_implicit:
#     res = results_implicit[h]
#     plt.plot(res['t'], res['Y'][:, 1], '-s', linewidth=2, markersize=5, label=f'h = {h}')
# plt.xlabel('t', fontsize=11)
# plt.ylabel('z(t)', fontsize=11)
# plt.title('Компонента z(t)', fontsize=12)
# plt.legend()
# plt.grid(True, alpha=0.3)
#
# plt.tight_layout()
# plt.savefig('2_неявный_эйлер.png', dpi=150)
# plt.show()
#
# # =============================================================================
#
# # График 3: Усовершенствованный метод Эйлера 2 порядка
# fig5 = plt.figure(figsize=(14, 5))
# fig5.suptitle('Г) УЛУЧШЕННЫЙ МЕТОД ЭЙЛЕРА (2-й порядок): Сравнение шагов h = 0.001, 0.002, 0.0025',
#               fontsize=13, fontweight='bold')
#
# # y(t)
# ax1 = plt.subplot(1, 2, 1)
# plt.plot(t_exact_fine, Y_exact_fine[:, 0], 'k-', linewidth=2.5, label='Точное y(t)')
# for h in h_values_improved:
#     res = results_improved[h]
#     plt.plot(res['t'], res['Y'][:, 0], '-^', linewidth=2, markersize=5, label=f'h = {h}')
# plt.xlabel('t', fontsize=11)
# plt.ylabel('y(t)', fontsize=11)
# plt.title('Компонента y(t)', fontsize=12, fontweight='bold')
# plt.legend()
# plt.grid(True, alpha=0.3)
#
# # z(t)
# ax2 = plt.subplot(1, 2, 2)
# plt.plot(t_exact_fine, Y_exact_fine[:, 1], 'k-', linewidth=2.5, label='Точное z(t)')
# for h in h_values_improved:
#     res = results_improved[h]
#     plt.plot(res['t'], res['Y'][:, 1], '-^', linewidth=2, markersize=5, label=f'h = {h}')
# plt.xlabel('t', fontsize=11)
# plt.ylabel('z(t)', fontsize=11)
# plt.title('Компонента z(t)', fontsize=12, fontweight='bold')
# plt.legend()
# plt.grid(True, alpha=0.3)
#
# plt.tight_layout()
# plt.savefig('3_улучшенный_эйлер.png', dpi=150, bbox_inches='tight')
# plt.show()
#
#
# # =============================================================================
#
# # График 4: сравнение ЯВНОГО и НЕЯВНОГО Эйлеров
# fig3 = plt.figure(figsize=(14, 5))
# fig3.suptitle('СРАВНЕНИЕ: Явный (h=0.0001) vs Неявный (h=0.01) vs Ус. Эйлер (h=0.001)',
#               fontsize=14, fontweight='bold')
#
# h_exp_best = 0.0001
# h_imp_best = 0.01
# h_impr_best = 0.001
#
# res_exp = results_explicit[h_exp_best]
# res_imp = results_implicit[h_imp_best]
# res_impr = results_improved[h_impr_best]
#
# # y(t)
# ax1 = plt.subplot(1, 2, 1)
# plt.plot(t_exact_fine, Y_exact_fine[:, 0], 'k-', linewidth=2, label='Точное')
# plt.plot(res_exp['t'], res_exp['Y'][:, 0], 'r-', linewidth=2, label=f'Явный (h={h_exp_best})')
# plt.plot(res_imp['t'], res_imp['Y'][:, 0], 'b--', linewidth=2, marker='o',
#          markersize=5, label=f'Неявный (h={h_imp_best})')
# plt.plot(res_impr['t'], res_impr['Y'][:, 0], 'g-.', linewidth=2, marker='^',
#          markersize=5, label=f'Улучш. Эйлер (h={h_impr_best})')
# plt.xlabel('t')
# plt.ylabel('y(t)')
# plt.title('Компонента y(t)')
# plt.legend(fontsize=10)
# plt.grid(True, alpha=0.3)
#
# # z(t)
# ax2 = plt.subplot(1, 2, 2)
# plt.plot(t_exact_fine, Y_exact_fine[:, 1], 'k-', linewidth=2, label='Точное')
# plt.plot(res_exp['t'], res_exp['Y'][:, 1], 'r-', linewidth=2, label=f'Явный (h={h_exp_best})')
# plt.plot(res_imp['t'], res_imp['Y'][:, 1], 'b--', linewidth=2, marker='s',
#          markersize=5, label=f'Неявный (h={h_imp_best})')
# plt.plot(res_impr['t'], res_impr['Y'][:, 1], 'g-.', linewidth=2, marker='^',
#          markersize=5, label=f'Улучш. Эйлер (h={h_impr_best})')
# plt.xlabel('t')
# plt.ylabel('z(t)')
# plt.title('Компонента z(t)')
# plt.legend(fontsize=10)
# plt.grid(True, alpha=0.3)
#
# plt.tight_layout()
# plt.savefig('график_сравнение_трёх_методов.png', dpi=150, bbox_inches='tight')
# plt.show()
#
# # =============================================================================
#
#
# #График 4: погрешности: норма, абсолютная, относительная
#
# fig4 = plt.figure(figsize=(18, 5))
# fig4.suptitle('АНАЛИЗ ПОГРЕШНОСТИ РЕШЕНИЯ', fontsize=14, fontweight='bold')
#
# h_values_explicit_stable = [h for h in h_values_explicit if h != 0.003]
#
# # ПОДГРАФИК 1: НОРМА ПОГРЕШНОСТИ
# ax1 = plt.subplot(1, 3, 1)
#
# # Явный метод - норма
# for h in h_values_explicit_stable:
#     res = results_explicit[h]
#     t = res['t']
#     Y = res['Y']
#
#     error_data = res['method'].compute_error(exact_solution, t, Y)
#     plt.semilogy(t, error_data['norm'], '-', linewidth=2, label=f'Явный h={h}')
#
# # Неявный метод - норма
# for h in h_values_implicit:
#     res = results_implicit[h]
#     t = res['t']
#     Y = res['Y']
#
#     error_data = res['method'].compute_error(exact_solution, t, Y)
#     plt.semilogy(t, error_data['norm'], '--o', linewidth=2, markersize=3,
#                  label=f'Неявный h={h}')
#
# plt.xlabel('t', fontsize=11)
# plt.ylabel('||Y_численное - Y_точное||', fontsize=11)
# plt.title('Евклидова норма погрешности', fontsize=12, fontweight='bold')
# plt.legend(fontsize=8)
# plt.grid(True, alpha=0.3, which='both')
#
#
# # ПОДГРАФИК 2: АБСОЛЮТНАЯ ПОГРЕШНОСТЬ
# ax2 = plt.subplot(1, 3, 2)
#
# # Явный метод - абсолютная
# for h in h_values_explicit_stable:
#     res = results_explicit[h]
#     t = res['t']
#     Y = res['Y']
#
#     error_data = res['method'].compute_error(exact_solution, t, Y)
#     max_abs_error = np.max(error_data['absolute'], axis=1)
#     plt.semilogy(t, max_abs_error, '-', linewidth=2, label=f'Явный h={h}')
#
# # Неявный метод - абсолютная
# for h in h_values_implicit:
#     res = results_implicit[h]
#     t = res['t']
#     Y = res['Y']
#
#     error_data = res['method'].compute_error(exact_solution, t, Y)
#     max_abs_error = np.max(error_data['absolute'], axis=1)
#     plt.semilogy(t, max_abs_error, '--o', linewidth=2, markersize=3,
#                  label=f'Неявный h={h}')
#
# plt.xlabel('t', fontsize=11)
# plt.ylabel('max(|Y_численное - Y_точное|)', fontsize=11)
# plt.title('Абсолютная погрешность (макс по компонентам)', fontsize=12, fontweight='bold')
# plt.legend(fontsize=8)
# plt.grid(True, alpha=0.3, which='both')
#
# # ПОДГРАФИК 3: ОТНОСИТЕЛЬНАЯ ПОГРЕШНОСТЬ
# ax3 = plt.subplot(1, 3, 3)
#
# # Явный метод - относительная
# for h in h_values_explicit_stable:
#     res = results_explicit[h]
#     t = res['t']
#     Y = res['Y']
#
#
#     error_data = res['method'].compute_error(exact_solution, t, Y)
#     rel_error = np.max(error_data['relative'], axis=1)
#     rel_error[rel_error < 1e-16] = 1e-16  # Минимум для логарифма
#     plt.semilogy(t, rel_error, '-', linewidth=2, label=f'Явный h={h}')
#
# # Неявный метод - относительная
# for h in h_values_implicit:
#     res = results_implicit[h]
#     t = res['t']
#     Y = res['Y']
#
#     error_data = res['method'].compute_error(exact_solution, t, Y)
#     rel_error = np.max(error_data['relative'], axis=1)
#     rel_error[rel_error < 1e-16] = 1e-16
#     plt.semilogy(t, rel_error, '--o', linewidth=2, markersize=3,
#                  label=f'Неявный h={h}')
#
# plt.xlabel('t', fontsize=11)
# plt.ylabel('max(|ΔY| / |Y_точное|)', fontsize=11)
# plt.title('Относительная погрешность', fontsize=12, fontweight='bold')
# plt.legend(fontsize=8)
# plt.grid(True, alpha=0.3, which='both')
#
# plt.tight_layout()
# plt.savefig('погрешность_анализ.png', dpi=150, bbox_inches='tight')
# plt.show()

# =============================================================================


#График 5: погрешности усовершенствованного: норма, абсолютная, относительная

fig5 = plt.figure(figsize=(18, 5))
fig5.suptitle('ПОГРЕШНОСТЬ: Усовершествованный метод Эйлера ', fontsize=14, fontweight='bold')

# ПОДГРАФИК 1: НОРМА ПОГРЕШНОСТИ
ax1 = plt.subplot(1, 3, 1)
for h in h_values_improved:
    res = results_improved[h]
    t = res['t']
    Y = res['Y']
    error_data = res['method'].compute_error(exact_solution, t, Y)
    plt.semilogy(t, error_data['norm'], '-^', linewidth=2, markersize=4, label=f'h={h}')
plt.xlabel('t', fontsize=11)
plt.ylabel('||Y_чисlenное - Y_точное||', fontsize=11)
plt.title('Евклидова норма погрешности', fontsize=12, fontweight='bold')
plt.legend(fontsize=8)
plt.grid(True, alpha=0.3, which='both')

# ПОДГРАФИК 2: АБСОЛЮТНАЯ ПОГРЕШНОСТЬ
ax2 = plt.subplot(1, 3, 2)
for h in h_values_improved:
    res = results_improved[h]
    t = res['t']
    Y = res['Y']
    error_data = res['method'].compute_error(exact_solution, t, Y)
    max_abs_error = np.max(error_data['absolute'], axis=1)
    plt.semilogy(t, max_abs_error, '-^', linewidth=2, markersize=4, label=f'h={h}')
plt.xlabel('t', fontsize=11)
plt.ylabel('max(|Y_численное - Y_точное|)', fontsize=11)
plt.title('Абсолютная погрешность', fontsize=12, fontweight='bold')
plt.legend(fontsize=8)
plt.grid(True, alpha=0.3, which='both')

# ПОДГРАФИК 3: ОТНОСИТЕЛЬНАЯ ПОГРЕШНОСТЬ
ax3 = plt.subplot(1, 3, 3)
for h in h_values_improved:
    res = results_improved[h]
    t = res['t']
    Y = res['Y']
    error_data = res['method'].compute_error(exact_solution, t, Y)
    rel_error = np.max(error_data['relative'], axis=1)
    rel_error[rel_error < 1e-16] = 1e-16
    plt.semilogy(t, rel_error, '-^', linewidth=2, markersize=4, label=f'h={h}')
plt.xlabel('t', fontsize=11)
plt.ylabel('max(|ΔY| / |Y_точное|)', fontsize=11)
plt.title('Относительная погрешность', fontsize=12, fontweight='bold')
plt.legend(fontsize=8)
plt.grid(True, alpha=0.3, which='both')

plt.tight_layout()
plt.savefig('погрешность_улучшенный_эйлер.png', dpi=150, bbox_inches='tight')
plt.show()


# =============================================================================
# Метод Гира
# =============================================================================

h_e = 0.001
h_values_d = [h_e, h_e * 2]
results_d = {}

for h in h_values_d :
    print(f"\nШаг h = {h}")
    gear_d = GearMethod(order=1)
    t_d, Y_d = gear_d.solve(f_system, t0, t_end, Y0, h)
    results_d[h] = {
        't': np.array(t_d),
        'Y': np.array(Y_d),
        'method': gear_d,
        'order': 1
    }

gear_e = GearMethod(order=4)
t_e, Y_e = gear_e.solve(f_system, t0, t_end, Y0, h_e)
results_e = {
    't': np.array(t_e),
    'Y': np.array(Y_e),
    'method': gear_e,
    'order': 4
}
results_star_gear = {}
for i in range(1, 4):
    gear_e = GearMethod(order=4, integration_method = GearMethod, integration_order =i)
    t_e, y_e = gear_e.solve(f_system, t0, t_end, Y0, h_e)
    results_star_gear[i] = {
        't': np.array(t_e),
        'Y': np.array(y_e),
        'method': gear_e,
        'order': 4
    }
    print(y_e)

# =============================================================================
# ПОСТРОЕНИЕ ГРАФИКОВ
# =============================================================================
fig, axes = plt.subplots(1, 2, figsize=(15, 6))

# Параметры визуализации
colors = {1: 'blue', 2: 'green', 3: 'red'}
markers = {1: 'o', 2: 's', 3: '^'}
labels = {1: 'Гир-1 (одношаговый)', 2: 'Гир-2 (двухшаговый)', 3: 'Гир-3 (трехшаговый)'}

# График 1: Первая компонента y₁(t)
ax1 = axes[0]
for i in range(1, 4):
    t_vals = results_star_gear[i]['t']
    Y_vals = results_star_gear[i]['Y']

    # Начальные точки (первые 4) — большие маркеры
    ax1.plot(t_vals[:4], Y_vals[:4, 0], markers[i], markersize=12,
             color=colors[i], markeredgecolor='black', markeredgewidth=1.5,
             label=f'{labels[i]} (начальные)', zorder=10)

    # Полное решение — линия
    ax1.plot(t_vals, Y_vals[:, 0], '-', linewidth=2.5,
             color=colors[i], alpha=0.6, zorder=5)

ax1.set_xlabel('Время t', fontsize=13, fontweight='bold')
ax1.set_ylabel('$y_1(t)$', fontsize=13, fontweight='bold')
ax1.set_title('Первая компонента: Сравнение инициализаций',
              fontsize=14, fontweight='bold')
ax1.legend(fontsize=10, loc='best')
ax1.grid(True, alpha=0.3)

# График 2: Вторая компонента y₂(t)
ax2 = axes[1]
for i in range(1, 4):
    t_vals = results_star_gear[i]['t']
    Y_vals = results_star_gear[i]['Y']

    # Начальные точки
    ax2.plot(t_vals[:4], Y_vals[:4, 1], markers[i], markersize=12,
             color=colors[i], markeredgecolor='black', markeredgewidth=1.5,
             label=f'{labels[i]} (начальные)', zorder=10)

    # Полное решение
    ax2.plot(t_vals, Y_vals[:, 1], '-', linewidth=2.5,
             color=colors[i], alpha=0.6, zorder=5)

ax2.set_xlabel('Время t', fontsize=13, fontweight='bold')
ax2.set_ylabel('$y_2(t)$', fontsize=13, fontweight='bold')
ax2.set_title('Вторая компонента: Сравнение инициализаций',
              fontsize=14, fontweight='bold')
ax2.legend(fontsize=10, loc='best')
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('gear4_initialization.png', dpi=150, bbox_inches='tight')
print("\nГрафик сохранен: gear4_initialization.png")
plt.show()


# ===== ГРАФИК 1: Решение методом Гира 1-го порядка для разных шагов =====
fig1 = plt.figure(figsize=(16, 5))
fig1.suptitle(f'Д) Метод Гира 1-го порядка: h = {h_e}, {h_e*2}',
              fontsize=13, fontweight='bold')

for idx, h in enumerate(h_values_d):
    res = results_d[h]
    t = res['t']
    Y = res['Y']
    y = Y[:, 0]
    z = Y[:, 1]

    # Компонента y
    ax1 = plt.subplot(2, 2, idx * 2 + 1)
    ax1.plot(t_exact_fine, Y_exact_fine[:, 0], 'k-', linewidth=2, label='Точное y(t)')
    ax1.plot(t, y, 'r-o', linewidth=2, markersize=5, label=f'Численное (h={h})')
    ax1.set_xlabel('t', fontsize=11)
    ax1.set_ylabel('y(t)', fontsize=11)
    ax1.set_title(f'y(t), h = {h}', fontsize=12, fontweight='bold')
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)

    # Компонента z
    ax2 = plt.subplot(2, 2, idx * 2 + 2)
    ax2.plot(t_exact_fine, Y_exact_fine[:, 1], 'k-', linewidth=2, label='Точное z(t)')
    ax2.plot(t, z, 'b-s', linewidth=2, markersize=5, label=f'Численное (h={h})')
    ax2.set_xlabel('t', fontsize=11)
    ax2.set_ylabel('z(t)', fontsize=11)
    ax2.set_title(f'z(t), h = {h}', fontsize=12, fontweight='bold')
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# ===== ГРАФИК 2: Решение методом Гира 4-го порядка =====
fig2 = plt.figure(figsize=(14, 5))
fig2.suptitle(f'Е) Метод Гира 4-го порядка: h = {h_e}',
              fontsize=13, fontweight='bold')

res_e = results_e
t_e = res_e['t']
Y_e = res_e['Y']

# y(t)
ax1 = plt.subplot(1, 2, 1)
ax1.plot(t_exact_fine, Y_exact_fine[:, 0], 'k-', linewidth=2.5, label='Точное y(t)')
ax1.plot(t_e, Y_e[:, 0], 'r-^', linewidth=2, markersize=6, label=f'Гира-4 (h={h_e})')
ax1.set_xlabel('t', fontsize=11)
ax1.set_ylabel('y(t)', fontsize=11)
ax1.set_title('Компонента y(t)', fontsize=12, fontweight='bold')
ax1.legend(fontsize=10)
ax1.grid(True, alpha=0.3)

# z(t)
ax2 = plt.subplot(1, 2, 2)
ax2.plot(t_exact_fine, Y_exact_fine[:, 1], 'k-', linewidth=2.5, label='Точное z(t)')
ax2.plot(t_e, Y_e[:, 1], 'b-^', linewidth=2, markersize=6, label=f'Гира-4 (h={h_e})')
ax2.set_xlabel('t', fontsize=11)
ax2.set_ylabel('z(t)', fontsize=11)
ax2.set_title('Компонента z(t)', fontsize=12, fontweight='bold')
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# ===== ГРАФИК 3: Анализ погрешности для Гира 1-го порядка =====
fig3 = plt.figure(figsize=(18, 5))
fig3.suptitle('АНАЛИЗ ПОГРЕШНОСТИ: Метод Гира 1-го порядка',
              fontsize=14, fontweight='bold')

# НОРМА ПОГРЕШНОСТИ
ax1 = plt.subplot(1, 3, 1)
for h in h_values_d:
    res = results_d[h]
    t = res['t']
    Y = res['Y']
    Y_exact_interp = np.array([exact_solution(ti) for ti in t])
    error_norm = np.linalg.norm(Y - Y_exact_interp, axis=1)
    ax1.semilogy(t, error_norm, '-o', linewidth=2, markersize=5, label=f'h = {h}')

ax1.set_xlabel('t', fontsize=11)
ax1.set_ylabel('||Y - Y_точное||', fontsize=11)
ax1.set_title('Евклидова норма погрешности', fontsize=12, fontweight='bold')
ax1.legend(fontsize=10)
ax1.grid(True, alpha=0.3, which='both')

# АБСОЛЮТНАЯ ПОГРЕШНОСТЬ
ax2 = plt.subplot(1, 3, 2)
for h in h_values_d:
    res = results_d[h]
    t = res['t']
    Y = res['Y']
    Y_exact_interp = np.array([exact_solution(ti) for ti in t])
    abs_error_y = np.abs(Y[:, 0] - Y_exact_interp[:, 0])
    abs_error_z = np.abs(Y[:, 1] - Y_exact_interp[:, 1])
    max_error = np.maximum(abs_error_y, abs_error_z)
    ax2.semilogy(t, max_error, '-o', linewidth=2, markersize=5, label=f'h = {h}')

ax2.set_xlabel('t', fontsize=11)
ax2.set_ylabel('max(|Δy|, |Δz|)', fontsize=11)
ax2.set_title('Абсолютная погрешность (макс по компонентам)', fontsize=12, fontweight='bold')
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.3, which='both')

# ОТНОСИТЕЛЬНАЯ ПОГРЕШНОСТЬ
ax3 = plt.subplot(1, 3, 3)
for h in h_values_d:
    res = results_d[h]
    t = res['t']
    Y = res['Y']
    Y_exact_interp = np.array([exact_solution(ti) for ti in t])
    rel_error_y = np.abs((Y[:, 0] - Y_exact_interp[:, 0]) / (np.abs(Y_exact_interp[:, 0]) + 1e-14))
    rel_error_z = np.abs((Y[:, 1] - Y_exact_interp[:, 1]) / (np.abs(Y_exact_interp[:, 1]) + 1e-14))
    max_rel_error = np.maximum(rel_error_y, rel_error_z)
    max_rel_error[max_rel_error < 1e-16] = 1e-16
    ax3.semilogy(t, max_rel_error, '-o', linewidth=2, markersize=5, label=f'h = {h}')

ax3.set_xlabel('t', fontsize=11)
ax3.set_ylabel('max(|Δy|/|y|, |Δz|/|z|)', fontsize=11)
ax3.set_title('Относительная погрешность', fontsize=12, fontweight='bold')
ax3.legend(fontsize=10)
ax3.grid(True, alpha=0.3, which='both')

plt.tight_layout()
plt.show()

# ===== ГРАФИК 4: Анализ погрешности для Гира 4-го порядка =====
fig4 = plt.figure(figsize=(18, 5))
fig4.suptitle('АНАЛИЗ ПОГРЕШНОСТИ: Метод Гира 4-го порядка',
              fontsize=14, fontweight='bold')

res_e = results_e
t_e = res_e['t']
Y_e = res_e['Y']
Y_exact_e = np.array([exact_solution(t) for t in t_e])

# НОРМА
ax1 = plt.subplot(1, 3, 1)
error_norm_e = np.linalg.norm(Y_e - Y_exact_e, axis=1)
ax1.semilogy(t_e, error_norm_e, '-^', linewidth=2, markersize=6, color='darkgreen', label='Гира-4')
ax1.set_xlabel('t', fontsize=11)
ax1.set_ylabel('||Y - Y_точное||', fontsize=11)
ax1.set_title('Евклидова норма погрешности', fontsize=12, fontweight='bold')
ax1.legend(fontsize=10)
ax1.grid(True, alpha=0.3, which='both')

# АБСОЛЮТНАЯ
ax2 = plt.subplot(1, 3, 2)
abs_error_e = np.abs(Y_e - Y_exact_e)
max_error_e = np.max(abs_error_e, axis=1)
ax2.semilogy(t_e, max_error_e, '-^', linewidth=2, markersize=6, color='darkgreen', label='Гира-4')
ax2.set_xlabel('t', fontsize=11)
ax2.set_ylabel('max(|Δy|, |Δz|)', fontsize=11)
ax2.set_title('Абсолютная погрешность', fontsize=12, fontweight='bold')
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.3, which='both')

# ОТНОСИТЕЛЬНАЯ
ax3 = plt.subplot(1, 3, 3)
rel_error_e = np.abs(abs_error_e / (np.abs(Y_exact_e) + 1e-14))
max_rel_error_e = np.max(rel_error_e, axis=1)
max_rel_error_e[max_rel_error_e < 1e-16] = 1e-16
ax3.semilogy(t_e, max_rel_error_e, '-^', linewidth=2, markersize=6, color='darkgreen', label='Гира-4')
ax3.set_xlabel('t', fontsize=11)
ax3.set_ylabel('max(|Δy|/|y|, |Δz|/|z|)', fontsize=11)
ax3.set_title('Относительная погрешность', fontsize=12, fontweight='bold')
ax3.legend(fontsize=10)
ax3.grid(True, alpha=0.3, which='both')

plt.tight_layout()
plt.show()

# ===== ГРАФИК 5: Сравнение Гира 1-го и 4-го порядков =====
fig5 = plt.figure(figsize=(14, 10))
fig5.suptitle(f'СРАВНЕНИЕ: Гира 1-го (h={h_e}) vs Гира 4-го (h={h_e})',
              fontsize=14, fontweight='bold')

# y(t)
ax1 = plt.subplot(2, 2, 1)
ax1.plot(t_exact_fine, Y_exact_fine[:, 0], 'k-', linewidth=2.5, label='Точное y(t)')
ax1.plot(results_d[h_e]['t'], results_d[h_e]['Y'][:, 0], 'r-o', linewidth=2,
         markersize=5, label='Гира-1')
ax1.plot(t_e, Y_e[:, 0], 'g-^', linewidth=2, markersize=5, label='Гира-4')
ax1.set_xlabel('t', fontsize=11)
ax1.set_ylabel('y(t)', fontsize=11)
ax1.set_title('Компонента y(t)', fontsize=12)
ax1.legend(fontsize=10)
ax1.grid(True, alpha=0.3)

# z(t)
ax2 = plt.subplot(2, 2, 2)
ax2.plot(t_exact_fine, Y_exact_fine[:, 1], 'k-', linewidth=2.5, label='Точное z(t)')
ax2.plot(results_d[h_e]['t'], results_d[h_e]['Y'][:, 1], 'r-s', linewidth=2,
         markersize=5, label='Гира-1')
ax2.plot(t_e, Y_e[:, 1], 'b-^', linewidth=2, markersize=5, label='Гира-4')
ax2.set_xlabel('t', fontsize=11)
ax2.set_ylabel('z(t)', fontsize=11)
ax2.set_title('Компонента z(t)', fontsize=12)
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.3)

# Погрешность y(t)
ax3 = plt.subplot(2, 2, 3)
Y_exact_d = np.array([exact_solution(t) for t in results_d[h_e]['t']])
error_y_1 = np.abs(results_d[h_e]['Y'][:, 0] - Y_exact_d[:, 0])
error_y_4 = np.abs(Y_e[:, 0] - Y_exact_e[:, 0])
ax3.semilogy(results_d[h_e]['t'], error_y_1, '-o', linewidth=2, markersize=5, label='Гира-1')
ax3.semilogy(t_e, error_y_4, '-^', linewidth=2, markersize=5, label='Гира-4')
ax3.set_xlabel('t', fontsize=11)
ax3.set_ylabel('|Δy|', fontsize=11)
ax3.set_title('Абсолютная погрешность y(t)', fontsize=12)
ax3.legend(fontsize=10)
ax3.grid(True, alpha=0.3, which='both')

# Погрешность z(t)
ax4 = plt.subplot(2, 2, 4)
error_z_1 = np.abs(results_d[h_e]['Y'][:, 1] - Y_exact_d[:, 1])
error_z_4 = np.abs(Y_e[:, 1] - Y_exact_e[:, 1])
ax4.semilogy(results_d[h_e]['t'], error_z_1, '-o', linewidth=2, markersize=5, label='Гира-1')
ax4.semilogy(t_e, error_z_4, '-^', linewidth=2, markersize=5, label='Гира-4')
ax4.set_xlabel('t', fontsize=11)
ax4.set_ylabel('|Δz|', fontsize=11)
ax4.set_title('Абсолютная погрешность z(t)', fontsize=12)
ax4.legend(fontsize=10)
ax4.grid(True, alpha=0.3, which='both')

plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 6))

colors = ['blue', 'orange', 'green']
labels = ['integration_order=1', 'integration_order=2', 'integration_order=3']

for i in range(1, 4):
    data = results_star_gear[i]
    plt.plot(data['t'], data['Y'][:, 0], 'o-', color=colors[i-1],
             label=f'Gear4, {labels[i-1]}', markersize=4, alpha=0.8)

# Если есть точное решение, добавить:
# plt.plot(t_exact, y_exact, 'k--', linewidth=2, label='Точное решение')

plt.xlabel('t', fontsize=12)
plt.ylabel('y(t)', fontsize=12)
plt.title('Метод Гира 4-го порядка с разным порядком интегрирования', fontsize=14)
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()


h_e = 0.001

results_star_gear = {}
for i in range(1, 4):
    gear_e = GearMethod(order=4, integration_method = GearMethod, integration_order =i)
    t_e, y_e = gear_e.solve(f_system, t0, t_end, Y0, h_e)
    results_star_gear[i] = {
        't': np.array(t_e),
        'Y': np.array(y_e),
        'method': gear_e,
        'order': 4
    }
    print(y_e)



fig, axes = plt.subplots(1, 2, figsize=(15, 6))

colors = {1: 'blue', 2: 'green', 3: 'red'}
markers = {1: 'o', 2: 's', 3: '^'}
labels = {1: 'Гир-1 (одношаговый) (начальные)', 2: 'Гир-2 (двухшаговый) (начальные)', 3: 'Гир-3 (трехшаговый) (начальные)'}

# График 1: Первая компонента y₁(t)
ax1 = axes[0]
for i in range(1, 4):
    t_vals = results_star_gear[i]['t']
    Y_vals = results_star_gear[i]['Y']

    ax1.plot(t_vals[:4], Y_vals[:4, 0], markers[i], markersize=12,
             color=colors[i], markeredgecolor='black', markeredgewidth=1.5,
             label=f'{labels[i]} ', zorder=10)

    ax1.plot(t_vals, Y_vals[:, 0], '-', linewidth=2.5,
             color=colors[i], alpha=0.6, zorder=5)

ax1.set_xlabel('Время t', fontsize=13, fontweight='bold')
ax1.set_ylabel('$y_1(t)$', fontsize=13, fontweight='bold')
ax1.set_title('Первая компонента: Сравнение инициализаций',
              fontsize=14, fontweight='bold')
ax1.legend(fontsize=10, loc='best')
ax1.grid(True, alpha=0.3)

# График 2: Вторая компонента y₂(t)
ax2 = axes[1]
for i in range(1, 4):
    t_vals = results_star_gear[i]['t']
    Y_vals = results_star_gear[i]['Y']

    # Начальные точки
    ax2.plot(t_vals[:4], Y_vals[:4, 1], markers[i], markersize=12,
             color=colors[i], markeredgecolor='black', markeredgewidth=1.5,
             label=f'{labels[i]} (начальные)', zorder=10)

    # Полное решение
    ax2.plot(t_vals, Y_vals[:, 1], '-', linewidth=2.5,
             color=colors[i], alpha=0.6, zorder=5)

ax2.set_xlabel('Время t', fontsize=13, fontweight='bold')
ax2.set_ylabel('$y_2(t)$', fontsize=13, fontweight='bold')
ax2.set_title('Вторая компонента: Сравнение инициализаций',
              fontsize=14, fontweight='bold')
ax2.legend(fontsize=10, loc='best')
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('gear4_initialization.png', dpi=150, bbox_inches='tight')
print("\nГрафик сохранен: gear4_initialization.png")
plt.show()


fig, axes = plt.subplots(1, 2, figsize=(15, 6))

colors = {1: 'blue', 2: 'green', 3: 'red'}
#labels = {1: 'Гир-1 (одношаговый)', 2: 'Гир-2 (двухшаговый)', 3: 'Гир-3 (трехшаговый)'}


ax1 = axes[0]
for i in range(1, 4):
    t_vals = results_star_gear[i]['t']
    Y_vals = results_star_gear[i]['Y']

    Y_exact = np.array([exact_solution(t) for t in t_vals])
    err_y1 = np.abs(Y_vals[:, 0] - Y_exact[:, 0])

    ax1.plot(t_vals, err_y1, color=colors[i], label=labels[i])

ax1.set_xlabel('t', fontsize=13, fontweight='bold')
ax1.set_ylabel('|error y₁|', fontsize=13, fontweight='bold')
ax1.set_title('Ошибка первой компоненты', fontsize=14, fontweight='bold')
ax1.grid(True, alpha=0.3)
ax1.legend(fontsize=10, loc='best')

# Ошибка второй компоненты
ax2 = axes[1]
for i in range(1, 4):
    t_vals = results_star_gear[i]['t']
    Y_vals = results_star_gear[i]['Y']

    Y_exact = np.array([exact_solution(t) for t in t_vals])
    err_y2 = np.abs(Y_vals[:, 1] - Y_exact[:, 1])

    ax2.plot(t_vals, err_y2, color=colors[i], label=labels[i])

ax2.set_xlabel('t', fontsize=13, fontweight='bold')
ax2.set_ylabel('|error y₂|', fontsize=13, fontweight='bold')
ax2.set_title('Ошибка второй компоненты', fontsize=14, fontweight='bold')
ax2.grid(True, alpha=0.3)
ax2.legend(fontsize=10, loc='best')
plt.show()
