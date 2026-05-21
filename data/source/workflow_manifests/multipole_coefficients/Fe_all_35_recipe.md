# `Fe_all_35` Multipole Basis Recipe

This note explains how to regenerate the missing `Fe_all_35` matrix pickle and
the HDF5 files derived from it. The exact old MultiPie launcher is not bundled
in this repository, but the configuration file, downstream conversion scripts,
and archived log evidence are all preserved here.

## Goal

Rebuild the archived chain:

```text
Fe.py
  -> Fe_model.py
  -> Fe_samb.py
  -> Fe_matrix.pkl
  -> Fe_matrix.hdf5
  -> trs_py_ed_tb.hdf5
  -> compact coefficient CSV
```

## Inputs

- MultiPie configuration:
  [inputs/multipie/fe_bcc/Fe.py](/Users/hirotosaito/Library/CloudStorage/Dropbox/AnacondaProjects/是常研究室/2025/github_projects/First-principles analysis of in-plane anomalous Hall effect using symmetry-adapted Wannier Hamiltonians and multipole decomposition/inputs/multipie/fe_bcc/Fe.py)
- Public matrix-to-HDF5 wrapper:
  [scripts/workflow/build_multipole_hdf5.py](/Users/hirotosaito/Library/CloudStorage/Dropbox/AnacondaProjects/是常研究室/2025/github_projects/First-principles analysis of in-plane anomalous Hall effect using symmetry-adapted Wannier Hamiltonians and multipole decomposition/scripts/workflow/build_multipole_hdf5.py)
- Archived-compatible matrix-to-HDF5 entry point:
  [src/symwan_multipie/multipole.py](/Users/hirotosaito/Library/CloudStorage/Dropbox/AnacondaProjects/是常研究室/2025/github_projects/First-principles analysis of in-plane anomalous Hall effect using symmetry-adapted Wannier Hamiltonians and multipole decomposition/src/symwan_multipie/multipole.py)
- Public decomposition driver:
  [inputs/symwannier/fe_bcc/decompose_ham.py](/Users/hirotosaito/Library/CloudStorage/Dropbox/AnacondaProjects/是常研究室/2025/github_projects/First-principles analysis of in-plane anomalous Hall effect using symmetry-adapted Wannier Hamiltonians and multipole decomposition/inputs/symwannier/fe_bcc/decompose_ham.py)
- Public compact export:
  [scripts/workflow/export_multipole_coefficients.py](/Users/hirotosaito/Library/CloudStorage/Dropbox/AnacondaProjects/是常研究室/2025/github_projects/First-principles analysis of in-plane anomalous Hall effect using symmetry-adapted Wannier Hamiltonians and multipole decomposition/scripts/workflow/export_multipole_coefficients.py)

## Step 1: Run MultiPie on `Fe.py`

Run your local MultiPie generator against `Fe.py` in a scratch directory.
This repository does not ship the original launcher, so the exact command
depends on your MultiPie installation. What matters is that the run consumes
the `Fe` dictionary from `Fe.py`.

Important settings already encoded in `Fe.py`:

- `bond`: shells `1..35`
- `spinful: True`
- `generate.time_reversal_type: "both"`
- `option.binary_output: True`

That last setting is what asks the archived workflow to emit the binary matrix
dictionary `Fe_matrix.pkl` rather than only a text-style Python export.

The archived `Fe_all_35/Fe.out` log confirms that this stage wrote:

- `Fe_model.py`
- `Fe_samb.py`
- `Fe_matrix.pkl`

The public repo keeps a curated copy of that evidence in
[Fe_all_35_generation_excerpt.txt](/Users/hirotosaito/Library/CloudStorage/Dropbox/AnacondaProjects/是常研究室/2025/github_projects/First-principles analysis of in-plane anomalous Hall effect using symmetry-adapted Wannier Hamiltonians and multipole decomposition/data/source/workflow_manifests/multipole_coefficients/Fe_all_35_generation_excerpt.txt).

## Step 2: Convert the matrix dictionary to HDF5

If the MultiPie run produced the archived filename `Fe_matrix.pkl`, use the
archived-compatible command:

