# Fe Rotation And WannierBerri AHC Inputs

This directory contains portable templates for the Fe anomalous Hall
conductivity workflows used by the `(111)`, `(103)`, rank-resolved, and
strain-dependent manuscript figures.

## Purpose

The workflow takes rotated tight-binding files generated from the
SymWannier/SAMB decomposition and evaluates the anomalous Hall conductivity
with WannierBerri on a dense k mesh.

## Files

- `rotation_grid.json`: rotation-plane vectors, angle grids, filters, and AHC
  settings used by the Fe workflows.
- `rotate_mag.py`: cleaned rotation driver that reads a decomposed HDF5 file
  plus a reference `tb.dat` and writes `*_phi{deg}_tb.dat` files for the
  selected rotation plane.
- `calc_energy.py`: cleaned total-energy summary helper that reproduces the
  old `angle_dep*.xml` and `kmesh_dep*.xml` style outputs from rotated
  `tb.dat` files.
- `ahc_template.py`: portable WannierBerri AHC calculation template. It reads
  the tight-binding file path from the command line rather than embedding a
  private workflow path.
- `make_ahc_jobs.py`: local helper that writes per-angle AHC run directories
  from rotated `*_phi*_tb.dat` files. It prepares scripts but does not submit
  cluster jobs.
- `submit_ahc_all.py`: cleaned replacement for the old source-tree helper that
  prepares all selected per-angle AHC folders and can optionally execute them
  locally.

## Required External Software

- Python with `numpy` and `wannierberri`.
- Rotated tight-binding files generated from the SymWannier/SAMB workflow.

## Expected Command Order

1. Generate TRS-Wannier HDF5 files from the DFT and Wannier90 inputs.
2. Generate SAMB metadata and decomposed Hamiltonians.
3. Rotate the selected magnetic and magnetic-toroidal `T1g` Hamiltonian
   components on the angle grid in `rotation_grid.json`.
4. Use `make_ahc_jobs.py` to create per-angle AHC folders.
5. Run `ahc_template.py` in each folder.
6. Extract compact CSV/XML summaries under `data/processed/`.

## Typical Command Order

```bash
python inputs/wannierberri/fe_bcc_rotation/rotate_mag.py \
  --multi-path trs_py_ed_tb.hdf5 \
  --samb-path Fe_samb.py \
  --tb-input trs_py_ed_tb.dat \
  --plane 103 \
  --output-prefix trs_py_ed

python inputs/wannierberri/fe_bcc_rotation/calc_energy.py \
  --prefix trs_py_ed \
  --angle-dep

python inputs/wannierberri/fe_bcc_rotation/submit_ahc_all.py \
  --targets ed_phi \
  --step 5
```

Large `Klist_ahc.pickle`, WannierBerri result folders, and rotated
tight-binding files should stay out of Git when they are generated outputs.
