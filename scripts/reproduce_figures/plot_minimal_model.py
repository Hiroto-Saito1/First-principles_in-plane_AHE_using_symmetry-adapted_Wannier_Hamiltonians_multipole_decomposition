#!/usr/bin/env python3
"""Plot minimal-model sigma_axis scans from compact CSV data."""

from __future__ import annotations

import argparse
from pathlib import Path

from _common import DEFAULT_OUTPUT, PROCESSED, get_pyplot, parse_float, read_csv


PAPER_XLABEL = r"$\psi\ [\mathrm{deg}]$"
PAPER_YLABEL = r"$\sigma_{\mathbf{n}}$ at $E_F$ [S/cm]"
SCAN_OUTPUTS = {
    "first_nn": "sigma_axis_model_1st_nn.pdf",
    "second_nn": "sigma_axis_model_2nd_nn.pdf",
}
SCAN_LABELS = {
    "first_nn": {
        "varying_symbol": r"t^{(1)}_{\mathrm{T}}",
        "fixed_symbol": r"t^{(2)}_{\mathrm{T}}",
        "fixed_value": 0.0,
    },
    "second_nn": {
        "varying_symbol": r"t^{(2)}_{\mathrm{T}}",
        "fixed_symbol": r"t^{(1)}_{\mathrm{T}}",
        "fixed_value": 0.2,
    },
}


def format_parameter_label(scan: str, parameter: float) -> str:
    symbol = SCAN_LABELS[scan]["varying_symbol"]
    return rf"${symbol}={parameter:g}$"


def plot_scan(rows, scan: str, output: Path) -> None:
    subset = [row for row in rows if row["scan"] == scan]
    parameters = sorted({parse_float(row["parameter_value"]) for row in subset})
    plt = get_pyplot()
    output.parent.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(5.2, 3.8))
    for parameter in parameters:
        series = [row for row in subset if parse_float(row["parameter_value"]) == parameter]
        series.sort(key=lambda row: parse_float(row["phi_deg"]))
        x = [parse_float(row["phi_deg"]) for row in series]
        y = [parse_float(row["sigma_axis"]) for row in series]
        plt.plot(
            x,
            y,
            marker="o",
            markersize=3,
            linewidth=1.2,
            label=format_parameter_label(scan, parameter),
        )
    plt.xlabel(PAPER_XLABEL)
    plt.ylabel(PAPER_YLABEL)
    plt.xlim(0, 180)
    plt.xticks(range(0, 181, 30))
    plt.grid(True, linewidth=0.4)
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(output)
    plt.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=PROCESSED / "minimal_model" / "model_sigma_axis.csv")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT / "minimal_model")
    args = parser.parse_args()

    if not args.input.is_file():
        raise SystemExit(
            "Missing compact minimal-model CSV. See "
            "data/processed/minimal_model/README.md."
        )
    rows = read_csv(args.input)
    plot_scan(rows, "first_nn", args.output_dir / SCAN_OUTPUTS["first_nn"])
    plot_scan(rows, "second_nn", args.output_dir / SCAN_OUTPUTS["second_nn"])


if __name__ == "__main__":
    main()
