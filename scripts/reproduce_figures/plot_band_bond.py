#!/usr/bin/env python3
"""Plot the Fe band/bond convergence comparison from recovered compact CSV data."""

from __future__ import annotations

import argparse
from pathlib import Path

from _common import DEFAULT_OUTPUT, PROCESSED, get_pyplot, grouped, parse_float, read_csv


XMIN = 92.16
XMAX = 414.72
XTICKS = [92.16, 169.95466, 224.963265, 279.971869, 347.342045, 414.72]
XTICK_POSITIONS = [(value - XMIN) / (XMAX - XMIN) for value in XTICKS]
XTICK_LABELS = [r"$\Gamma$", "H", "N", r"$\Gamma$", "P", "H"]
DEFAULT_CUTOFFS = [1, 2, 3, 4, 5, 10, 35]
PAPER_CUTOFFS = DEFAULT_CUTOFFS
PAPER_SERIES = ["DFT", "model"]
PAPER_YLABEL = r"$E-E_F$ [eV]"
PAPER_XRANGE = (0.0, 1.0)
PAPER_YRANGE = (-10.0, 5.8)


def ordinal(value: int) -> str:
    if 10 <= value % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(value % 10, "th")
    return f"{value}{suffix}"


def grouped_curves(rows: list[dict[str, str]]) -> dict[tuple[str, str], list[dict[str, str]]]:
    curves: dict[tuple[str, str], list[dict[str, str]]] = {}
    for row in rows:
        curves.setdefault((row["series"], row["curve_index"]), []).append(row)
    return curves


def plot_panel(ax, rows: list[dict[str, str]], cutoff: int) -> None:
    handles_done = set()
    style = {
        "model": {"color": "red", "linestyle": "--", "label": "model"},
        "DFT": {"color": "black", "linestyle": "-", "label": "DFT"},
    }
    for (series, _curve_index), curve_rows in grouped_curves(rows).items():
        curve_rows = sorted(curve_rows, key=lambda row: int(row["point_index"]))
        x = [parse_float(row["k_path_fraction"]) for row in curve_rows]
        y = [parse_float(row["energy_ev"]) for row in curve_rows]
        kwargs = style[series].copy()
        if series in handles_done:
            kwargs["label"] = None
        else:
            handles_done.add(series)
        ax.plot(x, y, linewidth=1.3, **kwargs)

    ax.set_title(f"{ordinal(cutoff)} nearest neighbors")
    ax.set_xlim(*PAPER_XRANGE)
    ax.set_ylim(*PAPER_YRANGE)
    ax.set_xticks(XTICK_POSITIONS)
    ax.set_xticklabels(XTICK_LABELS)
    ax.set_ylabel(PAPER_YLABEL)
    ax.grid(True, linewidth=0.4)
    ax.legend(fontsize=8, loc="upper right")


def plot(rows: list[dict[str, str]], output: Path, cutoffs: list[int]) -> None:
    plt = get_pyplot()
    output.parent.mkdir(parents=True, exist_ok=True)
    by_cutoff = grouped(rows, "cutoff_shell")

    figure = plt.figure(figsize=(20.0, 9.0))
    grid = figure.add_gridspec(2, 12, hspace=0.58, wspace=0.6)

    top_spans = {
        1: slice(0, 3),
        2: slice(3, 6),
        3: slice(6, 9),
        4: slice(9, 12),
    }
    bottom_spans = {
        5: slice(0, 3),
        10: slice(4, 7),
        35: slice(9, 12),
    }

    for cutoff, span in top_spans.items():
        if cutoff not in cutoffs:
            continue
        ax = figure.add_subplot(grid[0, span])
        plot_panel(ax, by_cutoff[str(cutoff)], cutoff)

    for cutoff, span in bottom_spans.items():
        if cutoff not in cutoffs:
            continue
        ax = figure.add_subplot(grid[1, span])
        plot_panel(ax, by_cutoff[str(cutoff)], cutoff)

    for position in [3, 8]:
        ax = figure.add_subplot(grid[1, position])
        ax.axis("off")
        ax.text(0.5, 0.5, "...", fontsize=42, ha="center", va="center")

    figure.savefig(output)
    plt.close(figure)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=PROCESSED / "band_bond" / "band_bond_curves.csv",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT / "band_bond",
    )
    parser.add_argument(
        "--cutoffs",
        default="1,2,3,4,5,10,35",
        help="Comma-separated shell cutoffs to include in the composite.",
    )
    args = parser.parse_args()

    if not args.input.is_file():
        raise SystemExit(
            "Missing compact band/bond CSV. See "
            "data/processed/band_bond/README.md and "
            "scripts/workflow/generate_large_files.md."
        )

    cutoffs = [int(value.strip()) for value in args.cutoffs.split(",") if value.strip()]
    rows = read_csv(args.input)
    plot(rows, args.output_dir / "band_bond.pdf", cutoffs)


if __name__ == "__main__":
    main()
