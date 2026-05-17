# Repository Reconstruction Plan

## Purpose

This directory will be reconstructed as the data availability repository for
the manuscript:

> First-principles analysis of in-plane anomalous Hall effect using
> symmetry-adapted Wannier Hamiltonians and multipole decomposition

The main goal is to organize the key computational results from the manuscript
so that external readers can trace and verify them. The target workflow is the
analysis of the in-plane anomalous Hall effect (IAHE) in body-centered cubic
Fe using time-reversal-symmetric Wannier Hamiltonians, symmetry-adapted
multipole basis (SAMB) decomposition, magnetization rotation, rank-resolved
contribution analysis, and strain-effect calculations.

The production calculation workspace is a private reference and must not be
modified during this reconstruction.

## Core Principles

1. Build a public repository containing the code, lightweight test data,
   processed representative data, and figure-generation scripts needed to
   reproduce or verify the manuscript results.
2. Avoid copying the production workspace wholesale. The full calculation tree
   is large, so calculation directories should be reduced to the
   required inputs, lightweight outputs, metadata, and retrieval instructions.
3. Use a test-driven development workflow. Start with small fixtures and tests,
   then port and clean the old code until the tests pass.
4. Prioritize traceability of the research results. Full DFT recomputation is
   not the default target; the repository should instead make the published
   Wannier Hamiltonians, multipole coefficients, AHC summaries, and figure data
   traceable.
5. Separate reusable library code from paper-reproduction scripts. Remove or
   template cluster-specific job scripts, absolute paths, and private
   environment assumptions.

## Planned Public Repository Layout

```text
.
├── README.md
├── LICENSE
├── CITATION.cff
├── pyproject.toml
├── environments/
│   ├── h5py-mpi.yml
│   └── wannierberri.yml
├── src/
│   └── symwan_multipie/
│       ├── multipole.py
│       ├── multipole_decomposition.py
│       ├── single_multipole_reader.py
│       ├── mag_rotation.py
│       ├── energy_diff.py
│       └── wannier_utils/
├── examples/
│   ├── ch4_small/
│   └── fe_bcc/
├── data/
│   ├── processed/
│   └── README.md
├── scripts/
│   ├── reproduce_figures/
│   └── workflow/
├── tests/
│   ├── fixtures/
│   ├── test_multipole_basis.py
│   ├── test_decomposition.py
│   ├── test_mag_rotation.py
│   └── test_energy_diff.py
└── docs/
    ├── workflow.md
    ├── data_inventory.md
    └── paper_mapping.md
```

## Code To Port

The first source files to port from the production workflow are:

- `src/multipole.py`: convert MultiPie `_matrix.pkl` or `_matrix.py` outputs
  into sparse HDF5 multipole-matrix files.
- `src/multipole_decomposition.py`: decompose Wannier Hamiltonians into the
  SAMB basis and write coefficients plus padded matrices to HDF5.
- `src/single_multipole_reader.py`: read selected multipole components from
  HDF5 output files.
- `src/mag_rotation.py`: select multipole components by type, rank, and
  irreducible representation, then generate rotated Hamiltonians.
- `src/energy_diff.py`: evaluate reconstruction errors between the original
  Hamiltonian and the multipole-decomposed Hamiltonian.
- `src/wannier_utils/`: port only the minimum utilities needed for `HamR`, band
  evaluation, and Wannier file parsing.

Cleanup required during porting:

- Remove absolute paths.
- Separate command-line entry points from Python APIs.
- Document the HDF5 schema.
- Allow serial execution for small tests even if production runs use MPI.
- Avoid requiring large files in the default test suite.

## Data Policy

Good candidates for GitHub:

- Small fixtures, such as CH4 or synthetic minimal Hamiltonians that can be
  tested quickly with `pytest`.
- Processed XML, CSV, or JSON files corresponding to manuscript figures.
- Representative multipole-coefficient tables.
- Lightweight data needed by figure-generation scripts.
- Calculation-condition files, input templates, and software-version metadata.
- Any required file below 100 MB, provided it is genuinely useful for
  reproducibility and not an avoidable intermediate.

Files that should not be stored directly in GitHub:

- Full large DFT working directories.
- Any file larger than 100 MB.
- Large HDF5 files, Wannier intermediate files, and full cluster-output logs
  when they can be regenerated.
- Job scripts containing private absolute paths or machine-specific settings.

For files larger than 100 MB, do not use Git, Git LFS, or an external archive
by default. Instead, document the exact procedure needed to generate the file
from smaller committed inputs or from the documented first-principles workflow.
The procedure should be recorded in `data/README.md`, `docs/data_inventory.md`,
or a workflow document under `scripts/workflow/`.

