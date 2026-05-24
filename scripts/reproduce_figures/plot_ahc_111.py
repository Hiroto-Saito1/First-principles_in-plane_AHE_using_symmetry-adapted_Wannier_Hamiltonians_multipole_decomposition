#!/usr/bin/env python3
"""Replot the compact Fe (111) AHC angular-dependence data."""

from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import Any

from _common import (
    DEFAULT_OUTPUT_DIAGNOSTICS,
    DEFAULT_OUTPUT_PAPER,
    PROCESSED,
    plot_methods,
    read_json,
    read_csv,
    require_file,
)


ALPHA = -894.308
BETA = 105.758
CONTRACT_PATH = (
    PROCESSED.parents[1]
    / "data"
    / "source"
    / "workflow_manifests"
    / "ahc"
    / "fit_ahc_reference_contract.json"
)

PAPER_METHODS = ["SW+ED", "Wan90"]
PAPER_LABELS = {
    "SW+ED": "model",
    "Wan90": "DFT",
    "fitting": "fitting",
}
PAPER_STYLES = {
    "SW+ED": {"marker": "o", "linestyle": "--", "color": "tab:red"},
    "Wan90": {"marker": "D", "linestyle": "--", "color": "black"},
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
        values = [ALPHA + BETA / 2.0 for _ in angles]
    elif component == "perp":
        values = [0.0 for _ in angles]
    elif component == "axis":
        values = [math.sqrt(6.0) / 6.0 * BETA * math.cos(3.0 * angle) for angle in radians]
    else:
        raise ValueError(component)
    return angles, values


def output_dir_for(style: str) -> Path:
    if style == "paper":
        return DEFAULT_OUTPUT_PAPER / "ahc_111"
    if style == "diagnostic":
        return DEFAULT_OUTPUT_DIAGNOSTICS / "ahc_111"
    raise ValueError(style)


def load_contract(component: str) -> dict[str, Any]:
    manifest = read_json(require_file(CONTRACT_PATH))
    return manifest["panels"][f"111:{component}"]


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

    rows = read_csv(require_file(PROCESSED / "ahc_111" / "ahc_angle_dependence.csv"))
    output_dir = args.output_dir or output_dir_for(args.style)
    outputs = {
        "para": "fit_ahc_para.pdf",
        "perp": "fit_ahc_perp.pdf",
        "axis": "fit_ahc_axis.pdf",
    }
    for component, filename in outputs.items():
        x, y = theory(component)
        if args.style == "paper":
            contract = load_contract(component)
            assert contract["paper_reproducible"] is True
            plot_methods(
                rows,
                component=component,
                output=output_dir / filename,
                extra_curves=[
                    ("fitting", x, y, {"color": "tab:blue", "linestyle": "-", "linewidth": 1.8})
                ],
                **paper_plot_config(component),
            )
        else:
            plot_methods(
                rows,
                component=component,
                output=output_dir / filename,
                title=f"Fe (111) sigma_{component}",
                extra_curves=[("cubic fit", x, y)],
            )


if __name__ == "__main__":
    main()
