import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# --------------------------------------------------
# 1. Имя входного файла
# --------------------------------------------------
file_name1 = r"C:\Users\6anna\PycharmProjects\Labs\Labs_C++\Sem6\Sem6Lab4_CFD\cmake-build-debug\case_L4_constant_field.csv"
file_name2 = r"C:\Users\6anna\PycharmProjects\Labs\Labs_C++\Sem6\Sem6Lab4_CFD\cmake-build-debug\case_L4_poiseuille_field.csv"
#file_name1 = r"C:\Users\6anna\PycharmProjects\Labs\Labs_C++\Sem6\Sem6Lab4_CFD\cmake-build-debug\case_L4_constant_fieldsave.csv"
#file_name2 = r"C:\Users\6anna\PycharmProjects\Labs\Labs_C++\Sem6\Sem6Lab4_CFD\cmake-build-debug\case_L4_poiseuille_fieldsave.csv"
out_dir = Path("plots_field")
out_dir.mkdir(exist_ok=True)

# --------------------------------------------------
# 2. Чтение данных
# --------------------------------------------------
df = pd.read_csv(file_name1)
df.columns = [c.strip() for c in df.columns]

# Ожидаемые столбцы:
# cellId,x,y,u,v,speed,p,pCorr
numeric_cols = ["cellId", "x", "y", "u", "v", "speed", "p", "pCorr"]
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna(subset=numeric_cols).copy()
df = df.sort_values(["y", "x"]).reset_index(drop=True)

# --------------------------------------------------
# 3. Подготовка сетки для contour / heatmap
# --------------------------------------------------
x_vals = np.sort(df["x"].unique())
y_vals = np.sort(df["y"].unique())

nx = len(x_vals)
ny = len(y_vals)

X, Y = np.meshgrid(x_vals, y_vals)

def make_grid(value_col):
    pivot = df.pivot(index="y", columns="x", values=value_col)
    pivot = pivot.reindex(index=y_vals, columns=x_vals)
    return pivot.values

U = make_grid("u")
V = make_grid("v")
SPEED = make_grid("speed")
P = make_grid("p")
PCORR = make_grid("pCorr")

# --------------------------------------------------
# 4. Карта давления p(x,y)
# --------------------------------------------------
plt.figure(figsize=(9, 4.5))
cont = plt.contourf(X, Y, P, levels=30, cmap="viridis")
plt.colorbar(cont, label="p")
plt.xlabel("x")
plt.ylabel("y")
plt.title("Распределение давления p(x, y)")
plt.tight_layout()
plt.savefig(out_dir / "pressure_field.png", dpi=200)
plt.show()

# --------------------------------------------------
# 5. Карта поправки давления pCorr(x,y)
# --------------------------------------------------
plt.figure(figsize=(9, 4.5))
cont = plt.contourf(X, Y, PCORR, levels=30, cmap="coolwarm")
plt.colorbar(cont, label="pCorr")
plt.xlabel("x")
plt.ylabel("y")
plt.title("Распределение поправки давления pCorr(x, y)")
plt.tight_layout()
plt.savefig(out_dir / "pressure_correction_field.png", dpi=200)
plt.show()

# --------------------------------------------------
# 6. Карта модуля скорости |U|(x,y)
# --------------------------------------------------
plt.figure(figsize=(9, 4.5))
cont = plt.contourf(X, Y, SPEED, levels=30, cmap="plasma")
plt.colorbar(cont, label="speed")
plt.xlabel("x")
plt.ylabel("y")
plt.title("Распределение модуля скорости |U|(x, y)")
plt.tight_layout()
plt.savefig(out_dir / "speed_field.png", dpi=200)
plt.show()

# --------------------------------------------------
# 7. Векторное поле скорости
# --------------------------------------------------
plt.figure(figsize=(10, 4.5))

# Чтобы стрелок было не слишком много, прореживаем сетку
step_x = max(1, nx // 20)
step_y = max(1, ny // 12)

plt.quiver(
    X[::step_y, ::step_x],
    Y[::step_y, ::step_x],
    U[::step_y, ::step_x],
    V[::step_y, ::step_x],
    SPEED[::step_y, ::step_x],
    cmap="inferno",
    scale=None
)

plt.xlabel("x")
plt.ylabel("y")
plt.title("Векторное поле скорости")
plt.tight_layout()
plt.savefig(out_dir / "velocity_vectors.png", dpi=200)
plt.show()

# --------------------------------------------------
# 8. Линии тока
# --------------------------------------------------
plt.figure(figsize=(10, 4.5))
plt.streamplot(
    x_vals,
    y_vals,
    U,
    V,
    color=SPEED,
    cmap="viridis",
    density=1.2
)
plt.colorbar(label="speed")
plt.xlabel("x")
plt.ylabel("y")
plt.title("Линии тока")
plt.tight_layout()
plt.savefig(out_dir / "streamlines.png", dpi=200)
plt.show()

# --------------------------------------------------
# 9. 4 графика в одном окне
# --------------------------------------------------
fig, axes = plt.subplots(2, 2, figsize=(12, 8))

c1 = axes[0, 0].contourf(X, Y, P, levels=25, cmap="viridis")
fig.colorbar(c1, ax=axes[0, 0])
axes[0, 0].set_title("Pressure p")
axes[0, 0].set_xlabel("x")
axes[0, 0].set_ylabel("y")

c2 = axes[0, 1].contourf(X, Y, PCORR, levels=25, cmap="coolwarm")
fig.colorbar(c2, ax=axes[0, 1])
axes[0, 1].set_title("Pressure correction pCorr")
axes[0, 1].set_xlabel("x")
axes[0, 1].set_ylabel("y")

c3 = axes[1, 0].contourf(X, Y, SPEED, levels=25, cmap="plasma")
fig.colorbar(c3, ax=axes[1, 0])
axes[1, 0].set_title("Speed magnitude")
axes[1, 0].set_xlabel("x")
axes[1, 0].set_ylabel("y")

axes[1, 1].quiver(
    X[::step_y, ::step_x],
    Y[::step_y, ::step_x],
    U[::step_y, ::step_x],
    V[::step_y, ::step_x],
    SPEED[::step_y, ::step_x],
    cmap="inferno"
)
axes[1, 1].set_title("Velocity vectors")
axes[1, 1].set_xlabel("x")
axes[1, 1].set_ylabel("y")

plt.tight_layout()
plt.savefig(out_dir / "all_fields_2x2.png", dpi=200)
plt.show()

print("Готово. Все картинки сохранены в папку:", out_dir.resolve())