```bash
PYTHONPATH=src python src/symwan_multipie/multipole.py Fe_matrix.pkl
```

This writes `Fe_matrix.hdf5` next to the pickle.

If instead you have a more explicit filename such as `Fe_all_35_matrix.py` or
`Fe_all_35_matrix.pkl`, use the public wrapper:

```bash
python scripts/workflow/build_multipole_hdf5.py \
  --matrix-path Fe_all_35_matrix.py \
  --output multi_matrix.hdf5
```

The two paths are equivalent in role:

- archived naming: `Fe_matrix.pkl -> Fe_matrix.hdf5`
- public generic naming: `Fe_all_35_matrix.py/.pkl -> multi_matrix.hdf5`

## Step 3: Inspect the basis HDF5

The archived job script immediately inspected the generated HDF5:

```bash
h5dump -d multipole_matrix/shape Fe_matrix.hdf5
h5ls Fe_matrix.hdf5/multipole_matrix
```

The surviving stdout log shows the archived shape:

```text
(0): 345708, 1067, 18, 18
```

That evidence is preserved in
[Fe_all_35_matrix_shape_excerpt.txt](/Users/hirotosaito/Library/CloudStorage/Dropbox/AnacondaProjects/是常研究室/2025/github_projects/First-principles analysis of in-plane anomalous Hall effect using symmetry-adapted Wannier Hamiltonians and multipole decomposition/data/source/workflow_manifests/multipole_coefficients/Fe_all_35_matrix_shape_excerpt.txt).

## Step 4: Build the decomposition HDF5

Run the decomposition driver in a directory that already contains the target
Wannier Hamiltonian text file, for example `trs_py_ed_tb.dat`.

For the manuscript ED branch:

```bash
python inputs/symwannier/fe_bcc/decompose_ham.py \
  --matrix-path Fe_matrix.hdf5 \
  --trs-py-ed
```

or, if you used the generic public filename:

```bash
python inputs/symwannier/fe_bcc/decompose_ham.py \
  --matrix-path multi_matrix.hdf5 \
  --trs-py-ed
```

This writes `trs_py_ed_tb.hdf5`, which contains the `z_coefficients` dataset
used by the bar-plot workflow.

Other supported branches are:

- `--symwan-pd` -> `pwscf_py_pd_tb.hdf5`
- `--symwan-ed` -> `pwscf_py_ed_tb.hdf5`
- `--wan-orig` -> `pwscf_tb.hdf5`

## Step 5: Export the compact coefficient table

Once both the decomposition HDF5 and `Fe_samb.py` are present:

```bash
python scripts/workflow/export_multipole_coefficients.py \
  --multi-path trs_py_ed_tb.hdf5 \
  --samb-path Fe_samb.py \
  --output multipole_coefficients.csv \
  --mode bar-merged
```

That compact CSV is the natural replacement for the current PDF-vector-backed
fallback under
[data/source/pdf_vector/multipole_coefficients/](/Users/hirotosaito/Library/CloudStorage/Dropbox/AnacondaProjects/是常研究室/2025/github_projects/First-principles analysis of in-plane anomalous Hall effect using symmetry-adapted Wannier Hamiltonians and multipole decomposition/data/source/pdf_vector/multipole_coefficients).

## Practical Notes

- `Fe_samb.py` and `Fe_matrix.pkl` are generated products; they are not meant
  to be hand-written.
- The repository currently preserves supporting evidence for the selected
  manuscript `z_i` labels in
  [Fe_all_20_supporting_samb.py.gz](/Users/hirotosaito/Library/CloudStorage/Dropbox/AnacondaProjects/是常研究室/2025/github_projects/First-principles analysis of in-plane anomalous Hall effect using symmetry-adapted Wannier Hamiltonians and multipole decomposition/data/source/workflow_manifests/multipole_coefficients/Fe_all_20_supporting_samb.py.gz),
  but that file is not a drop-in replacement for the missing direct
  `Fe_all_35` source.
- The public repo is intentionally documenting the expensive generation steps
  rather than trying to run the full MultiPie/HPC stage automatically.
