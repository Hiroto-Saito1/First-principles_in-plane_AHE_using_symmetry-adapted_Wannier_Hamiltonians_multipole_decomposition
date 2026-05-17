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

## Expected Generated Files

The workflow should produce Hamiltonian files analogous to:

- `pwscf_py_ed_tb.dat`
- `trs_py_ed_hr.hdf5`
- `trs_py_pd_hr.hdf5`
- `trs_tb_hr.hdf5`

The HDF5 files are large generated outputs. Keep them out of Git and document
their generation in `scripts/workflow/generate_large_files.md`.

