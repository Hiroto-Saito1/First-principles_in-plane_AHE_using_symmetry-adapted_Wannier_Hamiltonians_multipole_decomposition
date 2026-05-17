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

The present files are:

- `main_all.tex`: manuscript source.
- `main_all.pdf`: compiled manuscript.
- `plan.md`: reconstruction plan for the public repository.
- `README.md`: this overview.

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
- Clear instructions for large data that cannot be stored directly in Git.

The repository is not intended to contain every raw DFT or cluster-output
file. Large intermediate files should be represented by metadata, processed
outputs, or external archive links.

## Planned Code Components

The core implementation will be reconstructed from the old repository and
cleaned for publication:

- `multipole.py`: convert MultiPie multipole matrices to sparse HDF5 files.
- `multipole_decomposition.py`: decompose Wannier Hamiltonians into SAMB
  components and write coefficients and padded matrices to HDF5.
- `single_multipole_reader.py`: read selected multipole components from large
  HDF5 files.
- `mag_rotation.py`: rotate selected magnetic and magnetic-toroidal multipole
  components by rank, type, and irreducible representation.
- `energy_diff.py`: evaluate reconstruction errors between the original and
  multipole-decomposed Hamiltonians.
- `wannier_utils/`: minimal utilities for reading Wannier Hamiltonians and
  evaluating bands.

The final code should avoid absolute paths, separate command-line interfaces
from library APIs, and support small serial tests even if large production
jobs use MPI.

## Testing Policy

This repository will be built using a test-driven workflow. The initial test
suite should cover:

- HDF5 conversion of small multipole matrix fixtures.
- Orthogonality and normalization of the multipole basis.
- Reconstruction of a small Hamiltonian from multipole coefficients.
- Hermiticity and real-valued decomposition coefficients.
- Magnetization rotation against analytic or existing TRS-Wannier reference
  results.
- Energy-difference regression tests for lightweight fixtures.
- Basic figure-data loading and sanity checks for the processed Fe results.

Large MPI, WannierBerri, and full DFT workflows should be documented as
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

1. Create the package skeleton under `src/symwan_multipie/`.
2. Add `pyproject.toml`, `.gitignore`, license, and citation metadata.
3. Copy and clean the core source files from the old repository.
4. Create minimal fixtures and write the first pytest tests.
5. Build `docs/data_inventory.md` to decide which Fe data are small enough for
   GitHub and which should be archived externally.

## Notes

The old repository contains a mix of reusable code, calculation examples,
cluster job scripts, generated outputs, and large intermediate data. During
this reconstruction, only the parts needed for a clean public data repository
should be copied here. The old repository should remain unchanged.
