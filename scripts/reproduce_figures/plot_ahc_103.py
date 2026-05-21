#!/usr/bin/env python3
"""Replot the compact Fe (103) AHC angular-dependence data."""

from __future__ import annotations

import argparse
import math
from pathlib import Path

from _common import (
    DEFAULT_OUTPUT_DIAGNOSTICS,
    DEFAULT_OUTPUT_PAPER,
    PROCESSED,
    plot_methods,
    read_csv,
    require_file,
)


ALPHA = -896.116
BETA = 100.928

PAPER_METHODS = ["Wan90", "SW+ED"]
PAPER_LABELS = {
    "Wan90": "DFT",
    "SW+ED": "model",
    "fitting": "fitting",
}
PAPER_STYLES = {
    "Wan90": {"marker": "o", "linestyle": "None", "color": "black"},
    "SW+ED": {"marker": "s", "linestyle": "None", "color": "tab:blue"},
}
PAPER_YLABELS = {
    "para": r"$\sigma_{\parallel}\ [\mathrm{S/cm}]$",
    "perp": r"$\sigma_{\perp}\ [\mathrm{S/cm}]$",
    "axis": r"$\sigma_{n}\ [\mathrm{S/cm}]$",
}


def theory(component: str) -> tuple[list[float], list[float]]:
    angles = list(range(0, 181))
    radians = [math.radians(angle) for angle in angles]
    if component == "para":
        values = [
            ALPHA + BETA * (273.0 / 400.0 + 9.0 / 100.0 * math.cos(2.0 * angle) + 91.0 / 400.0 * math.cos(4.0 * angle))
            for angle in radians
        ]
    elif component == "perp":
        values = [
            -BETA / 400.0 * (18.0 * math.sin(2.0 * angle) + 91.0 * math.sin(4.0 * angle))
            for angle in radians
        ]
    elif component == "axis":
        values = [6.0 / 25.0 * BETA * math.sin(angle) ** 3 for angle in radians]
    else:
        raise ValueError(component)
    return angles, values


def output_dir_for(style: str) -> Path:
    if style == "paper":
        return DEFAULT_OUTPUT_PAPER / "ahc_103"
    if style == "diagnostic":
        return DEFAULT_OUTPUT_DIAGNOSTICS / "ahc_103"
    raise ValueError(style)


def paper_plot_config(component: str) -> dict[str, object]:
    return {
        "methods": PAPER_METHODS,
        "label_map": PAPER_LABELS,
        "style_map": PAPER_STYLES,
        "title": None,
        "xlabel": r"$\psi\ [\mathrm{deg}]$",
        "ylabel": PAPER_YLABELS[component],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--style", choices=("paper", "diagnostic"), default="paper")
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()

    rows = read_csv(require_file(PROCESSED / "ahc_103" / "ahc_angle_dependence.csv"))
    output_dir = args.output_dir or output_dir_for(args.style)
    outputs = {
        "para": "fit_ahc_para_103.pdf",
        "perp": "fit_ahc_perp_103.pdf",
        "axis": "fit_ahc_axis_103.pdf",
    }
    for component, filename in outputs.items():
        x, y = theory(component)
        if args.style == "paper":
            plot_methods(
                rows,
                component=component,
                output=output_dir / filename,
                extra_curves=[
                    ("fitting", x, y, {"color": "black", "linewidth": 1.6})
                ],
                **paper_plot_config(component),
            )
        else:
            plot_methods(
                rows,
                component=component,
                output=output_dir / filename,
                title=f"Fe (103) sigma_{component}",
                extra_curves=[("cubic fit", x, y)],
            )


if __name__ == "__main__":
    main()
