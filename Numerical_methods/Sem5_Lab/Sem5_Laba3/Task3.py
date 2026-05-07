import numpy as np


Ih = -0.195788515848799753839057233146
print(Ih)

#def f(t):
#    return (t**(-2/3)) * np.sin(t**(1/3)) * np.log(t) * np.exp(-t)
#

nodes = np.array([
    0.263560,
    1.413403,
    3.596426,
    7.085810,
    12.640801
])
weights = np.array([
    0.521756,
    0.398667,
    0.0759424,
    0.00361176,
    0.0000233700
])

#def laguerre_integral(nodes, weights):
#    I_gauss_laguerre = np.sum(weights * f(nodes))
#    return I_gauss_laguerre

#print ("laguerre_integral: ", laguerre_integral(nodes, weights)/9)



from scipy.integrate import fixed_quad, quad # вычисляет определённый интеграл заданной функции в заданных пределах [a, b]
from scipy.special import roots_laguerre

f = lambda x: np.exp(-x**3) * np.sin(x) * np.log(x)


# 1) Замена переменной x = t/(1-t), t ∈ (0,1)
def g(t):
    x = t/(1-t)
    return np.exp(-x**3) * np.sin(x) * np.log(x) * (1/(1-t)**2)

I_fixed, _ = fixed_quad(g, 1e-12, 1-1e-12, n=100)

# 2) Гаусс–Лагерр
n = 200
xL, wL = roots_laguerre(n)
I_lag = np.sum(wL * (np.exp(xL - xL**3) * np.sin(xL) * np.log(xL)))


n = 200
xL2, wL2 = roots_laguerre(n)
g = np.sin(xL2**(1/3)) * np.log(xL2) * xL2**(-2/3)
I_lag2 = np.sum(wL2 * g) / 9


# 3) Адаптивный quad на [0, ∞) - численно вычисляет НЕСОБСТВЕННЫЕ интегралы
I_quad, err_quad = quad(f, 0, np.inf, limit=1000)

print("fixed_quad:", I_fixed, "error:", abs(I_fixed - Ih))
print("Laguerre1  :", I_lag,   "error:", abs(I_lag   - Ih))
print("Laguerre2  :", I_lag2,   "error:", abs(I_lag2   - Ih))
print("quad      :", I_quad,  "error:", abs(I_quad  - Ih), "est.err:", err_quad)
