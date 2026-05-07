import Task1 as t1
import numpy as np
import matplotlib.pyplot as plt

a = 0.1
b = 7.7
#n_values = [10 * i for i in range(8)]  # 10, 20, 40, 80, 160, 320, 640, 1280

methods = [("Центральные прямоугольники", t1.formula_central_rectangles), ("Трапеции", t1.trapezoid_formula), ("Симпсон", t1.simpson_formula)]

#n_list = [10 * i for i in range(1, 31)]
n_list = [10 * 2**i for i in range(12)]
#n_list = [20 * 2**i for i in range(1, 12)]

gamma_theory = {"Центральные прямоугольники": 2, "Трапеции": 2, "Симпсон": 4}

results = {}

for name, method in methods:
    I_vals = []
    n_vals = []

    for n in n_list:
        x = np.linspace(a, b, n + 1)
        I = method(t1.f, x)
        I_vals.append(I)
        n_vals.append(n)

    R_vals = []
    n_R = []

    gamma = gamma_theory[name]
    r = 2
    denom = r ** gamma - 1

    for k in range(1, len(I_vals)):
        R = (I_vals[k] - I_vals[k - 1]) / denom
        R_vals.append(R)
        n_R.append(n_vals[k])

    ln_R = [np.log(abs(R)) for R in R_vals if R != 0]
    ln_n = [np.log(n) for n in n_R]

    gamma_k = []
    ln_n_gamma = []
    for i in range(1, len(R_vals)):
        if R_vals[i] != 0 and R_vals[i - 1] != 0:
            ratio = R_vals[i - 1] / R_vals[i]
        if ratio > 0:
            d_lnR = np.log(ratio)
            gamma_k.append(d_lnR / np.log(r))
            ln_n_gamma.append(ln_n[i])



    results[name] = {
        "ln_n": ln_n,
        "ln_R": ln_R,
        "ln_n_gamma": ln_n_gamma,
        "gamma_k": gamma_k,
        "theory_gamma": gamma}



# График  ln|R_k| от ln n_k
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
colors = ['red', 'blue', 'green']
for i, (name, data) in enumerate(results.items()):
    plt.plot(data["ln_n"], data["ln_R"], 'o-', color=colors[i], label=name)
plt.xlabel(r'$\ln n_k$')
plt.ylabel(r'$\ln |R_k|$')
plt.title(r'График $\ln |R_k|$ от $\ln n_k$')
plt.grid(True)
plt.legend()



plt.subplot(1, 2, 2)
for i, (name, data) in enumerate(results.items()):
    if  i == 2:
        continue
    plt.plot(data["ln_n_gamma"], data["gamma_k"], 's--', color=colors[i], label=name)
    # Горизонтальная линия — теоретический порядок
    plt.axhline(y=data["theory_gamma"], color=colors[i], linestyle=':', alpha=0.7)
plt.xlabel(r'$\ln n_k$')
plt.ylabel(r'Экспериментальный порядок $\gamma_k$')
plt.title(r'График $\gamma_k$ от $\ln n_k$')
plt.grid(True)
plt.legend()

plt.tight_layout()


plt.show()