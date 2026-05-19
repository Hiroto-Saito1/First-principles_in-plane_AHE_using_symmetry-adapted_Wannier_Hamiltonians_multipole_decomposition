# Fe SymWannier And TRS-Wannier Inputs

This directory records the portable settings needed after the Quantum
ESPRESSO and Wannier90 steps for the Fe workflows in the manuscript. The
generated Hamiltonian files are not committed here because production HDF5 and
rotated tight-binding outputs can exceed 100 MB.

## Purpose

The SymWannier stage constructs symmetry-adapted Wannier Hamiltonians for bcc
Fe and prepares the time-reversal-symmetric Hamiltonians used by the SAMB
decomposition, magnetization-rotation, and WannierBerri AHC workflows.

## Required Inputs

- Quantum ESPRESSO outputs from `inputs/dft/fe_bcc_unstrained/`.
- Wannier90 and `pw2wannier90` inputs from
  `inputs/wannier/fe_bcc_unstrained/`.
- A converged Fe Wannier model with 36 spinor Wannier functions.
- The pseudopotential documented in the DFT input README.

## Settings Captured Here

- `symwannier_settings.json`: compact manifest of the Fe model size,
  Hamiltonian variants, magnetization axes, and downstream generated files.
- `write_trs_ham.py`: cleaned helper that reconstructs a TRS-style
  `trs_py_ed_tb.dat` from `pwscf_py_ed_tb.dat`.
- `decompose_ham.py`: cleaned decomposition driver that writes compact HDF5
  decomposition outputs from `*.dat` Hamiltonians.
- `energy_diff_fe.py`: cleaned reconstruction-error driver for the Fe
  `wan`, `symwan`, and `trs` Hamiltonian branches.
- `submit_energy_diff.sh`: local shell wrapper that reproduces the manuscript
  energy-difference report variants without cluster-specific PBS settings.

## Expected Generated Files

The workflow should produce Hamiltonian files analogous to:

- `pwscf_py_ed_tb.dat`
- `trs_py_ed_tb.dat`
- `pwscf_py_ed_tb.hdf5`
- `pwscf_py_pd_tb.hdf5`
- `trs_py_ed_tb.hdf5`
- `pwscf_tb.hdf5`

## Typical Command Order

From a working directory that contains the generated `pwscf*.dat` files and
the recovered `Fe_samb.py` / `multi_matrix.hdf5` artifacts:

```bash
python scripts/workflow/build_multipole_hdf5.py --matrix-path Fe_all_35_matrix.py --output multi_matrix.hdf5
python inputs/symwannier/fe_bcc/write_trs_ham.py --input pwscf_py_ed_tb.dat --output-tb trs_py_ed_tb.dat
python inputs/symwannier/fe_bcc/decompose_ham.py --matrix-path multi_matrix.hdf5 --symwan-ed --trs-py-ed --wan-orig
python inputs/symwannier/fe_bcc/energy_diff_fe.py --samb-path Fe_samb.py
python scripts/workflow/export_multipole_coefficients.py --multi-path trs_py_ed_tb.hdf5 --samb-path Fe_samb.py --output coefficients.csv --mode bar-merged
```

The HDF5 files are large generated outputs. Keep them out of Git and document
their generation in `scripts/workflow/generate_large_files.md`.

For the manuscript coefficient figures, the important generated file is the
decomposition HDF5 with a `z_coefficients` dataset. The archived `plot_bar.py`
workflow consumes that HDF5 plus `Fe_samb.py`; the public
`export_multipole_coefficients.py` helper exists to turn the same pair into a
compact CSV before plotting.
