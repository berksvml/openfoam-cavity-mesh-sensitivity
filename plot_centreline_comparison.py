from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


# -----------------------------
# Paths
# -----------------------------
DATA_DIR = Path("data")
OUTPUT_DIR = Path("images")
OUTPUT_DIR.mkdir(exist_ok=True)

# -----------------------------
# CFD case files
# -----------------------------
cases = {
    "40 × 40, Δt = 0.001 s": DATA_DIR / "mesh40_t10.csv",
    "80 × 80, Δt = 0.001 s": DATA_DIR / "mesh80_t10.csv",
    "160 × 160, Δt = 0.0005 s": DATA_DIR / "mesh160_t10.csv",
}

# -----------------------------
# Create figure
# -----------------------------
plt.figure(figsize=(8, 8))

# -----------------------------
# Read and plot CFD results
# -----------------------------
for label, file_path in cases.items():
    if not file_path.exists():
        raise FileNotFoundError(f"Missing file: {file_path}")

    data = pd.read_csv(file_path)

    print(f"\n{file_path.name}")
    print(data.columns.tolist())

    # arc_length column check
    if "arc_length" not in data.columns:
        raise KeyError(
            f"'arc_length' column not found in {file_path}. "
            f"Available columns: {data.columns.tolist()}"
        )

    # Find x-velocity column
    if "U_X" in data.columns:
        ux_column = "U_X"
    elif "U:0" in data.columns:
        ux_column = "U:0"
    elif "U" in data.columns:
        ux_column = "U"
    else:
        raise KeyError(
            f"Could not find the x-velocity column in {file_path}. "
            f"Available columns: {data.columns.tolist()}"
        )

    # Plot CFD line
    plt.plot(
        data[ux_column],
        data["arc_length"],
        linewidth=2.2,
        label=label,
    )

    # Print minimum Ux and its y-location
    min_index = data[ux_column].idxmin()
    min_ux = data.loc[min_index, ux_column]
    min_y = data.loc[min_index, "arc_length"]

    print(f"Minimum Ux = {min_ux:.6f} m/s at y = {min_y:.6f} m")

# -----------------------------
# Read and plot benchmark data
# -----------------------------
benchmark_file = DATA_DIR / "ghia_re10000.csv"

if not benchmark_file.exists():
    raise FileNotFoundError(f"Missing benchmark file: {benchmark_file}")

benchmark = pd.read_csv(benchmark_file)

print(f"\n{benchmark_file.name}")
print(benchmark.columns.tolist())

if "Ux_over_Ulid" not in benchmark.columns or "y_over_L" not in benchmark.columns:
    raise KeyError(
        f"Benchmark file must contain 'Ux_over_Ulid' and 'y_over_L'. "
        f"Available columns: {benchmark.columns.tolist()}"
    )

# Convert y/L to physical y in meters
# Cavity size is 0.1 m, so y = (y/L) * 0.1
plt.scatter(
    benchmark["Ux_over_Ulid"],
    benchmark["y_over_L"] * 0.1,
    marker="o",
    facecolors="none",
    edgecolors="black",
    s=55,
    linewidths=1.5,
    label="Ghia et al. benchmark, Re = 10000",
    zorder=5,
)

# -----------------------------
# Figure formatting
# -----------------------------
plt.xlabel(r"$U_x$ [m/s]", fontsize=14)
plt.ylabel(r"$y$ [m]", fontsize=14)
plt.title(r"Vertical Centreline Velocity Profile at $t = 10$ s", fontsize=18)
plt.grid(True, alpha=0.3)

plt.legend(
    loc="upper center",
    bbox_to_anchor=(0.5, -0.12),
    ncol=2,
    frameon=True,
    fontsize=11,
)

plt.tight_layout()

# -----------------------------
# Save figure
# -----------------------------
output_path = OUTPUT_DIR / "centreline_velocity_comparison_with_benchmark.png"

plt.savefig(
    output_path,
    dpi=300,
    bbox_inches="tight",
)

print(f"\nFigure saved to: {output_path}")

