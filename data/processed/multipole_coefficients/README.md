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
`scripts/workflow/extract_pdf_vector_data.py`. The original first-principles
source is the decomposed TRS-Wannier HDF5 output and the corresponding SAMB
name table, but those generated files were not preserved in a Git-suitable
compact form.

Fallback source metadata is recorded in `data/source/pdf_vector/README.md`.
This is explicitly a recovered manuscript-vector provenance path, not a
first-principles regeneration path.

Columns:

- `index`: multipole index `z_i`.
- `name`: SAMB multipole label shown in the manuscript figure.
- `coefficient_ev`: coefficient value in eV.
- `abs_coefficient_ev`: absolute coefficient value in eV.
- `source_pdf`: manuscript PDF used for vector-data recovery.

The full HDF5-based generation procedure remains documented in
`scripts/workflow/generate_large_files.md`.
