import numpy as np
import sys

from Task1 import t_rks
sys.path.append ("C:\\Users\\6anna\\PycharmProjects\\Labs\\Numerical_methods\\Numerical_methods_classes\\Ordinary_Differential_Equations(ODE)")
import matplotlib.pyplot as plt
from EulerExplicit import EulerExplicit
from RungeKuttaMethod import RungeKuttaMethod

plt.plot()

plt.show()

def lorenz_rhs(t, y, sigma=10, b=8/3, r=28):
    x, y_, z = y
    dxdt = sigma * (y_ - x)
    dydt = -x*z + r*x - y_
    dzdt = x*y_ - b*z
    return np.array([dxdt, dydt, dzdt])

y0 = np.array([0.0, 1.0, 0.0])
t0 = 0
t_end = 30
h = 0.01

sigma = 100
b = 8/3
r = 25
r_values = [10, 25, 40]
colors = ["blue", "red", "green"]
labels = [f"r={r}" for r in r_values]

fig = plt.figure(figsize=(10, 16))

for idx, r in enumerate(r_values):
    ax = fig.add_subplot(3, 1, idx+1, projection='3d')
    def rhs(t, y):
        return lorenz_rhs(t, y, sigma=sigma, b=b, r=r)
    solver = RungeKuttaMethod(order=4)
    t, y = solver.solve(rhs, t0, t_end, y0, h)
    ax.plot(y[:, 0], y[:, 1], y[:, 2], color=colors[idx], alpha=0.85)
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.set_zlabel("$z$")
    ax.set_title(labels[idx], fontsize=14)
    ax.grid(False)
    ax.set_box_aspect([1,1,0.7])  # больше вытянут по z

plt.tight_layout()
plt.show()

rk_orders = [1, 4]
rk_labels = ["RK1 (Эйлер)", "RK2", "RK3", "RK4"]
colors = ["blue", "orange", "green", "red"]

t_rks = []
y_rks = []

for order in rk_orders:
    rk = RungeKuttaMethod(order=order)

    def rhs (t, y):
        return lorenz_rhs(t, y, sigma=sigma, b=b, r=r)

    t, y = rk.solve(rhs, t0, t_end, y0, h)
    t_rks.append(t)
    y_rks.append(y)


fig, axes = plt.subplots(3, 1, figsize=(12, 14), sharex=True)

components = [0, 1, 2]
compnames = ["x(t)", "y(t)", "z(t)"]

for comp_idx, ax in enumerate(axes):
    for idx, order in enumerate(rk_orders):
        ax.plot(t_rks[idx], y_rks[idx][:,comp_idx],
                label=rk_labels[idx], color=colors[idx], linewidth=1.6, alpha=0.85)
    ax.set_ylabel(compnames[comp_idx], fontsize=14)
    ax.legend(fontsize=13)
    ax.grid(True)
axes[2].set_xlabel('t', fontsize=14)
fig.suptitle("Временные зависимости компонент Лоренца (r=25) для разных порядков Рунге-Кутты", fontsize=16)
plt.tight_layout(rect=[0,0,1,0.98])
plt.show()
print("done")
# rk_orders = [1, 4]
# order_labels = ["RK1 (Эйлер)", "RK4"]
# h_values = [0.05, 0.01, 0.005]
# r = 25
#
# fig, axes = plt.subplots(len(h_values), 1, figsize=(11, 2.7*len(h_values)), sharex=False)
#
# for idx, h in enumerate(h_values):
#     ax = axes[idx]
#     for ord_ind, order in enumerate(rk_orders):
#         solver = RungeKuttaMethod(order=order)
#         rhs = lambda t, y: lorenz_rhs(t, y, sigma=10, b=8/3, r=r)
#         t, y = solver.solve(rhs, t0, t_end, y0, h)
#         ax.plot(t, y[:, 0], label=order_labels[ord_ind], linewidth=1.8 if order==4 else 1.2, alpha=0.87)
#         if np.any(np.isnan(y[:, 0])) or np.any(np.abs(y[:, 0]) > 1e6):
#             ax.text(t[-1]*0.8, 0, " ", color='red', fontsize=12, va='center')
#
#     ax.set_ylabel('x(t)', fontsize=13)
#     ax.set_title(f"x(t): шаг интегрирования h={h}", fontsize=14)
#     ax.grid(True)
#     ax.legend()
#
# axes[-1].set_xlabel('t', fontsize=13)
# plt.suptitle(f"Влияние шага и порядка Рунге-Кутты на поведение Лоренца (r={r})", fontsize=16)
# plt.tight_layout(rect=[0,0,1,0.96])
# plt.show()
#
# fig, axes = plt.subplots(len(h_values), 1, figsize=(11, 2.7*len(h_values)), sharex=False)
#
# for idx, h in enumerate(h_values):
#     ax = axes[idx]
#     for ord_ind, order in enumerate(rk_orders):
#         solver = RungeKuttaMethod(order=order)
#         rhs = lambda t, y: lorenz_rhs(t, y, sigma=10, b=8/3, r=r)
#         t, y = solver.solve(rhs, t0, t_end, y0, h)
#         ax.plot(t, y[:, 1], label=order_labels[ord_ind],
#                 linewidth=1.8 if order == 4 else 1.2, alpha=0.87)
#         if np.any(np.isnan(y[:, 1])) or np.any(np.abs(y[:, 1]) > 1e6):
#             ax.text(t[-1]*0.8, 0, " ", color='red', fontsize=12, va='center')
#
#     ax.set_ylabel('y(t)', fontsize=13)
#     ax.set_title(f"y(t): шаг интегрирования h={h}", fontsize=14)
#     ax.grid(True)
#     ax.legend()
#
# axes[-1].set_xlabel('t', fontsize=13)
# plt.suptitle(f"Влияние шага и порядка Рунге-Кутты на y(t) для Лоренца (r={r})", fontsize=16)
# plt.tight_layout(rect=[0,0,1,0.96])
# plt.show()
#
#
# fig, axes = plt.subplots(len(h_values), 1, figsize=(11, 2.7*len(h_values)), sharex=False)
#
# for idx, h in enumerate(h_values):
#     ax = axes[idx]
#     for ord_ind, order in enumerate(rk_orders):
#         solver = RungeKuttaMethod(order=order)
#         rhs = lambda t, y: lorenz_rhs(t, y, sigma=10, b=8/3, r=r)
#         t, y = solver.solve(rhs, t0, t_end, y0, h)
#         ax.plot(t, y[:, 2], label=order_labels[ord_ind],
#                 linewidth=1.8 if order == 4 else 1.2, alpha=0.87)
#         if np.any(np.isnan(y[:, 2])) or np.any(np.abs(y[:, 2]) > 1e6):
#             ax.text(t[-1]*0.8, 0, " ", color='red', fontsize=12, va='center')
#
#     ax.set_ylabel('z(t)', fontsize=13)
#     ax.set_title(f"z(t): шаг интегрирования h={h}", fontsize=14)
#     ax.grid(True)
#     ax.legend()
#
# axes[-1].set_xlabel('t', fontsize=13)
# plt.suptitle(f"Влияние шага и порядка Рунге-Кутты на z(t) для Лоренца (r={r})", fontsize=16)
# plt.tight_layout(rect=[0,0,1,0.96])
# plt.show()