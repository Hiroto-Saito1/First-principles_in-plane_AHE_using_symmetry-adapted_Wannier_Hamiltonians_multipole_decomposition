# Calculation Inputs

This directory collects portable input files and manifests for the
first-principles workflows behind the manuscript figures. It is intentionally
separate from `data/processed/`, which stores compact data already extracted
for plotting.

Files below 100 MB should be committed here when they are needed to understand
or rerun the workflow. Large generated outputs, HDF5 files, full work
directories, caches, and cluster logs should not be committed.

## Current Contents

- `dft/fe_bcc_unstrained/`: initial Quantum ESPRESSO input templates for the
  unstrained bcc Fe workflow.
- `dft/fe_bcc_strain_103/`: initial Quantum ESPRESSO input template and notes
  for the `[103]` strain structure workflow.
- `wannier/fe_bcc_unstrained/`: initial Wannier90 and `pw2wannier90` inputs
  for the unstrained bcc Fe workflow.
- `symwannier/fe_bcc/`: portable SymWannier/TRS-Wannier manifests for the Fe
  Hamiltonian variants, rotation planes, and rank filters.
- `multipie/fe_bcc/`: SAMB/MultiPie metadata manifest for the Fe 35-shell
  multipole decomposition.
- `wannierberri/fe_bcc_rotation/`: portable AHC settings, rotation grids, and
  per-angle WannierBerri job-generation templates.
- `wannierberri/fe_bcc_strain_103/`: reader-facing snapshot of the archived
  `[103]` strain workflow, linked to the public cell generator and compact
  strain CSV outputs.

## Pseudopotentials

Pseudopotential files are not committed until redistribution permissions are
confirmed. Each input README records the expected pseudopotential filename and
the local destination where a reader should place it before running Quantum
ESPRESSO.
