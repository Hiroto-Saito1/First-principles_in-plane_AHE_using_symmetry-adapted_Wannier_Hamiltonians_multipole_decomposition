#!/usr/bin/env python3
"""Replot the compact Fe (103) AHC angular-dependence data."""

from __future__ import annotations

import argparse
import math
from pathlib import Path

from _common import DEFAULT_OUTPUT, PROCESSED, plot_methods, read_csv, require_file


ALPHA = -896.116
BETA = 100.928


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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT / "ahc_103")
    args = parser.parse_args()

    rows = read_csv(require_file(PROCESSED / "ahc_103" / "ahc_angle_dependence.csv"))
    outputs = {
        "para": "fit_ahc_para_103.pdf",
        "perp": "fit_ahc_perp_103.pdf",
        "axis": "fit_ahc_axis_103.pdf",
    }
    for component, filename in outputs.items():
        x, y = theory(component)
        plot_methods(
            rows,
            component=component,
            output=args.output_dir / filename,
            title=f"Fe (103) sigma_{component}",
            extra_curves=[("cubic fit", x, y)],
        )


if __name__ == "__main__":
    main()
