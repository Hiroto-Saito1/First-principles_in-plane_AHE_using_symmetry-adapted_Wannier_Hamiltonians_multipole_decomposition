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
    render_notice_panel,
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
PAPER_MODEL_SOURCE = PROCESSED / "ahc_111" / "fit_ahc_angle_dependence.csv"
PAPER_DFT_SOURCE = PROCESSED / "ahc_111" / "fit_ahc_dft_angle_dependence.csv"

PAPER_STYLES = {
    "SW+ED": {"marker": "o", "linestyle": "None", "color": "tab:red", "markersize": 5.0},
    "DFT": {"marker": "D", "linestyle": "--", "color": "black", "markersize": 4.5, "linewidth": 1.0},
}
PAPER_YLABELS = {
    "para": r"$\sigma_{\parallel}$ at $E_F$ [S/cm]",
    "perp": r"$\sigma_{\perp}$ at $E_F$ [S/cm]",
    "axis": r"$\sigma_{n}$ at $E_F$ [S/cm]",
}
PAPER_LEGEND_KWARGS = {"loc": "upper right"}


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
    panel = load_contract(component)
    verified = panel["required_series"] + panel.get("optional_series", [])
    methods = [
        item["source_method"]
        for item in verified
        if item["source_method"] != "analytic_fit"
        and item["verification_status"] == "verified"
    ]
    label_map = {
        item["source_method"]: item["paper_label"]
        for item in verified
        if item["source_method"] != "analytic_fit"
        and item["verification_status"] == "verified"
    }
    style_map = {
        method: PAPER_STYLES[method]
        for method in methods
        if method in PAPER_STYLES
    }
    return {
        "methods": methods,
        "label_map": label_map,
        "style_map": style_map,
        "legend_kwargs": PAPER_LEGEND_KWARGS,
        "title": None,
        "xlabel": r"$\psi\ [\mathrm{deg}]$",
        "ylabel": PAPER_YLABELS[component],
    }


def paper_extra_curves(component: str) -> list[tuple[str, list[float], list[float], dict[str, object]]]:
    panel = load_contract(component)
    x, y = theory(component)
    return [
        ("fitting", x, y, {"color": "tab:red", "linestyle": "--", "linewidth": 1.6})
        for item in panel["required_series"] + panel.get("optional_series", [])
        if item["source_method"] == "analytic_fit" and item["verification_status"] == "verified"
    ]


def paper_notice_lines() -> list[str]:
    return [
        "Paper fit_ahc source recovery is incomplete.",
        "A required compact model or DFT role is missing.",
        "Use diagnostics for raw implementation curves until the role is restored.",
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--style", choices=("paper", "diagnostic"), default="paper")
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()

    diagnostic_rows = read_csv(require_file(PROCESSED / "ahc_111" / "ahc_angle_dependence.csv"))
    paper_rows = (
        read_csv(require_file(PAPER_MODEL_SOURCE))
        + read_csv(require_file(PAPER_DFT_SOURCE))
    )
    output_dir = args.output_dir or output_dir_for(args.style)
    outputs = {
        "para": "fit_ahc_para.pdf",
        "perp": "fit_ahc_perp.pdf",
        "axis": "fit_ahc_axis.pdf",
    }
    for component, filename in outputs.items():
        if args.style == "paper":
            contract = load_contract(component)
            if contract["paper_reproducible"]:
                plot_methods(
                    paper_rows,
                    component=component,
                    output=output_dir / filename,
                    extra_curves=paper_extra_curves(component),
                    **paper_plot_config(component),
                )
            else:
                render_notice_panel(
                    output_dir / filename,
                    title=None,
                    lines=paper_notice_lines(),
                    xlabel=r"$\psi\ [\mathrm{deg}]$",
                    ylabel=PAPER_YLABELS[component],
                )
        else:
            x, y = theory(component)
            plot_methods(
                diagnostic_rows,
                component=component,
                output=output_dir / filename,
                title=f"Fe (111) sigma_{component}",
                extra_curves=[("cubic fit", x, y)],
            )


if __name__ == "__main__":
    main()
