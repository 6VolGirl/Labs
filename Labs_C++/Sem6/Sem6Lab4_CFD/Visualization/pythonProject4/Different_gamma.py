import pandas as pd
import matplotlib.pyplot as plt
import os

# Базовый путь к папке с результатами
base_dir = r"C:\Users\6anna\PycharmProjects\Labs\Labs_C++\Sem6\Sem6Lab4_CFD\cmake-build-debug"

# Значения гаммы и их отображение для подписей
gammas = ["0_00", "0_01", "0_05", "0_10", "0_50"]
gamma_labels = {g: g.replace('_', '.') for g in gammas}

# Методы: отображение для легенды -> префикс в имени файла
methods = {
    "QUICK": "quick",
    "TVD Superbee": "tvd_superbee",
    "TVD Minmod": "tvd_minmod",
    "Upwind": "upwind"
}

# Цветовая схема для консистентности гамм на всех графиках (опционально)
colors = plt.cm.tab10.colors

plt.rcParams['figure.figsize'] = (8, 6)
plt.rcParams['font.size'] = 11

for method_label, method_prefix in methods.items():
    plt.figure()

    for idx, g in enumerate(gammas):
        filename = f"diag_{method_prefix}_gamma_{g}.csv"
        filepath = os.path.join(base_dir, filename)
        df = pd.read_csv(filepath)

        plt.plot(df["s"], df["phi"],
                 label=f"Gamma = {gamma_labels[g]}",
                 color=colors[idx % len(colors)],
                 linewidth=1.5)

    plt.xlabel("s along diagonal")
    plt.ylabel("phi")
    plt.title(f"Diagonal values for {method_label} scheme at different Gamma")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()

    # Сохраняем каждый график отдельно
    output_name = f"diag_{method_prefix}_gamma_comparison.png"
    plt.savefig(output_name, dpi=300)
    print(f"✓ Сохранён: {output_name}")
    plt.show()