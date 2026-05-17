#!/usr/bin/env python3
"""Replot the compact Fe (111) AHC angular-dependence data."""

from __future__ import annotations

import argparse
import math
from pathlib import Path

from _common import DEFAULT_OUTPUT, PROCESSED, plot_methods, read_csv, require_file


ALPHA = -894.308
BETA = 105.758


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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT / "ahc_111")
    args = parser.parse_args()

    rows = read_csv(require_file(PROCESSED / "ahc_111" / "ahc_angle_dependence.csv"))
    outputs = {
        "para": "fit_ahc_para.pdf",
        "perp": "fit_ahc_perp.pdf",
        "axis": "fit_ahc_axis.pdf",
    }
    for component, filename in outputs.items():
        x, y = theory(component)
        plot_methods(
            rows,
            component=component,
            output=args.output_dir / filename,
            title=f"Fe (111) sigma_{component}",
            extra_curves=[("cubic fit", x, y)],
        )


if __name__ == "__main__":
    main()
