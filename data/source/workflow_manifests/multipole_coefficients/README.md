# Archived Multipole-Coefficient Workflow Manifest

This directory records the archived workflow evidence for the manuscript
multipole-coefficient figures when the original compact source HDF5/CSV is not
available in the current local workspaces.

It is not the same as a direct production export. Instead, it preserves the
exact old workflow chain and the selected SAMB labels used by the manuscript:

```text
Fe.py
  -> Fe_samb.py + Fe_matrix.pkl
  -> Fe_matrix.hdf5
  -> trs_py_ed_tb.hdf5 (or the older trs_py_ed_hr.hdf5 branch)
  -> bar_ed_all_35.pdf / bar_ed_wo_q_35.pdf
```

Files:

- `workflow_manifest.json`: curated summary of the archived MultiPie,
  matrix-to-HDF5, decomposition, and label-selection steps.
- `Fe_all_35_recipe.md`: step-by-step rebuild recipe for the missing
  `Fe_matrix.pkl`, `Fe_matrix.hdf5`, and downstream decomposition HDF5 files.
- `selected_z_ids.csv`: the manuscript-selected SAMB entries extracted from the
  archived `submit_samb.sh` / `out_trs_ed` workflow.
- `Fe_all_35_generation_excerpt.txt`: curated excerpt from the surviving
  `Fe_all_35/Fe.out` log showing that the archived run wrote `Fe_model.py`,
  `Fe_samb.py`, and `Fe_matrix.pkl`.
- `Fe_all_35_matrix_shape_excerpt.txt`: curated excerpt from
  `Fe_all_35/submit.sh.o3507` showing the archived
  `python src/multipole.py Fe_matrix.pkl` step and the resulting
  `Fe_matrix.hdf5` shape.
- `Fe_all_20_supporting_samb.py.gz`: a gzipped archival `Fe_samb.py` copied
  from the surviving `Fe_all_20` branch. It contains all manuscript-selected
  `z_i` labels listed in `selected_z_ids.csv`, but it is only a supporting
  provenance artifact and not a substitute for the missing direct `Fe_all_35`
  source used to build the compact coefficient HDF5/CSV.

The compact numerical CSV still rebuilt by the repository lives under
`data/source/pdf_vector/multipole_coefficients/`. This manifest exists so the
upstream HDF5-generation path is documented even though the direct generated
HDF5 file is currently missing. The surviving `Fe_all_35/Fe.out` log confirms
that the original `Fe_all_35` workflow wrote `Fe_samb.py` and `Fe_matrix.pkl`,
but those direct artifacts are not present in the current local archives. For
the practical rebuild steps, start with
`data/source/workflow_manifests/multipole_coefficients/Fe_all_35_recipe.md`.
