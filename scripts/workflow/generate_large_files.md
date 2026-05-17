# Generation Procedures For Large Files

This document records how to regenerate manuscript artifacts that depend on
large files. Files larger than 100 MB should not be committed to this
repository; the procedure is stored here instead.

## Fe TRS-Wannier Hamiltonians

Purpose: regenerate the HDF5 Hamiltonians used for SAMB decomposition,
magnetization rotation, rank filtering, and coefficient extraction.

Expected generated files include TRS-Wannier Hamiltonian HDF5 files under the
old workflow directories such as:

```text
tests/Fe/FM_sqa_103/theta0_qe-7.2/hamiltonian_hdf5_trs/
tests/Fe/FM_sqa_111/theta0_qe-7.2/hamiltonian_hdf5_trs/
```

Procedure:

1. Run the Quantum ESPRESSO SCF and non-SCF calculations with the settings
   documented in `docs/workflow.md`.
2. Construct SymWannier models with 36 spinor Wannier functions for Fe.
3. Generate the time-reversal-symmetric Hamiltonian with the cleaned
   equivalent of `write_trs_ham.py`.
4. Run the cleaned decomposition workflow with `symwan_multipie` against the
   generated TRS-Wannier Hamiltonian.

Do not commit the generated HDF5 outputs if they exceed 100 MB.

## Multipole Coefficient Figures

Purpose: regenerate `bar_ed_all_35.pdf` and `bar_ed_wo_q_35.pdf`.

Inputs:

```text
decomposed TRS-Wannier HDF5 with z_coefficients
Fe_samb.py or Fe_samb.py.gz from the corresponding MultiPie run
```

Procedure:

1. Generate or locate the decomposed HDF5 output containing `z_coefficients`.
2. Generate or locate the SAMB metadata file containing the `Z` names.
3. Extract a compact CSV with columns such as
   `index,name,type,irrep,rank,coefficient_ev,abs_coefficient_ev`.
4. Store the compact CSV at
   `data/processed/multipole_coefficients/multipole_coefficients.csv`.
5. Run `scripts/reproduce_figures/plot_multipole_coefficients.py`.

The exact manuscript PDFs are already committed in `figures/paper/`.

## Rank-Resolved Rotated Hamiltonians

Purpose: regenerate rank-filtered and single-rank AHC outputs.

Procedure:

1. Start from the generated TRS-Wannier Hamiltonian and SAMB decomposition.
2. Use `symwan_multipie.mag_rotation` to select magnetic and
   magnetic-toroidal components by rank.
3. Generate rotated Hamiltonians for the target `(103)` angles.
4. Run WannierBerri at the documented Fermi level and convergence settings.
5. Extract compact XML or CSV summaries analogous to
   `data/processed/rank_resolved_103/rank_resolved_ahc.csv`.

Do not commit rotated Hamiltonians or full WannierBerri output directories if
they exceed 100 MB.

## [103] Strain Series

Purpose: regenerate strain-dependent AHC outputs for tensile and compressive
volume-preserving strain.

Cell-parameter generation:

```bash
python scripts/workflow/strain_103_cell.py --percent 1.0
python scripts/workflow/strain_103_cell.py --percent -1.0
```

Then rerun the Fe DFT, SymWannier, TRS-Wannier, decomposition, rotation, and
WannierBerri workflows for each strain value. Commit only compact XML, CSV, or
JSON summaries; leave raw work directories out of Git.
