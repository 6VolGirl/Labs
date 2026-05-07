import numpy as np
import random
import math
from numpy.polynomial.legendre import leggauss


def formula_central_rectangles(f, x):
    """ x — массив узлов сетки (произвольный, но упорядоченный) """
    x = np.array(x)
    if x.ndim != 1 or len(x) < 2:
        raise ValueError("x должен быть одномерным массивом длины >= 2")

    I =0.0
    for i in range(1, len(x)):
        h = x[i] - x[i-1]
        x_mid = (x[i] + x[i-1])/2.0
        I += f(x_mid) * h
    return I

def trapezoid_formula(f, x):
    x = np.array(x)
    if x.ndim != 1 or len(x) < 2:
        raise ValueError("x должен быть одномерным массивом длины >= 2")

    I = 0.0
    for i in range(1, len(x)):
        h = x[i] - x[i-1]
        I += (f(x[i-1])+f(x[i]))*h/2
    return I

def simpson_formula(f, x):
    x = np.array(x)
    if x.ndim != 1 or len(x) < 2:
        raise ValueError("x должен быть одномерным массивом длины >= 2")
    n = len(x) - 1
    if n % 2 != 0:
        raise ValueError("Число интервалов должно быть чётным для формулы Симпсона")
    h = (x[-1] - x[0]) / n
    I = f(x[0]) + f(x[-1])
    for i in range(1, n, 2):
        I += 4 * f(x[i])
    for i in range(2, n, 2):
        I += 2 * f(x[i])
    I *= h / 3
    return I

#def simpson_formula(f, x):
#    x = np.array(x)
#    if x.ndim != 1 or len(x) < 2:
#        raise ValueError("x должен быть одномерным массивом длины >= 2")
#
#    n = len(x) - 1
#    if n % 2 != 0:
#        raise ValueError("Число интервалов должно быть чётным для формулы Симпсона")
#
#    h = np.diff(x)
#    if not np.allclose(h, h[0], rtol=1e-12, atol=1e-12):
#        raise ValueError("Формула Симпсона требует равномерную сетку")

#    I = 0.0
#    for i in range(1, n):
#        h_i = h[0]
#        I += (f(x[i-1]) + 4*f((x[i]+x[i-1])/2) + f(x[i])) * h_i/6
#    return I

def gauss_christoffel(f, n, a, b):
    x_gauss, с_gauss = leggauss(n)

    # Преобразуем узлы и веса на отрезок [a, b]
    # x = (b-a)/2 * x_gauss + (a+b)/2
    # с = (b-a)/2 * с_gauss
    x_scaled = (b - a) / 2 * x_gauss + (a + b) / 2
    с_scaled = (b - a) / 2 * с_gauss

    I = np.sum(с_scaled * f(x_scaled))
    return I

def f(x): return x**(3/2)/(5*x + 2.8)**2

a = 0.1
b = 7.7
N = 1001

x_uniform = np.linspace(a, b, N)

I_wolfram = 0.111986

eps = 1e-8



def compute_integral_with_precision(f, a, b, epsilon, method, gamma, r=2, max_iterations=25):
    n = 10
    x = np.linspace(a, b, n + 1)
    I0 = method(f, x)

    for iteration in range(max_iterations):
        n *= r
        x = np.linspace(a, b, n + 1)
        I1 = method(f, x)

        R1 = (I1 - I0) / (r ** gamma - 1)
        I = I1 + R1

        if abs(R1) < epsilon:
            h = (b - a) / n
            return I, abs(R1), h, n

        I0 = I1

    print(f"Точность {epsilon} не достигнута за {max_iterations} итераций")
    h = (b - a) / n
    return I, abs(R1), h, n



print(compute_integral_with_precision(f, a, b, eps, formula_central_rectangles, 2, r=2, max_iterations=25))
print(compute_integral_with_precision(f, a, b, eps, trapezoid_formula, 2, r=2, max_iterations=25))
print(compute_integral_with_precision(f, a, b, eps, simpson_formula, 4, r=2, max_iterations=25))


#print(accuracy(formula_central_rectangles, f,  I_wolfram, eps, a, b, N))
#print(accuracy(trapezoid_formula, f,  I_wolfram, eps, a, b, N))
#print(accuracy(simpson_formula, f,  I_wolfram, eps, a, b, N))



print(formula_central_rectangles(f, x_uniform))
print(trapezoid_formula(f, x_uniform))
print(simpson_formula(f, x_uniform))
print(gauss_christoffel(f, 10, a, b))


# вольфрам: 0,111986


