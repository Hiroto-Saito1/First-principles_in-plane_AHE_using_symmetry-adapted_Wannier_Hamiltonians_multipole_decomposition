# First-Principles Analysis of In-Plane Anomalous Hall Effect

This repository accompanies the manuscript:

> First-principles analysis of in-plane anomalous Hall effect using
> symmetry-adapted Wannier Hamiltonians and multipole decomposition

Manuscript: [arXiv:2601.05689](https://arxiv.org/abs/2601.05689)

It is intended for readers who want to inspect, reuse, or verify the data
behind the paper. The repository contains the published figures, compact
processed data for the main figure workflows, lightweight tests, and scripts
for reproducing the currently bundled plots.

## What This Repository Contains

- `figures/paper/`: the PDF figures used in the manuscript.
- `data/processed/`: compact CSV and JSON files for figure data.
- `scripts/reproduce_figures/`: plotting scripts that read only
  `data/processed/`.
- `src/symwan_multipie/`: reusable Python utilities for multipole
  decomposition, magnetization rotation, and reconstruction checks.
- `tests/`: lightweight tests for the package and processed figure data.
- `docs/`: workflow notes and figure-to-data mappings.

The complete figure inventory is available at
`data/processed/figure_inventory.csv`.

## Scientific Context

The paper studies the in-plane anomalous Hall effect (IAHE) in body-centered
cubic Fe. The analysis combines first-principles electronic-structure
calculations, symmetry-adapted Wannier Hamiltonians, symmetry-adapted multipole
basis (SAMB) decomposition, magnetization rotation, and intrinsic anomalous
Hall conductivity calculations.

The main result is that high-rank magnetic and magnetic-toroidal multipoles
can contribute to the IAHE with amplitudes comparable to the magnetic-dipole
term. In the `(103)` magnetization-rotation plane, rank-4 magnetic-toroidal
components reshape the out-of-plane Hall response and can act with the
opposite sign. The repository is organized so these data products can be
checked without requiring the full production calculation directory.

## Data Availability

The repository includes compact data for:

- `(111)` AHC angular dependence:
  `data/processed/ahc_111/`
- `(103)` AHC angular dependence:
  `data/processed/ahc_103/`
- rank-cumulative `(103)` AHC contributions:
  `data/processed/rank_resolved_103/`
- tensile and compressive `[103]` strain response:
  `data/processed/strain_103/`

The exact manuscript figure PDFs are included even when the full compact
source table is still being curated. This currently applies to the multipole
coefficient bar plots, the single-rank `(103)` comparison, and the minimal
two-orbital model figures. The generation notes for large or expensive
intermediate files are documented in `scripts/workflow/generate_large_files.md`.

Files larger than 100 MB are not stored in Git. Instead, the repository records
the procedure needed to regenerate them and commits only compact summaries,
metadata, scripts, and final paper figures.

## Quick Start

To inspect the data, no installation is required; the CSV and JSON files can be
opened directly under `data/processed/`.

To run the lightweight tests:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[test]"
pytest
```

To regenerate the bundled data-backed figures, install the plotting
dependencies:

```bash
python -m pip install -e ".[test,plot]"
python scripts/reproduce_figures/plot_ahc_111.py
python scripts/reproduce_figures/plot_ahc_103.py
python scripts/reproduce_figures/plot_rank_resolved_103.py
python scripts/reproduce_figures/plot_strain_103.py
```

Generated figures are written to `results/figures/`, which is intentionally
ignored by Git.

## Figure Mapping

Use these files to connect the manuscript to repository artifacts:

- `data/processed/figure_inventory.csv`: machine-readable figure inventory.
- `docs/paper_mapping.md`: human-readable mapping from manuscript figures to
  data and scripts.
- `docs/data_inventory.md`: status of included data and large generated files.

## Code Scope

The Python package currently provides:

- MultiPie/SAMB sparse HDF5 conversion helpers.
- Hamiltonian decomposition into SAMB components.
- selected multipole reading from HDF5 outputs.
- magnetization rotation utilities for magnetic and magnetic-toroidal
  components.
- reconstruction-error utilities for lightweight validation.
- minimal Wannier Hamiltonian readers and band-evaluation helpers.

The default tests use synthetic fixtures and processed CSV files. They do not
require Quantum ESPRESSO, SymWannier, MultiPie, WannierBerri, MPI, or the full
Fe production data.

## Environment Notes

For larger reproduction workflows, environment templates are provided:

```bash
conda env create -f environments/h5py-mpi.yml
conda env create -f environments/wannierberri.yml
```

These environments are not needed for the default test suite.

## Citation

If this repository helps your work, please cite the associated manuscript and
use the metadata in `CITATION.cff` when citing the repository. The manuscript
preprint is available as [arXiv:2601.05689](https://arxiv.org/abs/2601.05689).
