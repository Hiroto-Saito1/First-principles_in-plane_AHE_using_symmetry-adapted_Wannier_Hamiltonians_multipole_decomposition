#!/usr/bin/env python3
"""Export compact minimal-model scans from archived AHC text outputs."""

from __future__ import annotations

import argparse
import csv
from math import sqrt
from pathlib import Path


SCAN_LAYOUT = {
    "first_nn": "1st_nn_t2_0",
    "second_nn": "2nd_nn_t1_0.2",
}
AXIS = (1.0 / sqrt(10.0), 0.0, 3.0 / sqrt(10.0))
DEFAULT_SIGMA_FILE = "sigma_ahc_eta1.00meV.txt"


def sigma_axis_from_file(path: Path, fermi_energy: float) -> float:
    """Return the out-of-plane AHC projected onto the `(103)` plane normal."""
    best_distance: float | None = None
    best_sigma_axis: float | None = None
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.startswith("#") or not line.strip():
                continue
            energy, sigma_xy, sigma_yz, sigma_zx = map(float, line.split())
            sigma_axis = sigma_yz * AXIS[0] + sigma_zx * AXIS[1] + sigma_xy * AXIS[2]
            distance = abs(energy - fermi_energy)
            if best_distance is None or distance < best_distance:
                best_distance = distance
                best_sigma_axis = sigma_axis
    if best_sigma_axis is None:
        raise ValueError(f"No numeric AHC rows found in {path}")
    return best_sigma_axis


def collect_rows(source_root: Path, sigma_filename: str, fermi_energy: float) -> list[dict[str, str]]:
    """Collect compact scan rows from the archived minimal-model source tree."""
    rows: list[dict[str, str]] = []
    for scan, source_tree in SCAN_LAYOUT.items():
        base = source_root / source_tree
        if not base.is_dir():
            raise FileNotFoundError(f"Missing minimal-model source directory: {base}")
        for sigma_path in sorted(base.rglob(sigma_filename)):
            relative = sigma_path.relative_to(base)
            if len(relative.parts) != 3:
                continue
            parameter_dir, psi_dir, _ = relative.parts
            parameter_value = float(parameter_dir.removeprefix("t_T_"))
            phi_deg = float(psi_dir.removeprefix("psi_"))
            sigma_axis = sigma_axis_from_file(sigma_path, fermi_energy)
            rows.append(
                {
                    "scan": scan,
                    "parameter_value": f"{parameter_value:g}",
                    "phi_deg": f"{phi_deg:g}",
                    "sigma_axis": f"{sigma_axis:.8f}",
                    "source_tree": source_tree,
                    "source_file": relative.as_posix(),
                }
            )
    rows.sort(
        key=lambda row: (
            row["scan"],
            float(row["parameter_value"]),
            float(row["phi_deg"]),
        )
    )
    return rows


def main() -> None:
    """Write the compact minimal-model CSV used by the paper figure scripts."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source-root",
        type=Path,
        required=True,
        help="Archived `bcc_model/` root containing `1st_nn_t2_0/` and `2nd_nn_t1_0.2/`.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Destination CSV path.",
    )
    parser.add_argument(
        "--sigma-file",
        default=DEFAULT_SIGMA_FILE,
        help=f"AHC text filename to read in each `psi_*` directory. Default: {DEFAULT_SIGMA_FILE}",
    )
    parser.add_argument(
        "--fermi-energy",
        type=float,
        default=0.0,
        help="Fermi energy in eV used to select the nearest AHC row. Default: 0.0",
    )
    args = parser.parse_args()

    rows = collect_rows(args.source_root, args.sigma_file, args.fermi_energy)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "scan",
                "parameter_value",
                "phi_deg",
                "sigma_axis",
                "source_tree",
                "source_file",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows to {args.output}")


if __name__ == "__main__":
    main()
