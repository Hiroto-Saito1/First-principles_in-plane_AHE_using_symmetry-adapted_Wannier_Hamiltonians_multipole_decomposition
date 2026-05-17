# First-Principles Analysis of In-Plane Anomalous Hall Effect

This repository is being reconstructed as the data-availability and
reproducibility repository for the manuscript:

> First-principles analysis of in-plane anomalous Hall effect using
> symmetry-adapted Wannier Hamiltonians and multipole decomposition

The repository will collect the scripts, lightweight test data, processed
results, and documentation needed to trace the calculations reported in the
paper. The main target system is body-centered cubic Fe, where the in-plane
anomalous Hall effect (IAHE) is analyzed using time-reversal-symmetric
Wannier Hamiltonians and a symmetry-adapted multipole basis.

## Current Status

This directory is currently a reconstruction workspace, not yet a finished
public code repository.

The current repository contains:

- `main_all.tex`: manuscript source.
- `main_all.pdf`: compiled manuscript.
- `plan.md`: reconstruction plan for the public repository.
- `figures/paper/`: exact PDF figure files referenced by `main_all.tex`.
- `data/processed/`: compact CSV/JSON data extracted for the manuscript
  figure workflows that can be reproduced without large raw calculations.
- `scripts/reproduce_figures/`: plotting scripts that read
  `data/processed/` and write regenerated figures under `results/figures/`.
- `src/symwan_multipie/`: initial Python package for multipole HDF5
  conversion, multipole decomposition, magnetization rotation, and
  reconstruction-error checks.
- `tests/`: lightweight synthetic fixtures and pytest coverage for the core
  workflow.
- `docs/`: workflow, data-inventory, and manuscript-mapping notes.

The original working repository is used only as a read-only reference. It
should not be modified during this reconstruction.

```text
/Users/hirotosaito/Library/CloudStorage/Dropbox/AnacondaProjects/是常研究室/2024/github_projects/symwan_multipie
```

## Scientific Scope

The project studies the microscopic origin of the IAHE in ferromagnets. The
paper combines the following components:

- First-principles electronic-structure calculations for bcc Fe.
- Symmetry-adapted Wannier Hamiltonians constructed with SymWannier.
- Time-reversal-symmetric Wannier gauge fixing for magnetization rotation.
- Symmetry-adapted multipole basis (SAMB) generated with MultiPie.
- Multipole decomposition of the Wannier Hamiltonian into electric,
  magnetic, magnetic toroidal, and electric toroidal components.
- Intrinsic anomalous Hall conductivity calculations using WannierBerri.

The main physical result is that high-rank magnetic and magnetic-toroidal
multipoles can contribute to IAHE with amplitudes comparable to the magnetic
dipole contribution. In the `(103)` magnetization-rotation plane, magnetic
toroidal rank-4 components reshape the out-of-plane AHC response and can act
with the opposite sign. The manuscript further shows that uniaxial strain
along `[103]` can tune this response and even invert its sign.

## Installation

For lightweight development and tests:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[test]"
pytest
```

Conda environment templates are also provided:

```bash
conda env create -f environments/h5py-mpi.yml
conda env create -f environments/wannierberri.yml
```

The default tests use synthetic fixtures and do not require full Fe production
data, Quantum ESPRESSO, SymWannier, MultiPie, or WannierBerri.

## Intended Repository Goals

The reconstructed repository should make the paper results traceable without
requiring the full private working directory. In particular, it should provide:

- A clean Python package for multipole decomposition and magnetization
  rotation of Wannier Hamiltonians.
- Small test fixtures for fast automated tests.
- Processed data used for the manuscript figures.
- Figure reproduction scripts.
- Documentation connecting each paper figure or table to the corresponding
  data and script.
- Clear generation procedures for files larger than 100 MB.

The repository is not intended to contain every raw DFT or cluster-output
file. Large intermediate files should be represented by metadata, processed
outputs, or generation procedures. Files larger than 100 MB are not stored in
this repository by default.

## Paper Figures

The same PDF figures used by the manuscript are included in `figures/paper/`.
The complete figure inventory is stored in
`data/processed/figure_inventory.csv`.

To regenerate the figures that already have compact processed data:

```bash
python scripts/reproduce_figures/plot_ahc_111.py
python scripts/reproduce_figures/plot_ahc_103.py
python scripts/reproduce_figures/plot_rank_resolved_103.py
python scripts/reproduce_figures/plot_strain_103.py
```

Generated outputs are written under `results/figures/` and are intentionally
ignored by Git.

## Implemented Code Components

The initial implementation has been reconstructed from the old repository's
responsibilities and cleaned for publication-oriented tests:

- `multipole.py`: converts MultiPie multipole matrices to sparse HDF5 files.
- `multipole_decomposition.py`: decomposes Wannier Hamiltonians into SAMB
  components and write coefficients and padded matrices to HDF5.
- `single_multipole_reader.py`: reads selected multipole components from large
  HDF5 files.
- `mag_rotation.py`: rotates selected magnetic and magnetic-toroidal multipole
  components by rank, type, and irreducible representation.
- `energy_diff.py`: evaluates reconstruction errors between the original and
  multipole-decomposed Hamiltonians.
- `wannier_utils/`: provides minimal utilities for reading Wannier Hamiltonians and
  evaluating bands.

This initial version avoids absolute paths and supports small serial tests.
Large production workflows can still use MPI-oriented scripts later, but those
should remain outside the default CI path.

## Testing Policy

This repository is being built using a test-driven workflow. The current test
suite covers:

- HDF5 conversion of small multipole matrix fixtures.
- Orthogonality and normalization of the multipole basis.
- Reconstruction of a small Hamiltonian from multipole coefficients.
- Hermiticity and real-valued decomposition coefficients.
- Magnetization rotation against analytic or existing TRS-Wannier reference
  results.
- Energy-difference regression tests for lightweight fixtures.
- Basic figure-data loading and sanity checks for the processed Fe results.

Large MPI, WannierBerri, and full DFT workflows are documented as
integration or reproduction workflows rather than required for every CI run.

## Planned Layout

```text
.
├── README.md
├── plan.md
├── pyproject.toml
├── environments/
├── src/
│   └── symwan_multipie/
├── tests/
│   └── fixtures/
├── examples/
├── data/
│   └── processed/
├── scripts/
│   └── reproduce_figures/
└── docs/
    ├── workflow.md
    ├── data_inventory.md
    └── paper_mapping.md
```

See `plan.md` for the detailed reconstruction strategy.

## Immediate Next Steps

1. Extract compact multipole-coefficient CSV data from the decomposed HDF5
   outputs used for `bar_ed_all_35.pdf` and `bar_ed_wo_q_35.pdf`.
2. Extract compact single-rank `(103)` AHC data for `sigma_para.pdf`,
   `sigma_perp.pdf`, and `sigma_axis.pdf`.
3. Add compact minimal-model CSV data for the two model figures.
4. Add CLI entry points for conversion, decomposition, and rotation workflows.
5. Expand the lightweight synthetic fixtures with a reduced CH4 fixture.

## Notes

The old repository contains a mix of reusable code, calculation examples,
cluster job scripts, generated outputs, and large intermediate data. During
this reconstruction, only the parts needed for a clean public data repository
should be copied here. The old repository should remain unchanged.
