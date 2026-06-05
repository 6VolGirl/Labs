
import numpy as np
import sys
import os
import matplotlib.pyplot as plt
sys.path.append ("C:\\Users\\6anna\PycharmProjects\\Labs\\Numerical_methods\\Numerical_methods_classes\\Ordinary_Differential_Equations(ODE)")
from AdamsBashforthMoulton import AdamsBashforthMoulton
from EulerExplicit import EulerExplicit
from EulerImplicit import EulerImplicit
from ImprovedEuler import ImprovedEuler
from GearMethod import GearMethod

def f(t,u):
    return t*np.sqrt(u)

def exact_sol(t):
    return (t**2 + 4)**2 /16

u0 = 1
t0 = 0
t_end = 0.5

hs = [0.001, 0.005, 0.1]
results = {}

for h in hs:
    ABM = AdamsBashforthMoulton(order=3)
    t_ABM, y_ABM = ABM.solve(f, t0, t_end, u0, h)
    err_ABM = ABM.compute_error(exact_sol, t_ABM, y_ABM)

    gear = GearMethod(order=3)
    t_gear, y_gear = gear.solve(f, t0, t_end, u0, h)
    err_gear = gear.compute_error(exact_sol, t_gear, y_gear)

    results[h] = {
        'ABM': {'t': t_ABM, 'y': y_ABM, 'err': err_ABM},
        'Gear': {'t': t_gear, 'y': y_gear, 'err': err_gear}
    }

t_fine = np.linspace(t0, t_end, 1000)
u_exact = exact_sol(t_fine)

