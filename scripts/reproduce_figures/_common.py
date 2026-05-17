from __future__ import annotations

import csv
import math
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
PROCESSED = REPO_ROOT / "data" / "processed"
DEFAULT_OUTPUT = REPO_ROOT / "results" / "figures"


def parse_float(value: str) -> float:
    value = value.strip()
    if value.lower() == "nan":
        return math.nan
    return float(value)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def require_file(path: Path) -> Path:
    if not path.is_file():
        raise FileNotFoundError(f"Required input file is missing: {path}")
    return path


def get_pyplot():
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    return plt


def grouped(rows: list[dict[str, str]], key: str) -> dict[str, list[dict[str, str]]]:
    out: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        out.setdefault(row[key], []).append(row)
    return out


def component_column(component: str) -> str:
    return f"sigma_{component}_s_cm"


def sorted_xy(rows: list[dict[str, str]], component: str) -> tuple[list[float], list[float]]:
    rows = sorted(rows, key=lambda row: parse_float(row["phi_deg"]))
    x = [parse_float(row["phi_deg"]) for row in rows]
    y = [parse_float(row[component_column(component)]) for row in rows]
    return x, y


def plot_methods(
    rows: list[dict[str, str]],
    *,
    component: str,
    output: Path,
    title: str,
    methods: list[str] | None = None,
    extra_curves: list[tuple[str, list[float], list[float]]] | None = None,
) -> None:
    plt = get_pyplot()
    output.parent.mkdir(parents=True, exist_ok=True)
    style = {
        "Wan90": {"marker": "o", "linestyle": "None"},
        "SW+ED": {"marker": "s", "linestyle": "-"},
        "SW+PD": {"marker": "^", "linestyle": "--"},
    }

    by_method = grouped(rows, "method")
    selected = methods or list(by_method)
    plt.figure(figsize=(5.0, 3.6))
    for method in selected:
        if method not in by_method:
            continue
        x, y = sorted_xy(by_method[method], component)
        kwargs = style.get(method, {"marker": "o", "linestyle": "-"})
        plt.plot(x, y, label=method, markersize=4, linewidth=1.4, **kwargs)
    if extra_curves:
        for label, x, y in extra_curves:
            plt.plot(x, y, label=label, color="black", linewidth=1.2)
    plt.xlabel("psi [deg]")
    plt.ylabel(f"sigma_{component} at E_F [S/cm]")
    plt.title(title)
    plt.xlim(0, 180)
    plt.xticks(range(0, 181, 30))
    plt.grid(True, linewidth=0.4)
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(output)
    plt.close()