## Test-Driven Development Plan

The initial test suite should cover the following areas.

1. Multipole-basis loading
   - Generate an HDF5 file from `_matrix.pkl` or a small fixture.
   - Check that `shape`, `irvec`, `coords`, and `data` match expectations.

2. Orthogonality and normalization
   - Verify `tr[Z_i^\dagger Z_j] = delta_ij` using a small fixture.

3. Hamiltonian decomposition
   - Decompose a small Hamiltonian into the multipole basis and reconstruct the
     original matrix within tolerance.
   - Confirm that decomposition coefficients `z_i` are real for Hermitian
     Hamiltonians.

4. Magnetization rotation
   - Compare the SU(2) rotation in `mag_rotation.py` with either an analytic
     result or an existing TRS-Wannier reference.
   - Verify that type, rank, and irreducible-representation filters select the
     expected components.

5. Energy-difference regression
   - Check that the band-energy difference between the original and
     reconstructed Hamiltonians is below the threshold for lightweight
     fixtures.

6. Figure-data regression
   - Load the processed data used for manuscript figures.
   - Check key angle points, signs, peak positions, or other compact
     regression values.

## Mapping To Manuscript Results

`docs/paper_mapping.md` should explicitly map manuscript figures and tables to
repository data and scripts.

Expected mappings:

- SAMB decomposition accuracy table: decomposition tests and energy-difference
  outputs.
- Leading multipole-coefficient plots: `z` coefficient HDF5 or CSV files and
  the corresponding plotting scripts.
- `(111)`-plane AHC angular dependence: processed Fe AHC data and figure
  script.
- `(103)`-plane AHC angular dependence: processed Fe AHC data and figure
  script.
- Rank-resolved contributions: rank-filter settings, rotated Hamiltonians, and
  AHC summary data.
- `[103]` strain effect: strain-resolved AHC data and plotting script.
- Minimal `p_z`-`d_xy` model: standalone model script and generated figure
  data.

## Implementation Order

1. Create the repository foundation.
   - Add `README.md`, `pyproject.toml`, `LICENSE`, `CITATION.cff`, and
     `.gitignore`.
   - Create `src/`, `tests/`, `examples/`, `docs/`, and `data/`.

2. Create small fixtures.
   - Use CH4 or a synthetic minimal Hamiltonian small enough for regular tests.
   - If fixtures are derived from production workflow outputs, record their provenance in
     `tests/fixtures/README.md`.

3. Port the core code.
   - Start with `multipole.py` and `single_multipole_reader.py`.
   - Then port `multipole_decomposition.py`.
   - Then port `mag_rotation.py` and `energy_diff.py`.

4. Make the tests pass.
   - Pass serial `pytest` first.
   - Keep MPI/HDF5 parallel writing as optional tests or integration tests
     outside the default CI path.

5. Organize manuscript data.
   - Put processed Fe `(111)`, `(103)`, strain, and rank-resolved data under
     `data/processed/`.
   - Create an inventory instead of copying all large raw data.

6. Clean figure-reproduction scripts.
   - Collect them under `scripts/reproduce_figures/`.
   - Standardize output paths such as `figures/` or `results/figures/`.

7. Write documentation.
   - `README.md`: overview, installation, and shortest reproducibility path.
   - `docs/workflow.md`: DFT-to-AHC workflow.
   - `docs/data_inventory.md`: meaning, source, size, and publication status of
     each data file.
   - `docs/paper_mapping.md`: mapping from manuscript figures and tables to
     repository artifacts.

8. Configure CI.
   - Run only the lightweight fixture tests in GitHub Actions.
   - Document large MPI, WannierBerri, and cluster calculations as local or HPC
     reproduction workflows.

## Completion Criteria

- `pytest` passes on the lightweight fixtures.
- `README.md` explains the repository purpose, required environment, shortest
  test path, and paper-result mapping.
- The main manuscript results can be traced to specific data files and scripts.
- The new repository stands alone for public documentation and lightweight
  validation, without requiring the production calculation workspace.
- The handling of large data is documented in `data/README.md` or
  `docs/data_inventory.md`.

## Immediate Tasks

The next milestone is not more package scaffolding. It is to make the
manuscript figures reproducible from repository artifacts. Work in this order.

1. Build a figure inventory from `main_all.tex`.
   - Extract every `\includegraphics{...}` target.
   - Assign each target a manuscript figure/table label, short description,
     source workflow, expected processed-data file, and
     expected plotting script.
   - Record this in `docs/paper_mapping.md`.

