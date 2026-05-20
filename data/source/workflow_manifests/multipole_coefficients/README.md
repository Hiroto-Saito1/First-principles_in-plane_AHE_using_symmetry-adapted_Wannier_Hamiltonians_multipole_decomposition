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
- `selected_z_ids.csv`: the manuscript-selected SAMB entries extracted from the
  archived `submit_samb.sh` / `out_trs_ed` workflow.

The compact numerical CSV still rebuilt by the repository lives under
`data/source/pdf_vector/multipole_coefficients/`. This manifest exists so the
upstream HDF5-generation path is documented even though the direct generated
HDF5 file is currently missing.
