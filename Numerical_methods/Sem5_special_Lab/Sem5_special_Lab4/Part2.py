import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append ("C:\\Users\\6anna\\PycharmProjects\\Numerical_methods")
from Volterra import Volterra
from Trapezoid import Trapezoid
from RungeKuttaMethod import RungeKuttaMethod

def exact(t):   # 51 номер
    return 4 * np.cos(2*t) - np.cos(t)

kernel = lambda t, s: s - t
f = lambda t: 3 * np.cos(t)

a, b = 0, 3
tau = 0.2
n = int((b - a) / tau) + 1
lambda_param = 4

volt = Volterra(lam=lambda_param, integration_method=Trapezoid())
t_vals1, x_vals1 = volt.solve(kernel, f, a, b, n=n)

# Надо свести к ОДУ
def system_ODY(t, y):
    dxdt = y[1]
    dydt = -4*y[0] - 3* np.cos(t)
    return np.array([dxdt, dydt])

y0 = [3, 0]
h = tau
rk = RungeKuttaMethod(order = 4)
t_vals2, y_vals2 = rk.solve(system_ODY, a, b, y0, h)
x_vals2 = y_vals2[:, 0]

t_smooth = np.linspace(0, 5, 300)
x_exact = [exact(t) for t in t_smooth]

plt.figure(figsize=(13, 7))
plt.plot(t_smooth, x_exact, 'k-', linewidth=3, label='Точное')
plt.plot(t_vals1, x_vals1, 'ro-', markersize=5, linewidth=2, label='Трапеции', alpha=0.7)
plt.plot(t_vals2, x_vals2, 'bs-', markersize=5, linewidth=2, label='Runge-Kutta по ОДУ', alpha=0.7)
plt.xlabel('t', fontsize=13, fontweight='bold')
plt.ylabel('x(t)', fontsize=13, fontweight='bold')
plt.title('Сравнение решений: аналитическое, Трапеции, Runge-Kutta', fontsize=14, fontweight='bold')
plt.legend(fontsize=12)
plt.grid(True, alpha=0.3)
plt.show()



