from Task2 import SOR_method
import random
import numpy as np
import pyamg

def generate_matrix_for_jacobi(n, diag_min=5, off_diag_max=2):
    """
    Генерирует случайную диагонально-преобладающую матрицу n×n
    (с ненулевыми элементами только на главной, под- и наддиагонали) для метода Якоби
    """
    A = np.zeros((n, n))
    for i in range(n):
        sum_off = 0
        if i > 0:
            A[i, i - 1] = random.uniform(-off_diag_max, off_diag_max)
            sum_off += abs(A[i, i - 1])
        if i < n - 1:
            A[i, i + 1] = random.uniform(-off_diag_max, off_diag_max)
            sum_off += abs(A[i, i + 1])

        A[i, i] = random.uniform(diag_min, diag_min + 2)

        if A[i, i] <= sum_off:
            A[i, i] = sum_off + 0.1  # гарантия

    return A

#a, fi = pyamg.gallery.linear_elasticity((2, 2))
#A = a.toarray()
#b= [i for i in range(len(A))]

A = generate_matrix_for_jacobi(100, diag_min=5, off_diag_max=2)
b= [i for i in range(len(A))]

it =[]
omeg = []
min_it = 10000
optimal_omega = 0
for omega in np.arange(0.6, 1.9, 0.05):
    x, iter, error = SOR_method(A, b, None, omega, 100000, 1e-7)
    if min_it >= iter:
        min_it = iter
        optimal_omega = omega

    it.append(iter)
    omeg.append(omega)

print(optimal_omega)


import matplotlib.pyplot as plt

plt.figure(figsize=(8, 5))
plt.plot(omeg, it, marker='o')
plt.xlabel('Параметр ω')
plt.ylabel('Число итераций до сходимости')
plt.title('Скорость сходимости метода SOR в зависимости от ω')
plt.grid(True)
plt.show()