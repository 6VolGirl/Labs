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

def rhs(t, y):
    return lorenz_rhs(t, y, sigma=10, b=8/3, r=28)


rk1 = RungeKuttaMethod(order=4)
t1, y1 = rk1.solve(rhs, t0, t_end, y0, h=0.01)

rk2 = RungeKuttaMethod(order=4)
t2, y2 = rk2.solve_with_precision(rhs, t0, t_end, y0, target_error=1e-6)


fig, axes = plt.subplots(1, 2, figsize=(14, 5))
# График 1
ax = axes[0]
ax.plot(t1, y1[:, 0], 'b-', linewidth=2, label='h=0.01 (фиксированный)', alpha=0.7)
ax.plot(t2, y2[:, 0], 'r--', linewidth=1.5, label='target_error=1e-6', alpha=0.8)
ax.set_xlabel('t', fontsize=12)
ax.set_ylabel('x(t)', fontsize=12)
ax.set_title('Компонента x(t)', fontsize=13, fontweight='bold')
ax.grid(True, alpha=0.3)
ax.legend(fontsize=11)

# График 2: 3D траектория
ax = fig.add_subplot(1, 2, 2, projection='3d')
ax.plot(y2[:, 0], y2[:, 1], y2[:, 2], 'b-', linewidth=1.5, alpha=0.8)
ax.set_xlabel('x', fontsize=11)
ax.set_ylabel('y', fontsize=11)
ax.set_zlabel('z', fontsize=11)
ax.set_title('Аттрактор Лоренца', fontsize=13, fontweight='bold')

plt.tight_layout()
plt.show()

