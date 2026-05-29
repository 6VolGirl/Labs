import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.tri as tri
from pathlib import Path

# CSV-файлы с решениями
files1 = {
    "Upwind": r"C:\Users\6anna\PycharmProjects\Labs\Labs_C++\Sem6\Sem6Lab4_CFD\cmake-build-debug\solution_upwind.csv",
    "TVD Minmod": r"C:\Users\6anna\PycharmProjects\Labs\Labs_C++\Sem6\Sem6Lab4_CFD\cmake-build-debug\solution_tvd_minmod.csv",
    "TVD VanLeer": r"C:\Users\6anna\PycharmProjects\Labs\Labs_C++\Sem6\Sem6Lab4_CFD\cmake-build-debug\solution_tvd_vanleer.csv",
    "TVD Superbee": r"C:\Users\6anna\PycharmProjects\Labs\Labs_C++\Sem6\Sem6Lab4_CFD\cmake-build-debug\solution_tvd_superbee.csv",
    "TVD Quick": r"C:\Users\6anna\PycharmProjects\Labs\Labs_C++\Sem6\Sem6Lab4_CFD\cmake-build-debug\solution_quick.csv",
}

files2 = {
    "Upwind": r"C:\Users\6anna\PycharmProjects\Labs\Labs_C++\Sem6\Sem6Lab4_CFD\cmake-build-debug\task2_solution_upwind.csv",
    "TVD Minmod": r"C:\Users\6anna\PycharmProjects\Labs\Labs_C++\Sem6\Sem6Lab4_CFD\cmake-build-debug\task2_solution_tvd_minmod.csv",
    "TVD VanLeer": r"C:\Users\6anna\PycharmProjects\Labs\Labs_C++\Sem6\Sem6Lab4_CFD\cmake-build-debug\task2_solution_tvd_vanleer.csv",
    "TVD Superbee": r"C:\Users\6anna\PycharmProjects\Labs\Labs_C++\Sem6\Sem6Lab4_CFD\cmake-build-debug\task2_solution_upwind.csv",
    "TVD Quick": r"C:\Users\6anna\PycharmProjects\Labs\Labs_C++\Sem6\Sem6Lab4_CFD\cmake-build-debug\task2_solution_quick.csv",
}

output_dir = Path("plots")
output_dir.mkdir(exist_ok=True)

# Сначала читаем все данные, чтобы сделать общую цветовую шкалу
all_phi = []
data = {}

for method, filename in files1.items():
    df = pd.read_csv(filename)
    data[method] = df
    all_phi.extend(df["phi"].values)

phi_min = min(all_phi)
phi_max = max(all_phi)

# ---------
# Отдельный график для каждого метода
# ---------
for method, df in data.items():
    x = df["x"].values
    y = df["y"].values
    phi = df["phi"].values

    triang = tri.Triangulation(x, y)

    plt.figure(figsize=(7, 6))
    contour = plt.tricontourf(
        triang, phi,
        levels=50,
        cmap="viridis",
        vmin=phi_min,
        vmax=phi_max
    )
    plt.colorbar(contour, label="phi")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title(f"2D solution: {method}")
    plt.axis("equal")
    plt.tight_layout()

    safe_name = method.lower().replace(" ", "_")
    plt.savefig(output_dir / f"{safe_name}_2d.png", dpi=300)
    plt.show()

# ---------
# Общий рисунок 2x2 для всех методов
# ---------
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
axes = axes.ravel()

for ax, (method, df) in zip(axes, data.items()):
    x = df["x"].values
    y = df["y"].values
    phi = df["phi"].values

    triang = tri.Triangulation(x, y)

    contour = ax.tricontourf(
        triang, phi,
        levels=50,
        cmap="viridis",
        vmin=phi_min,
        vmax=phi_max
    )
    ax.set_title(method)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_aspect("equal")

cbar = fig.colorbar(contour, ax=axes, shrink=0.9)
cbar.set_label("phi")

fig.suptitle("2D comparison of numerical schemes", fontsize=14)
plt.tight_layout()
plt.savefig(output_dir / "all_methods_2d.png", dpi=300)
plt.show()
