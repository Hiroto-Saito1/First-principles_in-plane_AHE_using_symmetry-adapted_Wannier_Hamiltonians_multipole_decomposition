#!/usr/bin/env python3
"""Centralize figure-generation dependency lists for preflight and tests."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


PAPER_PROCESSED_INPUTS = (
    "data/processed/definitions/bcc_planes.json",
    "data/processed/ahc_111/fit_ahc_angle_dependence.csv",
    "data/processed/ahc_111/fit_ahc_dft_angle_dependence.csv",
    "data/processed/ahc_103/fit_ahc_angle_dependence.csv",
    "data/processed/ahc_103/fit_ahc_dft_angle_dependence.csv",
    "data/processed/band_bond/band_bond_curves.csv",
    "data/processed/rank_resolved_103/rank_resolved_ahc.csv",
    "data/processed/rank_resolved_103/single_rank_ahc.csv",
    "data/processed/strain_103/strain_plus_ahc.csv",
    "data/processed/strain_103/strain_minus_ahc.csv",
    "data/processed/multipole_coefficients/multipole_coefficients.csv",
    "data/processed/minimal_model/model_sigma_axis.csv",
)

DIAGNOSTIC_PROCESSED_INPUTS = (
    "data/processed/ahc_111/ahc_angle_dependence.csv",
    "data/processed/ahc_103/ahc_angle_dependence.csv",
    "data/processed/rank_resolved_103/rank_resolved_ahc.csv",
    "data/processed/rank_resolved_103/single_rank_ahc.csv",
    "data/processed/multipole_coefficients/multipole_coefficients.csv",
)

PAPER_PLOTTING_SCRIPTS = (
    "scripts/reproduce_figures/plot_bcc_planes.py",
    "scripts/reproduce_figures/plot_ahc_111.py",
    "scripts/reproduce_figures/plot_band_bond.py",
    "scripts/reproduce_figures/plot_ahc_103.py",
    "scripts/reproduce_figures/plot_rank_resolved_103.py",
    "scripts/reproduce_figures/plot_strain_103.py",
    "scripts/reproduce_figures/plot_multipole_coefficients.py",
    "scripts/reproduce_figures/plot_minimal_model.py",
)

DIAGNOSTIC_PLOTTING_SCRIPTS = (
    "scripts/reproduce_figures/plot_ahc_111.py",
    "scripts/reproduce_figures/plot_ahc_103.py",
    "scripts/reproduce_figures/plot_rank_resolved_103.py",
    "scripts/reproduce_figures/plot_multipole_coefficients.py",
)

PAPER_SOURCE_DEPENDENCIES = (
    "data/source/README.md",
    "data/source/production_exports/README.md",
    "data/source/production_exports/ahc_111/ahc_angle_dependence.csv",
    "data/source/production_exports/ahc_111/energy_angle_dependence.csv",
    "data/source/production_exports/ahc_111/fit_ahc_angle_dependence.csv",
    "data/source/production_exports/ahc_111/fit_ahc_dft_angle_dependence.csv",
    "data/source/production_exports/ahc_103/ahc_angle_dependence.csv",
    "data/source/production_exports/ahc_103/energy_angle_dependence.csv",
    "data/source/production_exports/ahc_103/fit_ahc_angle_dependence.csv",
    "data/source/production_exports/ahc_103/fit_ahc_dft_angle_dependence.csv",
    "data/source/production_exports/rank_resolved_103/rank_resolved_ahc.csv",
    "data/source/production_exports/rank_resolved_103/rank_cumulative_energy.csv",
    "data/source/production_exports/rank_resolved_103/single_rank_ahc.csv",
    "data/source/production_exports/strain_103/strain_plus_ahc.csv",
    "data/source/production_exports/strain_103/strain_minus_ahc.csv",
    "data/source/production_exports/minimal_model/README.md",
    "data/source/production_exports/minimal_model/model_sigma_axis.csv",
    "data/source/pdf_vector/README.md",
    "data/source/pdf_vector/band_bond/README.md",
    "data/source/pdf_vector/band_bond/band_1.pdf",
    "data/source/pdf_vector/band_bond/band_2.pdf",
    "data/source/pdf_vector/band_bond/band_3.pdf",
    "data/source/pdf_vector/band_bond/band_4.pdf",
    "data/source/pdf_vector/band_bond/band_5.pdf",
    "data/source/pdf_vector/band_bond/band_10.pdf",
    "data/source/pdf_vector/band_bond/band_20.pdf",
    "data/source/pdf_vector/band_bond/band_35.pdf",
    "data/source/pdf_vector/multipole_coefficients/README.md",
    "data/source/pdf_vector/multipole_coefficients/multipole_coefficients.csv",
)

PAPER_CONTRACT_DEPENDENCIES = (
    "data/source/workflow_manifests/ahc/fit_ahc_reference_contract.json",
    "data/source/workflow_manifests/rank_resolved_103/rank_resolved_reference_contract.json",
    "data/source/workflow_manifests/strain_103/strain_reference_contract.json",
    "data/source/workflow_manifests/minimal_model/minimal_model_reference_contract.json",
    "data/source/workflow_manifests/band_bond/band_bond_reference_contract.json",
    "data/source/workflow_manifests/multipole_coefficients/bar_plot_reference_contract.json",
    "data/source/workflow_manifests/definitions/bcc_planes_reference_contract.json",
)

CONTACT_SHEET_SCRIPTS = ("scripts/reproduce_figures/make_paper_contact_sheet.py",)


def inventory_rows(root: Path) -> list[dict[str, str]]:
    with (root / "data/processed/figure_inventory.csv").open(
        newline="", encoding="utf-8"
    ) as handle:
        return list(csv.DictReader(handle))


def included_paper_pdfs(root: Path) -> list[Path]:
    rows = inventory_rows(root)
    return sorted(
        root / row["included_pdf"]
        for row in rows
        if row["reproduction_category"] == "reproducible_plot" and row["included_pdf"]
    )


def dependency_paths(
    root: Path,
    *,
    include_paper: bool,
    include_diagnostics: bool,
    include_contact_sheet: bool,
) -> list[Path]:
    paths: set[Path] = set()

    if include_paper:
        paths.update(root / rel for rel in PAPER_PROCESSED_INPUTS)
        paths.update(root / rel for rel in PAPER_PLOTTING_SCRIPTS)
        paths.update(root / rel for rel in PAPER_SOURCE_DEPENDENCIES)
        paths.update(root / rel for rel in PAPER_CONTRACT_DEPENDENCIES)

    if include_diagnostics:
        paths.update(root / rel for rel in DIAGNOSTIC_PROCESSED_INPUTS)
        paths.update(root / rel for rel in DIAGNOSTIC_PLOTTING_SCRIPTS)

    if include_contact_sheet:
        paths.update(root / rel for rel in CONTACT_SHEET_SCRIPTS)
        paths.update(included_paper_pdfs(root))

    return sorted(paths)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--paper", action="store_true")
    parser.add_argument("--diagnostics", action="store_true")
    parser.add_argument("--contact-sheet", action="store_true")
    args = parser.parse_args()

    for path in dependency_paths(
        args.root,
        include_paper=args.paper,
        include_diagnostics=args.diagnostics,
        include_contact_sheet=args.contact_sheet,
    ):
        print(path)


if __name__ == "__main__":
    main()
