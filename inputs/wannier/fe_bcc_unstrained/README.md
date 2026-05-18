# Unstrained bcc Fe Wannier Inputs

This directory contains the portable Wannier90 and `pw2wannier90` input
templates for the unstrained bcc Fe workflow. The current files are aligned
with the source `FM_sqa_z/.../symwannier/` production inputs used for the
public reproduction package.

## Files

- `pw2wan.in`: Quantum ESPRESSO `pw2wannier90` input.
- `pwscf.win`: Wannier90 input with the 8 x 8 x 8 k-point grid, explicit
  `Fe: s,p,d [0,0,1]` projections, `spinors = .true.`, and the production
  disentanglement window.
- `kpoints.py`: helper script used to generate the k-point list in
  `pwscf.win`.

Generated Wannier files such as `.amn`, `.mmn`, `.eig`, `.chk`, `.hr`, `.tb`,
and any large HDF5 conversion outputs are not committed.
