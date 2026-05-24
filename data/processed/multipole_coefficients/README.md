# Multipole Coefficient Data

```text
data/processed/multipole_coefficients/multipole_coefficients.csv
```

This CSV contains compact multipole coefficients for the manuscript
coefficient-bar figures:

- `bar_ed_all_35.pdf`
- `bar_ed_wo_q_35.pdf`

The table was recovered from the Matplotlib vector paths and labels embedded
in the committed manuscript PDFs using
`scripts/workflow/extract_pdf_vector_data.py`. A committed source snapshot now
lives under `data/source/pdf_vector/multipole_coefficients/` so ordinary
rebuilds do not need to reparse the PDFs. The original first-principles source
is the decomposed TRS-Wannier HDF5 output and the corresponding SAMB name
table, but those generated files were not preserved in a Git-suitable compact
form.

Fallback source metadata is recorded in `data/source/pdf_vector/README.md` and
`data/source/pdf_vector/multipole_coefficients/README.md`. Archived evidence for
the original HDF5-generation workflow is recorded in
`data/source/workflow_manifests/multipole_coefficients/`. This is explicitly a
recovered manuscript-vector provenance path, not a first-principles
regeneration path.

Columns:

- `index`: multipole index `z_i`.
- `name`: SAMB multipole label shown in the manuscript figure.
- `coefficient_ev`: coefficient value in eV.
- `abs_coefficient_ev`: absolute coefficient value in eV.
- `source_pdf`: manuscript PDF used for vector-data recovery.

The full HDF5-based generation procedure remains documented in
`scripts/workflow/generate_large_files.md`.

The repository plotting script now supports two presentation modes:

- paper mode: manuscript-facing `z_i` + SAMB labels with compact family-letter
  legends under `results/figures_paper/multipole_coefficients/`;
- diagnostic mode: raw `z_i` + SAMB names under
  `results/figures_diagnostics/multipole_coefficients/`, together with more
  explicit family-role legend text.

The paper-facing bar plots are additionally guarded by
`data/source/workflow_manifests/multipole_coefficients/bar_plot_reference_contract.json`.
That contract fixes the selected `z_i` entries, their ordering, and the
compact family-letter legend semantics expected from the manuscript-style
figures.

When the decomposition HDF5 is available, the direct compact-export command is:

```bash
python scripts/workflow/export_multipole_coefficients.py --multi-path trs_py_ed_tb.hdf5 --samb-path Fe_samb.py --output multipole_coefficients.csv --mode bar-merged
```
