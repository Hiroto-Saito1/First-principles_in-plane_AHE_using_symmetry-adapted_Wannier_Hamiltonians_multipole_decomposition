from __future__ import annotations

import csv
import math
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
PROCESSED = REPO_ROOT / "data" / "processed"
DEFAULT_OUTPUT_PAPER = REPO_ROOT / "results" / "figures_paper"
DEFAULT_OUTPUT_DIAGNOSTICS = REPO_ROOT / "results" / "figures_diagnostics"
DEFAULT_OUTPUT = DEFAULT_OUTPUT_PAPER


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
    title: str | None,
    methods: list[str] | None = None,
    extra_curves: list[
        tuple[str, list[float], list[float]]
        | tuple[str, list[float], list[float], dict[str, object]]
    ]
    | None = None,
    label_map: dict[str, str] | None = None,
    style_map: dict[str, dict[str, object]] | None = None,
    xlabel: str = "psi [deg]",
    ylabel: str | None = None,
) -> None:
    plt = get_pyplot()
    output.parent.mkdir(parents=True, exist_ok=True)
    style = {
        "Wan90": {"marker": "o", "linestyle": "None"},
        "SW+ED": {"marker": "s", "linestyle": "-"},
        "SW+PD": {"marker": "^", "linestyle": "--"},
    }
    style.update(style_map or {})

    by_method = grouped(rows, "method")
    selected = methods or list(by_method)
    plt.figure(figsize=(5.0, 3.6))
    for method in selected:
        if method not in by_method:
            continue
        x, y = sorted_xy(by_method[method], component)
        kwargs = style.get(method, {"marker": "o", "linestyle": "-"})
        label = (label_map or {}).get(method, method)
        plt.plot(x, y, label=label, markersize=4, linewidth=1.4, **kwargs)
    if extra_curves:
        for curve in extra_curves:
            if len(curve) == 3:
                label, x, y = curve
                kwargs = {"color": "black", "linewidth": 1.2}
            else:
                label, x, y, kwargs = curve
                kwargs = {"color": "black", "linewidth": 1.2, **kwargs}
            label = (label_map or {}).get(label, label)
            plt.plot(x, y, label=label, **kwargs)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel or f"sigma_{component} at E_F [S/cm]")
    if title:
        plt.title(title)
    plt.xlim(0, 180)
    plt.xticks(range(0, 181, 30))
    plt.grid(True, linewidth=0.4)
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(output)
    plt.close()