2. Classify each figure by reproducibility level.
   - Level 1: can be reproduced from compact processed data committed to Git.
   - Level 2: needs derived files below 100 MB that may be committed if they
     materially improve reproducibility.
   - Level 3: needs expensive DFT/Wannier/AHC recomputation and should be
     documented as a workflow rather than run in CI. Any required file larger
     than 100 MB belongs here and should be described by generation steps, not
     stored.
   - Store this classification in `docs/data_inventory.md`.

3. Extract processed data for the primary manuscript figures.
   - `(111)` AHC angular dependence: `fit_ahc_para.pdf`,
     `fit_ahc_perp.pdf`, `fit_ahc_axis.pdf`.
   - `(103)` AHC angular dependence: `fit_ahc_para_103.pdf`,
     `fit_ahc_perp_103.pdf`, `fit_ahc_axis_103.pdf`.
   - Rank-resolved `(103)` AHC: `sigma_para_group*.pdf`,
     `sigma_perp_group*.pdf`, `sigma_axis_group*.pdf`,
     `sigma_para.pdf`, `sigma_perp.pdf`, `sigma_axis.pdf`.
   - Strain response: `sigma_plus_strain_sigma_axis.pdf` and
     `sigma_minus_strain_sigma_axis.pdf`.
   - Multipole coefficients: `bar_ed_all_35.pdf`,
     `bar_ed_wo_q_35.pdf`, and the named multipole schematic inputs if they
     can be represented compactly.
   - Minimal model: `sigma_axis_model_1st_nn.pdf` and
     `sigma_axis_model_2nd_nn.pdf`.

4. Standardize processed-data files under `data/processed/`.
   - Prefer CSV for tabular curve data.
   - Use JSON or YAML for plot metadata such as axis labels, units, fitting
     parameters, magnetization plane, strain value, and source path.
   - Include a `README.md` in each processed-data subdirectory explaining how
     the files were extracted from the paper workflow outputs.

5. Add one plotting script per manuscript figure group.
   - Put scripts under `scripts/reproduce_figures/`.
   - Each script should read only `data/processed/` inputs.
   - Each script should write to `results/figures/` or a user-specified output
     directory.
   - The script name should match the paper mapping, for example
     `plot_ahc_111.py`, `plot_ahc_103.py`, `plot_rank_resolved_103.py`,
     `plot_strain_103.py`, `plot_multipole_coefficients.py`, and
     `plot_minimal_model.py`.

6. Add regression tests for figure data.
   - Tests should load each processed-data file.
   - Check compact numerical invariants such as row counts, angle ranges,
     signs, peak or valley locations, and selected reference values.
   - Keep tests lightweight and independent of WannierBerri or full DFT.

7. Document generation procedures for files larger than 100 MB.
   - For each large Hamiltonian, HDF5, Wannier, or AHC intermediate file,
     record the command sequence, input files, software versions, and expected
     output path.
   - Include expected file sizes and checksums only when a local generated copy
     is available.
   - Keep these large generated files out of Git.

8. Only after figure reproduction is traceable, add workflow CLI entry points.
   - Multipole conversion CLI.
   - Hamiltonian decomposition CLI.
   - Magnetization rotation CLI.
   - AHC-summary extraction CLI.

## Current Figure-Reproduction Progress

The repository now contains the exact PDF files referenced by `main_all.tex`
under `figures/paper/`. This satisfies the requirement that the public
repository include the same figures as the manuscript.

Completed compact-data items:

1. Full figure inventory:
   - `data/processed/figure_inventory.csv`
   - `tests/test_paper_figures.py`

2. Primary AHC angular-dependence data:
   - `data/processed/ahc_111/`
   - `data/processed/ahc_103/`
   - `scripts/reproduce_figures/plot_ahc_111.py`
   - `scripts/reproduce_figures/plot_ahc_103.py`

3. Rank-cumulative `(103)` data:
   - `data/processed/rank_resolved_103/`
   - `scripts/reproduce_figures/plot_rank_resolved_103.py`

4. `[103]` strain data:
   - `data/processed/strain_103/`
   - `scripts/reproduce_figures/plot_strain_103.py`

5. Lightweight regression tests:
   - `tests/test_processed_figure_data.py`

Remaining compact-data extraction items:

1. Multipole coefficient CSV for `bar_ed_all_35.pdf` and
   `bar_ed_wo_q_35.pdf`.
2. Single-rank `(103)` AHC CSV for `sigma_para.pdf`, `sigma_perp.pdf`, and
   `sigma_axis.pdf`.
3. Minimal-model CSV for `sigma_axis_model_1st_nn.pdf` and
   `sigma_axis_model_2nd_nn.pdf`.

Files larger than 100 MB remain excluded from Git. Their generation procedures
are documented in `scripts/workflow/generate_large_files.md`.
