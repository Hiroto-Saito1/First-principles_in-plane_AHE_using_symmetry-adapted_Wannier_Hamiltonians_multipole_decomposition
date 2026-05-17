#!/usr/bin/env python3
"""Replot compact Fe (103) strain-dependent AHC data."""

from __future__ import annotations

import argparse
from pathlib import Path

from _common import DEFAULT_OUTPUT, PROCESSED, get_pyplot, parse_float, read_csv, require_file


def plot_branch(csv_path: Path, output: Path, title: str) -> None:
    rows = [
        row
        for row in read_csv(require_file(csv_path))
        if row["method"] == "SW+ED"
    ]
    strain_values = sorted({parse_float(row["strain_percent"]) for row in rows})
    plt = get_pyplot()
    output.parent.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(5.2, 3.8))
    for strain in strain_values:
        subset = [
            row
            for row in rows
            if parse_float(row["strain_percent"]) == strain
        ]
        subset.sort(key=lambda row: parse_float(row["phi_deg"]))
        x = [parse_float(row["phi_deg"]) for row in subset]
        y = [parse_float(row["sigma_axis_s_cm"]) for row in subset]
        plt.plot(x, y, marker="o", markersize=3, linewidth=1.2, label=f"{strain:g}%")
    plt.xlabel("psi [deg]")
    plt.ylabel("sigma_axis at E_F [S/cm]")
    plt.title(title)
    plt.xlim(0, 180)
    plt.xticks(range(0, 181, 30))
    plt.grid(True, linewidth=0.4)
    plt.legend(title="strain", fontsize=8)
    plt.tight_layout()
    plt.savefig(output)
    plt.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT / "strain_103")
    args = parser.parse_args()

    plot_branch(
        PROCESSED / "strain_103" / "strain_plus_ahc.csv",
        args.output_dir / "sigma_plus_strain_sigma_axis.pdf",
        "Fe (103) tensile strain",
    )
    plot_branch(
        PROCESSED / "strain_103" / "strain_minus_ahc.csv",
        args.output_dir / "sigma_minus_strain_sigma_axis.pdf",
        "Fe (103) compressive strain",
    )


if __name__ == "__main__":
    main()
