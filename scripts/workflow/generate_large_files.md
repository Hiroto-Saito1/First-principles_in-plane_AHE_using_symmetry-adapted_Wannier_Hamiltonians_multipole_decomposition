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
   documented in `inputs/dft/`.
2. Construct SymWannier models with 36 spinor Wannier functions for Fe.
3. Use the settings in `inputs/symwannier/fe_bcc/symwannier_settings.json` to
   generate the time-reversal-symmetric Hamiltonian variants.
4. Run the cleaned decomposition workflow with `symwan_multipie` and the SAMB
   metadata described in `inputs/multipie/fe_bcc/samb_manifest.json`.

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
3. Generate rotated Hamiltonians for the target `(103)` angles in
   `inputs/wannierberri/fe_bcc_rotation/rotation_grid.json`.
4. Run WannierBerri at the documented Fermi level and convergence settings in
   `inputs/wannierberri/fe_bcc_rotation/ahc_template.py`.
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

## WannierBerri AHC Runs

Purpose: regenerate the AHC XML or pickle outputs that are summarized in
`data/processed/ahc_111/`, `data/processed/ahc_103/`,
`data/processed/rank_resolved_103/`, and `data/processed/strain_103/`.

Inputs:

```text
rotated *_phi*_tb.dat files from the SymWannier/SAMB rotation workflow
inputs/wannierberri/fe_bcc_rotation/rotation_grid.json
inputs/wannierberri/fe_bcc_rotation/ahc_template.py
```

Procedure:

1. Place rotated tight-binding files in a working directory.
2. Copy `ahc_template.py` and `make_ahc_jobs.py` from
   `inputs/wannierberri/fe_bcc_rotation/`.
3. Run `python make_ahc_jobs.py --tb-dir . --target ed_phi --step 5`.
4. Run each generated `run_ahc.sh` with the desired CPU count.
5. Extract compact CSV summaries and commit only those summaries.

The generated `Klist_ahc.pickle`, per-angle WannierBerri work directories, and
rotated tight-binding files should remain outside Git when they are large.
