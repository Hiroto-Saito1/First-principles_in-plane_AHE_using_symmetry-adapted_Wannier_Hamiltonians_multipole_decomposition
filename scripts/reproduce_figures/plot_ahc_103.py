#!/usr/bin/env python3
"""Replot the compact Fe (103) AHC angular-dependence data."""

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


ALPHA = -896.116
BETA = 100.928
CONTRACT_PATH = (
    PROCESSED.parents[1]
    / "data"
    / "source"
    / "workflow_manifests"
    / "ahc"
    / "fit_ahc_reference_contract.json"
)
PAPER_MODEL_SOURCE = PROCESSED / "ahc_103" / "fit_ahc_angle_dependence.csv"
PAPER_DFT_SOURCE = PROCESSED / "ahc_103" / "fit_ahc_dft_angle_dependence.csv"

PAPER_STYLES = {
    "SW+ED": {
        "marker": "o",
        "linestyle": "-",
        "color": "tab:red",
        "markersize": 5.0,
        "linewidth": 1.6,
    },
    "DFT": {
        "marker": "D",
        "linestyle": "None",
        "color": "black",
        "markersize": 4.5,
    },
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


def load_contract(component: str) -> dict[str, Any]:
    manifest = read_json(require_file(CONTRACT_PATH))
    return manifest["panels"][f"103:{component}"]


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
        ("fitting", x, y, {"color": "tab:blue", "linestyle": "-", "linewidth": 1.8})
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

    output_dir = args.output_dir or output_dir_for(args.style)
    paper_rows = None
    diagnostic_rows = None
    if args.style == "paper":
        paper_rows = (
            read_csv(require_file(PAPER_MODEL_SOURCE))
            + read_csv(require_file(PAPER_DFT_SOURCE))
        )
    else:
        diagnostic_rows = read_csv(
            require_file(PROCESSED / "ahc_103" / "ahc_angle_dependence.csv")
        )
    outputs = {
        "para": "fit_ahc_para_103.pdf",
        "perp": "fit_ahc_perp_103.pdf",
        "axis": "fit_ahc_axis_103.pdf",
    }
    for component, filename in outputs.items():
        if args.style == "paper":
            assert paper_rows is not None
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
            assert diagnostic_rows is not None
            x, y = theory(component)
            plot_methods(
                diagnostic_rows,
                component=component,
                output=output_dir / filename,
                title=f"Fe (103) sigma_{component}",
                extra_curves=[("cubic fit", x, y)],
            )


if __name__ == "__main__":
    main()
