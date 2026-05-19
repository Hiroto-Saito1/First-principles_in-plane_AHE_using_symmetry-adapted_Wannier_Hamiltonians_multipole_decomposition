#!/usr/bin/env python3
"""Rebuild committed processed CSV files from committed small sources."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

import extract_pdf_vector_data


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "data" / "source"
PROCESSED = ROOT / "data" / "processed"


PRODUCTION_EXPORTS = [
    (
        SOURCE / "production_exports/ahc_111/ahc_angle_dependence.csv",
        PROCESSED / "ahc_111/ahc_angle_dependence.csv",
    ),
    (
        SOURCE / "production_exports/ahc_111/energy_angle_dependence.csv",
        PROCESSED / "ahc_111/energy_angle_dependence.csv",
    ),
    (
        SOURCE / "production_exports/ahc_103/ahc_angle_dependence.csv",
        PROCESSED / "ahc_103/ahc_angle_dependence.csv",
    ),
    (
        SOURCE / "production_exports/ahc_103/energy_angle_dependence.csv",
        PROCESSED / "ahc_103/energy_angle_dependence.csv",
    ),
    (
        SOURCE / "production_exports/rank_resolved_103/rank_resolved_ahc.csv",
        PROCESSED / "rank_resolved_103/rank_resolved_ahc.csv",
    ),
    (
        SOURCE / "production_exports/rank_resolved_103/rank_cumulative_energy.csv",
        PROCESSED / "rank_resolved_103/rank_cumulative_energy.csv",
    ),
    (
        SOURCE / "production_exports/rank_resolved_103/single_rank_ahc.csv",
        PROCESSED / "rank_resolved_103/single_rank_ahc.csv",
    ),
    (
        SOURCE / "production_exports/strain_103/strain_plus_ahc.csv",
        PROCESSED / "strain_103/strain_plus_ahc.csv",
    ),
    (
        SOURCE / "production_exports/strain_103/strain_minus_ahc.csv",
        PROCESSED / "strain_103/strain_minus_ahc.csv",
    ),
]


def copy_export(source: Path, destination: Path) -> None:
    """Copy one committed production export into the processed-data tree."""
    if not source.is_file():
        raise FileNotFoundError(f"Missing source export: {source}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def main() -> None:
    """Rebuild all lightweight processed CSVs."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--skip-pdf-vector",
        action="store_true",
        help="Skip CSV recovery from tracked manuscript vector PDFs.",
    )
    args = parser.parse_args()

    for source, destination in PRODUCTION_EXPORTS:
        copy_export(source, destination)

    if not args.skip_pdf_vector:
        extract_pdf_vector_data.write_band_bond()
        extract_pdf_vector_data.write_multipole_coefficients()
        extract_pdf_vector_data.write_minimal_model()

    print("Rebuilt processed CSV files from committed source data.")


if __name__ == "__main__":
    main()
