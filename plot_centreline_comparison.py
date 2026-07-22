from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


DATA_DIR = Path("data")
OUTPUT_DIR = Path("images")
OUTPUT_DIR.mkdir(exist_ok=True)

cases = {
    "40 × 40, Δt = 0.001 s": DATA_DIR / "mesh40_t10.csv",
    "80 × 80, Δt = 0.001 s": DATA_DIR / "mesh80_t10.csv",
    "160 × 160, Δt = 0.0005 s": DATA_DIR / "mesh160_t10.csv",
}

plt.figure(figsize=(7, 7))

for label, file_path in cases.items():
    if not file_path.exists():
        raise FileNotFoundError(f"Missing file: {file_path}")

    data = pd.read_csv(file_path)

    print(f"\n{file_path.name}")
    print(data.columns.tolist())

    if "arc_length" not in data.columns:
        raise KeyError(f"'arc_length' column not found in {file_path}")

    if "U_X" in data.columns:
        ux_column = "U_X"
    elif "U:0" in data.columns:
        ux_column = "U:0"
    else:
        raise KeyError(
            f"Could not find the x-velocity column in {file_path}. "
            f"Available columns: {data.columns.tolist()}"
        )

    plt.plot(
        data[ux_column],
        data["arc_length"],
        linewidth=2,
        label=label,
    )

    min_index = data[ux_column].idxmin()
    min_ux = data.loc[min_index, ux_column]
    min_y = data.loc[min_index, "arc_length"]

    print(f"Minimum Ux = {min_ux:.6f} m/s at y = {min_y:.6f} m")

plt.xlabel(r"$U_x$ [m/s]")
plt.ylabel(r"$y$ [m]")
plt.title(r"Vertical Centreline Velocity Profile at $t=10$ s")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()

output_path = OUTPUT_DIR / "centreline_velocity_comparison.png"
plt.savefig(output_path, dpi=300, bbox_inches="tight")
plt.show()

print(f"\nFigure saved to: {output_path}")
