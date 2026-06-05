import numpy as np
import math
import matplotlib.pyplot as plt
import sys

sys.path.append("C:\\Users\\6anna\\PycharmProjects\\Numerical_methods")

from PotentialSinusoidal import PotentialSinusoidal
from PotentialTriangular import PotentialTriangular
from SmoluchowskiBTCS import SmoluchowskiBTCS


def plot_solution_evolution(t_grid, rho_grid, x, t_indices=None, title=""):
    """Построение эволюции распределения"""
    if t_indices is None:
        t_indices = [0, len(t_grid) // 4, len(t_grid) // 2, 3 * len(t_grid) // 4, -1]

    plt.figure(figsize=(10, 6))
    colors = ['b', 'g', 'r', 'c', 'm']

    for idx, color in zip(t_indices, colors):
        if idx < len(rho_grid):
            plt.plot(x, rho_grid[idx, :], color=color, label=f"t = {t_grid[idx]:.3f}", linewidth=2)

    plt.xlabel("Координата x", fontsize=12)
    plt.ylabel("Плотность вероятности ρ(x,t)", fontsize=12)
    plt.title(title, fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=10)
    plt.tight_layout()
    plt.show()


def plot_approach_to_equilibrium(t_grid, rho_grid, rho_eq, x):
    """Построение сходимости к равновесному распределению"""
    errors = np.zeros(len(t_grid))

    # сдвиг болцмановского профиля на L/2
    x_shifted = (x + L/2) % L
    idx_sort = np.argsort(x_shifted)
    rho_eq_shifted = rho_eq[idx_sort]

    for n in range(len(t_grid)):
        errors[n] = np.sqrt(np.sum((rho_grid[n, :] - rho_eq) ** 2) * (x[1] - x[0]))

    plt.figure(figsize=(10, 5))
    plt.semilogy(t_grid, errors, 'b-', linewidth=2)
    plt.xlabel("Время t", fontsize=12)
    plt.ylabel("L2-норма ошибки", fontsize=12)
    plt.title("Сходимость к равновесному распределению", fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def plot_comparison_with_boltzmann_shifted(t_grid, rho_grid, rho_eq, x, L, time_index=-1):
    """Сравнение с Больцмановским распределением со сдвигом на L/2"""
    plt.figure(figsize=(10, 6))

    plt.plot(x, rho_grid[time_index, :], 'b-', linewidth=2.5,
             label=f"Численное решение, t={t_grid[time_index]:.3f}")

    x_shifted = (x + L / 2) % L  # периодический сдвиг
    idx_sort = np.argsort(x_shifted)
    rho_eq_shifted = rho_eq[idx_sort]
    x_shifted_sorted = x_shifted[idx_sort]

    plt.plot(x_shifted_sorted, rho_eq_shifted, 'r--', linewidth=2.5,
             label="Больцмановское распределение (сдвинуто на L/2)")

    plt.xlabel("Координата x", fontsize=12)
    plt.ylabel("Плотность вероятности ρ(x)", fontsize=12)
    plt.title("Сравнение с равновесным распределением", fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=10)
    plt.tight_layout()
    plt.show()

    error_shifted = np.sqrt(np.sum((rho_grid[time_index, :] - rho_eq_shifted) ** 2) * (x[1] - x[0]))
    print(f"L2-ошибка после сдвига на L/2: {error_shifted:.6e}")



L = 2.0 * np.pi  # Период для синусоидального потенциала
nx = 200
nt = 500
t_end = 5.0

U0=2.0
D=1.0
beta=2.0
F=1.0

def rho_init(x):
    return np.ones_like(x) / L


print("Тестирование синусоидального потенциала...")
pot_sin = PotentialSinusoidal(U0=U0, L=L)  # U0 - амплитуда потенциала
smol_sin = SmoluchowskiBTCS(potential=pot_sin, D=D, beta=beta, F=F, L=L)
x_sin, t_sin, rho_sin = smol_sin.solve(rho_init=rho_init, x_domain=(0.0, L), t_domain=(0.0, t_end), nx=nx, nt=nt)

rho_eq_sin = smol_sin.boltzmann_distribution()

plot_solution_evolution(t_sin, rho_sin, x_sin, title="Синусоидальный потенциал")
#plot_approach_to_equilibrium(t_sin, rho_sin, rho_eq_sin, x_sin)
plot_comparison_with_boltzmann_shifted(t_sin, rho_sin, rho_eq_sin, x_sin, L)


print("Готово для треугольный потенциала!")

pot_tri = PotentialTriangular(U0=U0, x0=0.2*L, L=L)
smol_tri = SmoluchowskiBTCS(potential=pot_tri, D=D, beta=beta, F=F, L=L)
x_tri, t_tri, rho_tri = smol_tri.solve(rho_init=rho_init, x_domain=(0.0, L), t_domain=(0.0, t_end), nx=nx, nt=nt)

rho_eq_tri = smol_tri.boltzmann_distribution()


plot_solution_evolution(t_tri, rho_tri, x_tri, title="Треугольный потенциал")
#plot_approach_to_equilibrium(t_tri, rho_tri, rho_eq_tri, x_tri)
plot_comparison_with_boltzmann_shifted(t_tri, rho_tri, rho_eq_tri, x_tri, L)




#=======================================================================================
# Пункт 3
#=======================================================================================

sys.path.append("C:\\Users\\6anna\\PycharmProjects\\Sem5_special_Lab2(1)")
#from main import generate_trajectory

def generate_trajectory (M, N, dt, D, x0, F_const):
    t = np.linspace(0, N * dt, N + 1)
    # x[i,n] = координата i-го испытания в момент n
    x = np.zeros((M, N + 1))
    for i in range(M):
        x[i, 0] = x0
        for n in range(N):
            w = np.random.randn()  # нормальное(Гауссовское) распределение
            #F_pot = -U0 * (2*np.pi/L) * np.cos(2*np.pi * x[i, n] / L)
            #x[i, n + 1] = x[i, n] + (F + F_const) * dt + np.sqrt(2 * dt) * w
            F_pot = -U0 * (2 * np.pi / L) * np.cos(2 * np.pi * x[i, n] / L)
            x[i, n + 1] = x[i, n] + (F_pot + F_const) * dt + np.sqrt(2 * D * dt) * w

            if x[i, n + 1] < 0:
                x[i, n + 1] += L
            elif x[i, n + 1] > L:
                x[i, n + 1] -= L
    return x, t


def plot_hist_with_smoluchowski_envelope(samples_x, rho_grid, t_grid, x_grid, t_star_index=-1, bins=40, title=""):
    rho_t = rho_grid[t_star_index, :]

    plt.figure(figsize=(10, 6))
    plt.hist(samples_x, bins=bins, density=True,
             alpha=0.4, label='Ланжевен: гистограмма')

    plt.plot(x_grid, rho_t, 'r-', linewidth=2.5,
             label=f'Смолуховский: ρ(x, t={t_grid[t_star_index]:.3f})')

    plt.xlabel("Координата x", fontsize=12)
    plt.ylabel("Плотность вероятности", fontsize=12)
    plt.title(title, fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=10)
    plt.tight_layout()
    plt.show()

def compare_langevin_smoluchowski_for_sin():
    M = 1000
    N = 500
    D = 1
    x0 = 0
    dt = 0.01
    x_lan, t_lan = generate_trajectory(M, N, dt, D, x0, F)

    t_star = t_sin[-1]
    idx_star = np.argmin(np.abs(t_lan - t_star))

    samples_x = x_lan[:, idx_star]

    # рисуем гистограмму + огибающую из решения Смолуховского
    plot_hist_with_smoluchowski_envelope(samples_x=samples_x, rho_grid=rho_sin, t_grid=t_sin, x_grid=x_sin, t_star_index=-1, bins=60, title="Синусоидальный потенциал: Ланжевен vs Смолуховский")

compare_langevin_smoluchowski_for_sin()




#=======================================================================================
# Пункт 4
#=======================================================================================
import numpy as np

def v_stratonovich(F, potential, D, beta, L, nx_int=2000):
    """
    Стратоновичевская средняя скорость <v> = L * J_st
    F – постоянная сила
    potential(x) – U(x)
    D, beta – коэффициент диффузии и 1/(k_B T)
    L – период
    nx_int – число точек для численной интеграции
    """
    x = np.linspace(0.0, L, nx_int)
    dx = x[1] - x[0]

    #Ux = potential(x) - F * x
    #num = 1.0 - np.exp(-beta * F * L)
    # интегралы
    #exp_plus = np.exp(beta * Ux)
    #exp_minus = np.exp(-beta * Ux)
    # Интеграл ∫_0^L e^{βU(x)} dx
    #I_plus_full = np.sum(exp_plus) * dx
    # Для каждого x нужно ∫_0^x e^{βU(y)} dy
    #cum_int_plus = np.cumsum(exp_plus) * dx
    #inner_bracket = I_plus_full - (1.0 - np.exp(-beta * F * L)) * cum_int_plus
    # интеграл ∫_0^L dx e^{-βU(x)}
    #denom = np.sum(exp_minus * inner_bracket) * dx

    #J_st = D * num / denom
    #v_st = L * J_st

    U_total = potential(x) - F * x

    # Вычисление интегралов
    exp_betaU = np.exp(beta * U_total)
    exp_minus_betaU = np.exp(-beta * U_total)

    # ∫_0^L exp(βU(x)) dx
    I_plus = np.trapezoid(exp_betaU, x)

    # ∫_0^x exp(βU(y)) dy для каждого x
    cum_int = np.zeros_like(x)
    for i in range(len(x)):
        cum_int[i] = np.trapezoid(exp_betaU[:i + 1], x[:i + 1])

    # Внутренний интеграл
    inner = I_plus - (1 - np.exp(-beta * F * L)) * cum_int

    # Внешний интеграл ∫_0^L exp(-βU(x)) * inner dx
    integrand = exp_minus_betaU * inner
    I_total = np.trapezoid(integrand, x)

    # Ток и скорость
    J = D * (1 - np.exp(-beta * F * L)) / I_total
    v_st = L * J

    return v_st


F = 0.2
beta = 1.0
D = 1.0

v_analytical = v_stratonovich(F, pot_sin, D, beta, L)
print("v_Stratonovich =", v_analytical)

M = 1000
N = 500
D = 1
x0 = 0.0
dt = 0.001
x_lan, t_lan = generate_trajectory(M, N, dt, D, x0, F)
displacement = x_lan[:, -1] - x_lan[:, 0]
v_num = np.mean(displacement) / t_lan[-1]
print("v_num =", v_num)

F_list = [0.1, 0.2, 0.3, 0.4]
v_analytical_list = []
v_num_list = []

M = 1000
N = 500
dt = 0.001
D = 1.0
x0 = 0.0

for F in F_list:
    v_an = v_stratonovich(F, pot_sin, D, beta, L)
    v_analytical_list.append(v_an)

    x_lan, t_lan = generate_trajectory(M, N, dt, D, x0, F)
    displacement = x_lan[:, -1] - x_lan[:, 0]
    v_num = np.mean(displacement) / t_lan[-1]
    v_num_list.append(v_num)

plt.figure(figsize=(8,5))
plt.plot(F_list, v_analytical_list, 'r-', lw=2.5, label='v(F) по формуле Стратоновича')
plt.plot(F_list, v_num_list, 'bo--', lw=1.5, ms=6, label='v(F) по Ланжевену (численно)')
plt.xlabel('Сила F')
plt.ylabel('Средняя скорость v')
plt.title('Сравнение с формулой Стратоновича')
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.show()



#=======================================================================================
# Пункт 5
#=======================================================================================
L = 1.0
l = 0.3
U0 = 2.0

def U_asym(x):
    x = np.mod(x, L)
    return np.where(x < l, U0 * x / l, U0 * (L - x) / (L - l))

def dU_asym(x):
    x = np.mod(x, L)
    return np.where(x < l, U0 / l, -U0 / (L - l))

def generate_trajectory_ratchet(M, N, dt, D, x0, lam):
    """
    On-off рэтчет: U(x,t) = η(t) U_asym(x), η(t) ∈ {0,1}
    lam – интенсивность переключения η (1/время)
    """
    t = np.linspace(0, N * dt, N + 1)
    x = np.zeros((M, N + 1))

    eta = 1
    p_switch = lam * dt

    for i in range(M):
        x[i, 0] = x0

    for n in range(N):
        if np.random.rand() < p_switch:
            eta = 1 - eta

        w = np.random.randn(M)
        F_pot = -eta * dU_asym(x[:, n])     # -η U'(x)
        x[:, n+1] = x[:, n] + F_pot * dt + np.sqrt(2 * D * dt) * w

        x[:, n+1] = np.mod(x[:, n+1], L)

    return x, t

M = 5000
N = 5000
dt = 0.001
D = 1.0
x0 = 0.0
lam = 1.0

x_rat, t_rat = generate_trajectory_ratchet(M, N, dt, D, x0, lam)
displacement = x_rat[:, -1] - x_rat[:, 0]
displacement = (displacement + L/2) % L - L/2

v_r = np.mean(displacement) / t_rat[-1]
print("v_ratchet =", v_r)



