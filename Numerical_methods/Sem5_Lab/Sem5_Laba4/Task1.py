import numpy as np
import sys
sys.path.append ("C:\\Users\\6anna\\PycharmProjects\\Labs\\Numerical_methods\\Numerical_methods_classes\\Ordinary_Differential_Equations(ODE)")
import matplotlib.pyplot as plt
from EulerExplicit import EulerExplicit
from RungeKuttaMethod import RungeKuttaMethod

def oscillator_rhs(t, y):
    omega = 1.0
    x, v = y
    dxdt = v
    dvdt = -omega**2 * x
    return np.array([dxdt, dvdt])

y0 = np.array([1.0, 0.0])
t0 = 0
t_end = 5 * np.pi
h = 0.05

def x_exact(t):
    return np.cos(t)

def v_exact(t):
    return -np.sin(t)

rk_orders = [1, 2, 3, 4]
rk_solvers = []
t_rks = []
y_rks = []
error = []

for order in rk_orders:
    rk = RungeKuttaMethod(order=order)
    t_rk, y_rk = rk.solve(oscillator_rhs, t0, t_end, y0, h)
    rk_solvers.append(rk)
    t_rks.append(t_rk)
    y_rks.append(y_rk)
    err = rk.compute_error(x_exact, t_rk, y_rk[:, 0])
    error.append(err['absolute'])

labels = ["RK1 (Эйлер)", "RK2", "RK3", "RK4"]
plt.figure(figsize=(14, 8))
for idx in range(4):
    plt.plot(t_rks[idx], y_rks[idx][:, 0], label=labels[idx])
plt.plot(t_rks[-1], x_exact(t_rks[-1]), 'k--', label="Аналитика", linewidth=2)
plt.xlabel('t')
plt.ylabel('x(t)')
plt.title('x(t) для методов Рунге-Кутты 1–4 порядка')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

plt.figure(figsize=(14, 8))
for idx in range(4):
    plt.plot(t_rks[idx], error[idx], label=labels[idx])
plt.yscale('log')
plt.xlabel('t')
plt.ylabel('Абсолютная ошибка x(t)')
plt.title('Погрешности x(t) для методов Рунге-Кутты 1–4 порядка')
plt.legend()
plt.grid(True, which='both')
plt.tight_layout()
plt.show()



rk4_steps = [0.2, 0.05, 0.01, 0.005]
t_rk4, y_rk4, err_rk4 = [], [], []
for h in rk4_steps:
    rk = RungeKuttaMethod(order=4)
    t, y = rk.solve(oscillator_rhs, t0, t_end, y0, h)
    t_rk4.append(t)
    y_rk4.append(y)
    err = rk.compute_error(x_exact, t, y[:,0])
    err_rk4.append(err['absolute'])

plt.figure(figsize=(14,8))
for idx, h in enumerate(rk4_steps):
    plt.plot(t_rk4[idx], y_rk4[idx][:,0], label=f"RK4, h={h}")
plt.plot(t_rk4[-1], x_exact(t_rk4[-1]), 'k--', label="Аналитика", linewidth=2)
plt.xlabel('t')
plt.ylabel('x(t)')
plt.title('Влияние шага интегрирования на x(t) для RK4')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()


plt.figure(figsize=(14,8))
for idx, h in enumerate(rk4_steps):
    plt.plot(t_rk4[idx], err_rk4[idx], label=f"RK4, h={h}")
plt.yscale('log')
plt.xlabel('t')
plt.ylabel('Абсолютная ошибка x(t)')
plt.title('Погрешность RK4 для разных шагов')
plt.legend()
plt.grid(True, which='both')
plt.tight_layout()
plt.show()