# Workflow

This document describes the intended computational workflow represented by the
repository. The current implementation contains the lightweight Python core and
test fixtures; production data and full figure scripts will be added as the
repository is reconstructed.

## 1. First-Principles Calculation

The manuscript uses Quantum ESPRESSO to calculate the electronic structure of
body-centered cubic Fe. The important output for this repository is not the
entire DFT working directory, but the Wannier-ready data needed to construct a
tight-binding Hamiltonian.

Production settings such as pseudopotentials, energy cutoffs, k meshes, spin
quantization axes, and strain tensors should be documented in
`docs/data_inventory.md` and in future example directories.

## 2. Symmetry-Adapted Wannier Hamiltonian

SymWannier/TRS-Wannier is used to construct a symmetry-adapted Wannier
Hamiltonian. The Hamiltonian is represented as real-space matrices
`H(R)`, stored in `wannier_hr.dat`, `wannier_tb.dat`, or HDF5-derived formats.

The package currently provides a minimal `HamR` reader under
`symwan_multipie.wannier_utils`.

## 3. MultiPie SAMB Generation

MultiPie generates the symmetry-adapted multipole basis (SAMB). The old
workflow produced `*_matrix.pkl`, `*_matrix.py`, and `*_samb.py` files. The
new repository converts the matrix output into a compact HDF5 representation:

```text
*_matrix.pkl or *_matrix.py -> multipole_matrix.hdf5
```

The implemented entry point is `symwan_multipie.Multipole`.
The corresponding public workflow wrapper is
`scripts/workflow/build_multipole_hdf5.py`.

## 4. Multipole Decomposition

The Wannier Hamiltonian is decomposed as

```text
H(R) = sum_i z_i Z_i(R)
```

where `Z_i` are SAMB matrices and `z_i` are decomposition coefficients. The
output HDF5 stores:

- `irvec`,
- `ndegen`,
- `z_coefficients`,
- padded sparse multipole matrices.

The implemented entry point is `symwan_multipie.MultipoleDecomposition`.
The public wrapper for the Fe workflow is
`inputs/symwannier/fe_bcc/decompose_ham.py`.

### 4a. Coefficient-Plot Route

The manuscript multipole-coefficient bar plots do not come from a text file
named `z_coefficients.dat`. The archived `plot_bar.py` workflow reads:

- a decomposition HDF5 containing the `z_coefficients` dataset, and
- the corresponding `Fe_samb.py` file for SAMB labels.

In public-repo terms, the intended compact route is:

```text
Fe_all_35_matrix.py or .pkl
  -> multi_matrix.hdf5
  -> trs_py_ed_tb.hdf5 (or pwscf_py_ed_tb.hdf5 / pwscf_py_pd_tb.hdf5)
  -> compact coefficient CSV
```

The repository now includes the two conversion steps as reusable scripts:

```bash
python scripts/workflow/build_multipole_hdf5.py --matrix-path Fe_all_35_matrix.py --output multi_matrix.hdf5
python inputs/symwannier/fe_bcc/decompose_ham.py --matrix-path multi_matrix.hdf5 --trs-py-ed
python scripts/workflow/export_multipole_coefficients.py --multi-path trs_py_ed_tb.hdf5 --samb-path Fe_samb.py --output coefficients.csv --mode bar-merged
```

The original compact coefficient HDF5/CSV used for the manuscript is still
missing from the currently available local workspaces, so the committed
processed CSV remains a tracked recovered snapshot rather than a direct export.

## 5. Magnetization Rotation

Selected magnetic or magnetic-toroidal components can be filtered by
multipole type, rank, and irreducible representation, then rotated in spin
space. This is used to analyze rank-resolved contributions to the angular
dependence of AHC.

The implemented entry point is `symwan_multipie.MagRotation`.

## 6. AHC Calculation

Production AHC calculations are performed with WannierBerri. The repository
will store lightweight processed outputs for manuscript figure reproduction.
Full WannierBerri calculations should be documented as integration workflows
because they can be computationally expensive.

## 7. Figure Reproduction

Figure scripts should read from `data/processed/` and write to a dedicated
output directory. Each script must be mapped to a manuscript figure in
`docs/paper_mapping.md`.