# =============================================================================
# ПОСТРОЕНИЕ ГРАФИКОВ
# =============================================================================
#График 1: U(t) точное и численное метод АВМ
plt.figure(figsize=(8, 5))
plt.plot(t_fine, u_exact, 'k-', linewidth=2.5, label='Точное решение')
plt.plot(t_ABM, y_ABM, 'ro-', linewidth=1.5, markersize=4, label='ABM3 (численное)')
plt.xlabel('t', fontsize=12)
plt.ylabel('U(t)', fontsize=12)
plt.title('U\' = t√U, U(0)=1: Точное vs ABM3', fontsize=13, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.show()

#График 2: U(t) точное и численное метод Гира
plt.figure(figsize=(10, 6))
plt.plot(t_fine, u_exact, 'b-', linewidth=2.5, label='Точное решение', zorder=3)
plt.plot(t_gear, y_gear, 'ro--', linewidth=1.5, markersize=7, label='Численное решение (Gear)', alpha=0.8, zorder=2)
plt.xlabel('t', fontsize=12, fontweight='bold')
plt.ylabel('u(t)', fontsize=12, fontweight='bold')
plt.title('ОДУ: du/dt = t√u, u(0) = 1\nТочное vs Численное решение (Gear)',
          fontsize=13, fontweight='bold')
plt.legend(fontsize=11, loc='best')
plt.grid(True, alpha=0.3, linestyle='--')
plt.tight_layout()

# График 3:  ABM3 (решение + ошибки)
fig1, (ax_abm_sol, ax_abm_abs, ax_abm_rel) = plt.subplots(3, 1, figsize=(8, 10), sharex=False)
fig1.suptitle('ABM3: решение и погрешности', fontsize=14)

# Решение ABM3
ax_abm_sol.plot(t_fine, u_exact, color='k', linewidth=3, label='Точное решение')
for h in hs:
    ta, ya = results[h]['ABM']['t'], results[h]['ABM']['y']
    ax_abm_sol.plot(
        ta, ya,
        linestyle='-',
        marker=('o' if h==0.001 else ('s' if h==0.005 else 'D')),
        markersize=4,
        color=('#1f77b4' if h==0.001 else ('#ff7f0e' if h==0.005 else '#2ca02c')),
        alpha=0.9,
        label=f'ABM3, h={h}'
    )
ax_abm_sol.set_ylabel('u(t)')
ax_abm_sol.grid(True, alpha=0.3)
ax_abm_sol.legend(fontsize=9)

# Абсолютная погрешность ABM3
for h in hs:
    ta, ya = results[h]['ABM']['t'], results[h]['ABM']['y']
    ua = exact_sol(ta)
    ax_abm_abs.plot(
        ta, np.abs(ya-ua),
        linestyle='-',
        color=('#1f77b4' if h==0.001 else ('#ff7f0e' if h==0.005 else '#2ca02c')),
        label=f'h={h}'
    )
ax_abm_abs.set_yscale('log')
ax_abm_abs.set_ylabel('|u_num - u_exact|')
ax_abm_abs.grid(True, which='both', alpha=0.3)
ax_abm_abs.legend(title='ABM3', fontsize=9)

# Относительная погрешность ABM3
for h in hs:
    ta, ya = results[h]['ABM']['t'], results[h]['ABM']['y']
    ua = exact_sol(ta)
    ax_abm_rel.plot(
        ta, np.abs((ya-ua)/ua),
        linestyle='-',
        color=('#1f77b4' if h==0.001 else ('#ff7f0e' if h==0.005 else '#2ca02c')),
        label=f'h={h}'
    )
ax_abm_rel.set_yscale('log')
ax_abm_rel.set_xlabel('t')
ax_abm_rel.set_ylabel('Относительная ошибка')
ax_abm_rel.grid(True, which='both', alpha=0.3)
ax_abm_rel.legend(title='ABM3', fontsize=9)

plt.tight_layout(rect=[0, 0, 1, 0.96])

# График 4: Gear3 (решение + ошибки)
fig2, (ax_g_sol, ax_g_abs, ax_g_rel) = plt.subplots(3, 1, figsize=(8, 10), sharex=False)
fig2.suptitle('Gear3: решение и погрешности', fontsize=14)

# Решение Gear3
ax_g_sol.plot(t_fine, u_exact, color='k', linewidth=3, label='Точное решение')
for h in hs:
    tg, yg = results[h]['Gear']['t'], results[h]['Gear']['y']
    ax_g_sol.plot(
        tg, yg,
        linestyle='--',
        marker=('o' if h==0.001 else ('s' if h==0.005 else 'D')),
        markersize=4,
        color=('#1f77b4' if h==0.001 else ('#ff7f0e' if h==0.005 else '#2ca02c')),
        alpha=0.9,
        label=f'Gear3, h={h}'
    )
ax_g_sol.set_ylabel('u(t)')
ax_g_sol.grid(True, alpha=0.3)
ax_g_sol.legend(fontsize=9)

# Абсолютная погрешность Gear3
for h in hs:
    tg, yg = results[h]['Gear']['t'], results[h]['Gear']['y']
    ug = exact_sol(tg)
    ax_g_abs.plot(
        tg, np.abs(yg-ug),
        linestyle='--',
        color=('#1f77b4' if h==0.001 else ('#ff7f0e' if h==0.005 else '#2ca02c')),
        label=f'h={h}'
    )
ax_g_abs.set_yscale('log')
ax_g_abs.set_ylabel('|u_num - u_exact|')
ax_g_abs.grid(True, which='both', alpha=0.3)
ax_g_abs.legend(title='Gear3', fontsize=9)

# Относительная погрешность Gear3
for h in hs:
    tg, yg = results[h]['Gear']['t'], results[h]['Gear']['y']
    ug = exact_sol(tg)
    ax_g_rel.plot(
        tg, np.abs((yg-ug)/ug),
        linestyle='--',
        color=('#1f77b4' if h==0.001 else ('#ff7f0e' if h==0.005 else '#2ca02c')),
        label=f'h={h}'
    )
ax_g_rel.set_yscale('log')
ax_g_rel.set_xlabel('t')
ax_g_rel.set_ylabel('Относительная ошибка')
ax_g_rel.grid(True, which='both', alpha=0.3)
ax_g_rel.legend(title='Gear3', fontsize=9)

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()

# =============================================================================

# Количество итераций коррекции
max_iterations_list = [1, 2, 4, 8]
results_iterations = {}

for max_iter in max_iterations_list:
    ABM = AdamsBashforthMoulton(order=3, max_iterations=max_iter)
    t_ABM, y_ABM = ABM.solve(f, t0, t_end, u0, h)
    err = ABM.compute_error(exact_sol, t_ABM, y_ABM)

    stats = ABM.get_iteration_statistics()

    results_iterations[max_iter] = {
        't': t_ABM,
        'y': y_ABM,
        'error': err,
        'stats': stats,
        'iterations_used': ABM.iterations_used
    }


# =============================================================================
# график 5: Зависимость ошибки от числа итераций (2×2)

selected_iters = [1, 2, 4, 8]
colors = plt.cm.coolwarm(np.linspace(0, 1, len(selected_iters)))
labels = [f'Коррекция: {k}' for k in selected_iters]

t_fine = np.linspace(t0, t_end, 1000)
u_exact_fine = exact_sol(t_fine)

# График 1: решения при разном числе итераций коррекции
plt.figure(figsize=(8,5))
plt.plot(t_fine, u_exact_fine, 'k-', lw=2.5, label='Точное решение', zorder=10)
for i, k in enumerate(selected_iters):
    t_vals = results_iterations[k]['t']
    y_vals = results_iterations[k]['y']
    plt.plot(t_vals, y_vals,
        marker='o', markersize=4, color=colors[i], linewidth=1.3, alpha=0.9, label=labels[i])
plt.xlabel('t')
plt.ylabel('u(t)')
plt.title('ABM3: Решения при разном числе итераций коррекции')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# График 2: относительная погрешность в log масштабе
plt.figure(figsize=(8,5))
for i, k in enumerate(selected_iters):
    t_vals = results_iterations[k]['t']
    ua = exact_sol(t_vals)
    y_vals = results_iterations[k]['y']
    rel_err = np.abs((y_vals - ua) / ua)
    plt.semilogy(t_vals, rel_err, marker='o', markersize=4, color=colors[i],
        linewidth=1.3, alpha=0.9, label=labels[i])
plt.xlabel('t')
plt.ylabel('Относительная погрешность')
plt.title('ABM3: Относительная погрешность при разном числе коррекций')
plt.legend()
plt.grid(True, which='both', alpha=0.3)
plt.tight_layout()
plt.show()


