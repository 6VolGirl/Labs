import random


def tridiagonal_matrix_algorithm(a:list, b:list, c:list, f:list):
    """
     Метод прогонки (алгоритм Томаса) для решения трёхдиагональной СЛАУ
     a — поддиагональ, b — наддиагональ, c — диагональ, f — правая часть
     """

    n = len(c)
    a = [-x for x in a]
    b = [-x for x in b]
    x = [0] * n            # вектор решения
    a_new = [0]
    b_new = [0]

    a_new.append(b[0]/c[0])
    b_new.append(f[0]/c[0])

    #previous_a = b[0]/c[0]
    #previous_b = f[0]/c[0]

    for i in range(1, n):
        if abs(c[i] - a[i] * a_new[i]) < pow(10, -6):
            raise ZeroDivisionError(f"Нулевой знаменатель в строке {i}")
            #с = c[i]
            #a = a[i]
            #b = a_new
        a_new.append(b[i] / (c[i] - a[i] * a_new[i]))
        b_new.append((f[i] + a[i] * b_new[i])/ (c[i] - a[i] * a_new[i]))

    x[n-1] = b_new[n]
    for i in range(n-2, -1, -1):
        x[i] = a_new[i + 1] * x[i + 1] + b_new[i + 1]
    return x

def matrix_view(a, b, c):
    """
    Формирует явную трёхдиагональную матрицу по её под-, над- и главной диагоналям
    """
    n = len(c)
    matrix = [[0] * n for _ in range(n)]

    for i in range(n):
        matrix[i][i] = c[i]
        if i > 0:
            matrix[i][i - 1] = a[i]
        if i < n - 1:
            matrix[i][i + 1] = b[i]

    return matrix

def generate_tridiagonal_matrix(n:int, lower:int, higher:int):
    """
    Генерирует коэффициенты трёхдиагональной матрицы размера n×n
    (поддиагональ a, наддиагональ b, диагональ c с диагональным преобладанием)
    """
    a = [0] * n
    b = [0] * n
    c = [0] * n

    for i in range(n):
        if i > 0:
            a[i] = random.randint(lower, higher)
        if i < n-1:
            b[i] = random.randint(lower, higher)

        c[i] = abs(a[i]) + abs(b[i]) + random.randint(1, 100)

    return [a, b, c]

def multiply_tridiagonal_vector(a, c, b, x):
    """
    Умножает трёхдиагональную матрицу (заданную под-, над- и главной диагоналями a, b, c) на вектор x
    """
    n = len(x)
    f = [0] * n
    for i in range(n):
        if i==n-1:
            f[i] = a[i] * x [i-1] + c[i] * x [i]
            break
        if i==0:
            f[i] = c[i] * x [i] + b[i] * x [i+1]
        else:
            f[i] = a[i] * x [i-1] + c[i] * x [i] + b[i] * x [i+1]
    return f

#третий пункт
n = 10
a, b, c = generate_tridiagonal_matrix(n, 1, 100)
x_exact = [i for i in range(n)]
f_exact = multiply_tridiagonal_vector(a, c, b, x_exact)
x = tridiagonal_matrix_algorithm(a, b, c, f_exact)
print(x)

absolute_err = max(abs(xi - yi) for xi, yi in zip(x, x_exact))
relative_err = max(abs((xi - yi) / yi) if yi != 0 else 0 for xi, yi in zip(x, x_exact))
print(f"для n= {n}:  абс = {absolute_err} \t отн = {relative_err}")

import time
import numpy as np
import matplotlib.pyplot as plt

def time_solve(n):
    """
    Генерирует трёхдиагональную СЛАУ размера n, решает её методом прогонки,
    измеряет время решения и оценивает абсолютную и относительную ошибки
    """
    a, b, c = generate_tridiagonal_matrix(n, 0, 100)
    x_exact = [i for i in range(n)]
    f_exact = multiply_tridiagonal_vector(a, c, b, x_exact)

    for i in range(1, n):
        if abs(c[i]) < abs(a[i]) + abs(b[i]):
            raise ValueError(f"Нет диагонального преобладания в строке {i}")

    t0 = time.perf_counter()
    x = tridiagonal_matrix_algorithm(a, b, c, f_exact)
    t1 = time.perf_counter()
    delta_t = t1 - t0

    absolute_err = max(abs(xi - yi) for xi, yi in zip(x, x_exact))
    relative_err = max(abs((xi - yi)/yi) if yi!=0 else 0 for xi, yi in zip(x, x_exact))
    print(f"для n= {n}:  абс = {absolute_err} \t отн = {relative_err}")

    return delta_t

error = []
points_grafic = []
n = 100
for _ in range(50):
    t = time_solve(n)
    points_grafic.append((n, t))
    n +=100

n_values = [p[0] for p in points_grafic]
t_values = [p[1] for p in points_grafic]

n = np.array(n_values)
t = np.array(t_values)

m = len(n)
a = (np.sum(n * t) - np.sum(n) * np.sum(t) / m) / (np.sum(n**2) - np.sum(n)**2 / m)
b = np.mean(t) - a * np.mean(n)


plt.plot(n_values, t_values, marker='o', linestyle='-', color='b', label='Время решения')
plt.plot(n_values, a * n + b, 'r--', linewidth=2, label=f'МНК: t = {a:.4e}·n + {b:.4e}')

plt.xlabel("Размер системы n")
plt.ylabel("Время решения (сек)")
plt.title("Зависимость времени решения от размера системы")
plt.grid(True, which="both", linestyle="--", linewidth=0.5)
plt.legend()
plt.show()

