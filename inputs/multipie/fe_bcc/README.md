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
- `pwscf_py_ed_tb.hdf5` with `z_coefficients`
- `pwscf_py_pd_tb.hdf5` with `z_coefficients`
- `trs_py_ed_tb.hdf5` with `z_coefficients`
- `pwscf_tb.hdf5` with `z_coefficients`

Do not commit generated HDF5 files larger than 100 MB. Instead, extract the
compact coefficient table described in
`data/processed/multipole_coefficients/README.md`.

## Typical HDF5 Build Step

After MultiPie emits a matrix dictionary such as `Fe_all_35_matrix.py`,
`Fe_all_35_matrix.pkl`, or the gzipped variants, convert it to the compact
basis HDF5 used by the public decomposition workflow:

```bash
python scripts/workflow/build_multipole_hdf5.py --matrix-path Fe_all_35_matrix.py --output multi_matrix.hdf5
```

For compatibility with the archived production job scripts, the package also
supports the original direct module entry point:

```bash
python src/symwan_multipie/multipole.py Fe_matrix.pkl
```

When `--output` is omitted, this writes `Fe_matrix.hdf5` next to the input
matrix dictionary, matching the archived `submit.sh` workflow.

That file is then consumed by
`inputs/symwannier/fe_bcc/decompose_ham.py` to generate decomposition HDF5
files with the `z_coefficients` dataset. The archived manuscript bar-plot
workflow reads those decomposition HDF5 files together with `Fe_samb.py`.

For the full `Fe_all_35` rebuild path from `Fe.py` through
`Fe_matrix.pkl`, `Fe_matrix.hdf5`, and `trs_py_ed_tb.hdf5`, see
`data/source/workflow_manifests/multipole_coefficients/Fe_all_35_recipe.md`.
