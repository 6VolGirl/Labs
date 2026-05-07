import math
import numpy as np
import matplotlib.pyplot as plt

def analyzed_function(x: float):
    return  2 * math.log(x) + math.sin(math.log(x)) - math.cos(math.log(x))
def diff_analyzed_function(x: float):
    return (2 + math.cos(math.log(x)) + math.sin(math.log(x)))/x

def phi(y: float):
    return (-math.sin(y) +math.cos(y)) / 2

def sample_fun(x):
    return 4 - math.exp(x) - 2 * x**2

def bisection_method(a:float, b:float, epsilon, fun):
    if fun(a)*fun(b) > 0:
        print(f"Не корректный отрезок: [{a}, {b}] " )
    k = 0

    while (b-a)>epsilon:
        c = (a+b)/2.0
        print(f"a= {a}, b= {b}, c= {c}")
        if (c <= 1e-10):
            absolute_err = abs(b-a)/2
            # относительную не посчитать деление на ноль
            return c, absolute_err, 0
        elif fun(a) * fun(c) < 0:
            b = c
        elif fun(c) * fun(b) < 0:
            a = c
        k+=1
        absolute_err = abs(b - a) / 2
        if  (c < 1e-10):
            raise ValueError("Приближение к корню равно нулю — относительная погрешность не определена.")
        relative_err = absolute_err / c
    return c, k, absolute_err, relative_err

def iteration_method(phi, y0: float, tol: float):

    for k in range(100):

        y1 = phi(y0)
        absolute_err = abs(y1 - y0)
        if y1 < 1e-10:
            relative_err = 0
        else:
            relative_err = absolute_err / y1

        if absolute_err < tol:
            return y1, k, absolute_err, relative_err
        y0 = y1
    raise RuntimeError("Метод не сошёлся за максимальное число итераций.")

def newton_method(f, df, x, tol):

    for k in range(100):
        if abs(df(x)) < 1e-10:
            f = df(x)
            raise ZeroDivisionError(f"Производная f'(x) = 0 в точке x = {x}. Метод Ньютона невозможен.")
        x1 = x - f(x)/df(x)

        absolute_err = abs(x1 - x)
        if x1 < 1e-10:
            relative_err = 0
        else:
            relative_err = absolute_err / x1

        if absolute_err < tol:
            return x1, k, absolute_err, relative_err
        x = x1

    raise RuntimeError("Метод не сошёлся за максимальное число итераций.")
print(bisection_method(1, 3, 1e-7, analyzed_function))
print(iteration_method(phi, 0.0005, 1e-7))
print(newton_method(analyzed_function, diff_analyzed_function, 1, 1e-7))

glob_count = 0

def fun_oscillation(t : float, v0 = 1.0 , l0 = math.pi, omega = 1, amplitude = 3):
    #Asin(wt) + l0 - v0*t = 0
    global glob_count
    glob_count += 1
    return amplitude * math.sin(omega*t) - v0*t + l0

def diff_oscillation(t : float, v0 = 1.0, l0 = math.pi, omega = 1, amplitude = 3):
    global glob_count
    glob_count += 1
    return amplitude * math.cos(omega * t) - v0

def phi_oscillation(t : float, v0 = 2.0, l0 = math.pi, omega = 1, amplitude = 3):
    global glob_count
    glob_count += 1
    return (amplitude * math.sin(omega * t) + l0)/v0


#print(bisection_method(1, 100, 1e-7, fun_oscillation))
#print(iteration_method(phi_oscillation, 0.0005, 1e-7))
#print(newton_method(fun_oscillation, diff_oscillation, 1, 1e-7))

def estimate_multiplicity_simple(f, x_star, delta=1e-6):
    """ 𝑚 ≈ log|f(x)|/log|x−x∗| """
    x = x_star + delta
    fx = f(x)

    if abs(fx) < 1e-15:
        x = x_star + 1e-5
        fx = f(x)

    if abs(fx) < 1e-16:
        return 1

    try:
        m = math.log(abs(fx)) / math.log(abs(x - x_star))
    except:
        return 1

    m = max(1, round(m))
    return m if m <= 10 else 1

#x, _, _, _ = newton_method(fun_oscillation, diff_oscillation, 1, 1e-7)
#print( "m = ", estimate_multiplicity_simple(fun_oscillation, x))


# График t(v)
v_values = []
t_values = []


# for v in np.arange(1, 7.0, 0.2):
#     f = lambda t: fun_oscillation(t, v0=v)
#     df = lambda t: diff_oscillation(t, v0=v)
#     t, _, _, _ = newton_method(f, df, 1, 1e-7)  # начальное приближение
#     t_values.append(t)
#     v_values.append(v)




plt.figure(figsize=(10, 6))
plt.plot(v_values, t_values, marker='o', color='blue')
plt.xlabel('Скорость v')
plt.ylabel('Время t(v)')
plt.title('Зависимость времени от скорости: t(v)')
plt.grid(True)
#plt.show()