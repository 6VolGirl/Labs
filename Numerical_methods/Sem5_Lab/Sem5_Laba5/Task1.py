import numpy as np
import matplotlib.pyplot as plt


import sys
sys.path.append ("C:\\Users\\6anna\\PycharmProjects\\Labs\\Numerical_methods\\Numerical_methods_classes\\Linear_Systems\\Direct_Methods")
from TridiagonalMatrixAlgorithm import TridiagonalMatrixAlgorithm

def build_bessel_tridiagonal_matrix(a: float, b: float, N: int, v: float =1):
    """
    Строим матрицу A и вектор f для задачи:
        x^2 u'' + x u' + (x^2 - 1)u = 0, x ∈ [a, b]
        u(a) = 1, u(b) = 0
    """
    h = (b - a) / N
    x = np.linspace(a, b, N + 1)
    n = N - 1
    A = np.zeros((n, n))
    f = np.zeros(n)

    for k in range(n):
        i = k + 1

        k05 = 0.25 * (x[i] + x[i - 1])**2  # k_{i-1/2}
        k15 = 0.25 * (x[i] + x[i + 1])**2  # k_{i+1/2}

        A_i = k05 / h ** 2 + x[i] / (2*h)
        B_i = - (k05 + k15) / h**2 + x[i]**2 - v**2
        C_i = k15 / h ** 2 - x[i] / (2*h)

        A[k, k] = B_i
        if k > 0:
            A[k, k - 1] = A_i
        if k < n - 1:
            A[k, k + 1] = C_i

        rhs = 0.0
        if i == 1:
            rhs -= A_i * 1.0
        if i == N - 1:
            rhs -= C_i * 0.0

        f[k] = rhs

    return A, f, x



a = 1
b = 15
nu = 3.0
N = 100
u_a = 1
u_b = 0

A, f, x = build_bessel_tridiagonal_matrix(a, b, N, nu)
tma = TridiagonalMatrixAlgorithm()
u_without_conditions = tma.solve(A, f)
u = np.zeros(N + 1)
u[0] = 1.0
u[-1] = 0.0
u[1:-1] = u_without_conditions


plt.plot(x, u, "-o", ms=3)
plt.grid(True)
plt.xlabel("x")
plt.ylabel("u(x)")
plt.show()


