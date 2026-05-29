import pandas as pd
import matplotlib.pyplot as plt

files1 = {
    "Upwind": r"C:\Users\6anna\PycharmProjects\Labs\Labs_C++\Sem6\Sem6Lab4_CFD\cmake-build-debug\diag_upwind.csv",
    "TVD Minmod": r"C:\Users\6anna\PycharmProjects\Labs\Labs_C++\Sem6\Sem6Lab4_CFD\cmake-build-debug\diag_tvd_minmod.csv",
    #"TVD VanLeer": r"C:\Users\6anna\PycharmProjects\Labs\Labs_C++\Sem6\Sem6Lab4_CFD\cmake-build-debug\diag_tvd_valeer.csv",
    "TVD Superbee": r"C:\Users\6anna\PycharmProjects\Labs\Labs_C++\Sem6\Sem6Lab4_CFD\cmake-build-debug\diag_tvd_superbee.csv",
    "TVD Quick": r"C:\Users\6anna\PycharmProjects\Labs\Labs_C++\Sem6\Sem6Lab4_CFD\cmake-build-debug\diag_quick.csv",
}

files2 = {
    "Upwind": r"C:\Users\6anna\PycharmProjects\Labs\Labs_C++\Sem6\Sem6Lab4_CFD\cmake-build-debug\task2_diag_tvd_minmod.csv",
    "TVD Minmod": r"C:\Users\6anna\PycharmProjects\Labs\Labs_C++\Sem6\Sem6Lab4_CFD\cmake-build-debug\task2_diag_tvd_superbee.csv",
    #"TVD VanLeer": r"C:\Users\6anna\PycharmProjects\Labs\Labs_C++\Sem6\Sem6Lab4_CFD\cmake-build-debug\task2_diag_tvd_valeer.csv",
    "TVD Superbee": r"C:\Users\6anna\PycharmProjects\Labs\Labs_C++\Sem6\Sem6Lab4_CFD\cmake-build-debug\task2_diag_upwind.csv",
    "TVD Quick": r"C:\Users\6anna\PycharmProjects\Labs\Labs_C++\Sem6\Sem6Lab4_CFD\cmake-build-debug\task2_diag_quick.csv",
}

plt.figure(figsize=(9, 5))

phi_exact_drawn = False

for method, filename in files1.items():
    df = pd.read_csv(filename)
    df = df.sort_values("s")

    plt.plot(
        df["s"],
        df["phi"],
        marker="o",
        markersize=4,
        linewidth=1.6,
        label=method
    )

    if not phi_exact_drawn:
        plt.plot(
            df["s"],
            df["phi_exact"],
            "k--",
            linewidth=2.2,
            label="Exact"
        )
        phi_exact_drawn = True

plt.xlabel("s = x on line y = 1 - x")
plt.ylabel("phi")
plt.title("Comparison of schemes on secondary diagonal")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.show()