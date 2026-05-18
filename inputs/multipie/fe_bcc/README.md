# Fe MultiPie/SAMB Inputs

This directory documents the MultiPie and SAMB metadata needed for the Fe
multipole decomposition workflow. The full generated SAMB tables and
decomposed HDF5 matrices are generated products and may be too large for Git.

## Purpose

The MultiPie/SAMB stage defines the symmetry-adapted multipole basis used to
decompose the Fe Wannier Hamiltonian. The resulting basis metadata supplies
the `Z` labels used by the multipole-coefficient bar plots and rank-filtered
magnetization-rotation workflows.

## Required Inputs

- TRS-Wannier Hamiltonians from `inputs/symwannier/fe_bcc/`.
- Fe SAMB basis generation settings for the 35-shell decomposition used in
  the manuscript.

## Settings Captured Here

- `Fe.py`: compact MultiPie model definition for the 35-shell spinful Fe
  decomposition.
- `Fe_model.py`: expanded MultiPie model metadata emitted by the production
  Fe basis generation step.
- `samb_manifest.json`: compact manifest of the expected Fe SAMB basis
  metadata, downstream consumers, and generated files.
- `submit_samb.sh`: portable post-processing template for extracting the
  manuscript-selected SAMB labels from a MultiPie output directory.

## Expected Generated Files

The production workflow should generate files analogous to:

- `Fe_samb.py` or `Fe_samb.py.gz`
- `multi_matrix.hdf5`
- `trs_py_ed_hr.hdf5` with `z_coefficients`
- `trs_py_pd_hr.hdf5` with `z_coefficients`
- `trs_tb_hr.hdf5` with `z_coefficients`

Do not commit generated HDF5 files larger than 100 MB. Instead, extract the
compact coefficient table described in
`data/processed/multipole_coefficients/README.md`.
