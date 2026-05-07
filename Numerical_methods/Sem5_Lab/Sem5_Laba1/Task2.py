import  random
import numpy as np
import pyamg

def generate_matrix_for_jacobi(n, diag_min=5, off_diag_max=2):
    """
    Генерирует случайную диагонально-преобладающую матрицу n×n для устойчивой работы метода Якоби
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


def jacobi_method(A, f, x0, max_iter = 50, tol = 1e-6):
    """
    Реализует метод Якоби для решения системы линейных уравнений Ax=f
    с заданным числом итераций и точностью; возвращает решение, число итераций и историю невязки
    """
    error_rate = []
    A = np.array(A)
    f = np.array(f)
    n = len(f)

    if x0 is None:
        x = np.zeros(n)
    else:
        x = np.array(x0)

    for k in range(max_iter):
        x_new = np.zeros_like(x)

        for i in range(n):
            s = np.dot(A[i, :], x) - A[i, i] * x[i]
            x_new[i] = (f[i] - s) / A[i][i]
            if np.isnan(x_new).any():
                print(f"A[i, :] = {A[i, :]} A[i, i] = {A[i, i]}  x[i] = {x[i]}" )
            if A[i][i] <1e-10:
                print ("0!!!!!!!")

        error_rate.append(np.linalg.norm(A @ x - f)/np.linalg.norm(f))

        if np.linalg.norm(x_new - x) < tol:
            print(f"Сходится за {k + 1} итераций")
            return x_new, k + 1, error_rate

        x = x_new

    return (x, max_iter, error_rate)

def seidel_method(A, f, x0, max_iter = 10000, tol = 1e-6):
     """
     Реализует метод Гаусса–Зейделя для решения системы Ax=f:
     возвращает приближённое решение, число итераций и историю невязки
     """
     error_rate = []
     A = np.array(A)
     f = np.array(f)
     n = len(f)

     if x0 is None:
          x = np.zeros(n)
     else:
          x = np.array(x0)

     for k in range(max_iter):
          x_prev = np.copy(x)
          for i in range(n):
               s1 = np.dot(A[i, :i], x[:i])
               s2 = np.dot(A[i, i+1:], x_prev[i+1:])
               x[i] = (f[i] - s1 - s2)/A[i][i]

          error_rate.append(np.linalg.norm(A @ x_prev - f) / np.linalg.norm(f))

          if np.linalg.norm(x - x_prev) < tol:
               print(f"Сходится за {k + 1} итераций")
               return x, k + 1, error_rate

     return x, max_iter, error_rate

def SOR_method(A, f, x0, omega = 1, max_iter = 10000, tol = 1e-6):
     """
     Реализует метод верхней релаксации (SOR) для решения системы Ax=f:
     возвращает приближённое решение, число итераций и историю невязки
     """
     error_rate = []
     A = np.array(A)
     f = np.array(f)
     n = len(f)
     if x0 is None:
          x = np.zeros(n)
     else:
          x = np.array(x0)

     for k in range(max_iter):
          x_prev = np.copy(x)
          for i in range(n):
               s1 = np.dot(A[i, :i], x[:i])
               s2 = np.dot(A[i, i+1:], x_prev[i+1:])
               x[i] = (1 - omega)*x_prev[i] + omega * (f[i] - s1 - s2)/A[i][i]

          error_rate.append( np.linalg.norm(A @ x_prev - f) / np.linalg.norm(f))

          if np.linalg.norm(x - x_prev) < tol:
               print(f"Сходится за {k + 1} итераций")
               return x, k + 1, error_rate

     return x, max_iter, error_rate


#a, fi = pyamg.gallery.linear_elasticity((10, 10))
#A = a.toarray()
#b= [i for i in range(len(A))]

A = generate_matrix_for_jacobi(100, diag_min=5, off_diag_max=2)
b= [i for i in range(len(A))]


for i in range(len(A)):
    if abs(A[i, i]) <= np.sum(np.abs(A[i])) - abs(A[i, i]):
        print("нет сторого диаг преобладания")
        break

x, iter, jacobi = jacobi_method(A, b, None)
x, iter, seidel = seidel_method(A, b, None)
x, iter, sor = SOR_method(A, b, None, 0.9)
#print(jacobi, seidel, sor)

import matplotlib.pyplot as plt

plt.figure(figsize=(8, 5))
plt.semilogy(jacobi, label='Якоби')
plt.semilogy(seidel, label='Зейдель')
plt.semilogy(sor, label='SOR (ω=0.9)')
plt.xlabel('Номер итерации')
plt.ylabel('Относительная невязка ∥Ax - b∥ / ∥b∥')
plt.title('Сравнение скорости сходимости')
plt.legend()
plt.grid(True, which='both', linestyle='--')
plt.show()



