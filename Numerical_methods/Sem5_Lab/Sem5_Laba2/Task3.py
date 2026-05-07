import numpy as np
import matplotlib.pyplot as plt
#from Task1 import newton_method




# Параметры сетки
x = np.arange(-2, 2.004, 0.004)
y = np.arange(-2, 2.004, 0.004)
X, Y = np.meshgrid(x, y)
Z0 = X + 1j * Y    # сетка комплексных чисел


def f(z):return z**3 - 1
def df(z):return 3 * z**2

roots = np.array([1, np.exp(2j*np.pi/3), np.exp(-2j*np.pi/3)])


#def modificate_newton_method(f, df, x, roots, max_iter=30, tol=1e-8):
#    z = x
#    for k in range(max_iter):
#        if abs(df(z)) < 1e-12:
#            break
#        z_new = z - f(z) / df(z)
#        if abs(z_new - z) < tol:
#            z = z_new
#            break
#        z = z_new
#    distances = [abs(z - r) for r in roots]
#    return int(distances.index(min(distances)))
#
#
#result = np.zeros(Z0.shape, dtype=int)
#total = Z0.shape[0] * Z0.shape[1]
#count = 0
#
#for i in range(Z0.shape[0]):
#    for j in range(Z0.shape[1]):
#        z0 = Z0[i, j]
#        idx = modificate_newton_method(f, df, z0, roots, max_iter=30)
#        result[i, j] = idx
#        count += 1
#        if count % 100000 == 0:
#            print(f"Обработано {count}/{total} точек")
#


Z = Z0.copy()
for _ in range(30):
    Z -= f(Z) / df(Z)

result = np.zeros(Z.shape, dtype=int)
for i, r in enumerate(roots):
    result[np.abs(Z - r) < 1e-3] = i


plt.figure(figsize=(8, 8))
plt.imshow(result, extent=(-2, 2, -2, 2), origin='lower', cmap='brg')
plt.title("Области притяжения метода Ньютона для f(z) = z³ - 1")
plt.xlabel("Re(z)")
plt.ylabel("Im(z)")
plt.colorbar(label="Номер корня")
plt.show()






