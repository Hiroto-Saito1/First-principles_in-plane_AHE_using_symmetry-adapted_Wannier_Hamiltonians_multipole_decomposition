# Unstrained bcc Fe Wannier Inputs

This directory contains initial Wannier90 and `pw2wannier90` input templates
for the unstrained bcc Fe workflow.

## Files

- `pw2wan.in`: Quantum ESPRESSO `pw2wannier90` input.
- `pwscf.win`: Wannier90 input with the 8 x 8 x 8 k-point grid.
- `kpoints.py`: helper script used to generate the k-point list in
  `pwscf.win`.

Generated Wannier files such as `.amn`, `.mmn`, `.eig`, `.chk`, `.hr`, `.tb`,
and any large HDF5 conversion outputs are not committed.
