import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ---- 1. Путь к файлу ----
file_name1 = r"C:\Users\6anna\PycharmProjects\Labs\Labs_C++\Sem6\Sem6Lab4_CFD\cmake-build-debug\case_L4_constant_profile.csv"
file_name2 = r"C:\Users\6anna\PycharmProjects\Labs\Labs_C++\Sem6\Sem6Lab4_CFD\cmake-build-debug\case_L4_poiseuille_profile.csv"
#file_name1 = r"C:\Users\6anna\PycharmProjects\Labs\Labs_C++\Sem6\Sem6Lab4_CFD\cmake-build-debug\case_L4_constant_profilesave.csv"
#file_name2 = r"C:\Users\6anna\PycharmProjects\Labs\Labs_C++\Sem6\Sem6Lab4_CFD\cmake-build-debug\case_L4_poiseuille_profilesave.csv"
out_dir = Path("plots")
out_dir.mkdir(exist_ok=True)

# ---- 2. Чтение CSV ----
df = pd.read_csv(file_name1)

# Если в файле есть лишние пробелы в названиях столбцов
df.columns = [c.strip() for c in df.columns]

# Ожидаемые столбцы:
# x,y,u_numeric,v_numeric,speed_numeric,p,u_theory,abs_error

# Приводим к числам и удаляем плохие строки
numeric_cols = ["x", "y", "u_numeric", "v_numeric", "speed_numeric", "p", "u_theory", "abs_error"]
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna(subset=numeric_cols).copy()

# Сортировка для красивых графиков
df = df.sort_values(["x", "y"]).reset_index(drop=True)

# Иногда в profile-файле x немного отличается из-за выбора ближайших ячеек.
# Поэтому группируем близкие x через округление.
df["x_group"] = df["x"].round(3)

# ---- 3. График: u_numeric и u_theory от y ----
plt.figure(figsize=(8, 6))

for xg, group in df.groupby("x_group"):
    group = group.sort_values("y")
    plt.plot(group["u_numeric"], group["y"], marker="o", linewidth=1.5, label=f"u_numeric, x={xg}")

# Теорию рисуем один раз по среднему профилю, если она одинакова для всех x-групп
theory_df = (
    df.groupby("y", as_index=False)["u_theory"]
    .mean()
    .sort_values("y")
)
plt.plot(theory_df["u_theory"], theory_df["y"],
         color="black", linestyle="--", linewidth=2.0, label="u_theory")

plt.xlabel("u")
plt.ylabel("y")
plt.title("Профиль скорости: численный и теоретический")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig(out_dir / "u_profile.png", dpi=200)
plt.show()

# ---- 4. График: абсолютная ошибка от y ----
plt.figure(figsize=(8, 6))

for xg, group in df.groupby("x_group"):
    group = group.sort_values("y")
    plt.plot(group["abs_error"], group["y"], marker="o", linewidth=1.5, label=f"abs_error, x={xg}")

plt.xlabel("Absolute error")
plt.ylabel("y")
plt.title("Абсолютная ошибка профиля скорости")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig(out_dir / "abs_error_profile.png", dpi=200)
plt.show()

# ---- 5. График: давление от y ----
plt.figure(figsize=(8, 6))

for xg, group in df.groupby("x_group"):
    group = group.sort_values("y")
    plt.plot(group["p"], group["y"], marker="o", linewidth=1.5, label=f"p, x={xg}")

plt.xlabel("p")
plt.ylabel("y")
plt.title("Давление по профилю")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig(out_dir / "pressure_profile.png", dpi=200)
plt.show()

# ---- 6. График: speed_numeric от y ----
plt.figure(figsize=(8, 6))

for xg, group in df.groupby("x_group"):
    group = group.sort_values("y")
    plt.plot(group["speed_numeric"], group["y"], marker="o", linewidth=1.5, label=f"speed, x={xg}")

plt.xlabel("Speed")
plt.ylabel("y")
plt.title("Модуль скорости по профилю")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig(out_dir / "speed_profile.png", dpi=200)
plt.show()

# ---- 7. Дополнительно: диаграмма рассеяния x-y, цвет = abs_error ----
plt.figure(figsize=(8, 5))
sc = plt.scatter(df["x"], df["y"], c=df["abs_error"], cmap="viridis", s=50)
plt.colorbar(sc, label="abs_error")
plt.xlabel("x")
plt.ylabel("y")
plt.title("Распределение ошибки в точках профиля")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(out_dir / "error_scatter_xy.png", dpi=200)
plt.show()

print("Готово. Картинки сохранены в папку:", out_dir.resolve())