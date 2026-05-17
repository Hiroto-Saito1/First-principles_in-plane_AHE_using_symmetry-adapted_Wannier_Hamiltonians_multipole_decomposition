# Multipole Coefficient Data

The exact manuscript PDFs for the coefficient-bar figures are included under
`figures/paper/`:

- `bar_ed_all_35.pdf`
- `bar_ed_wo_q_35.pdf`

The compact coefficient table is not yet included because it must be generated
from the decomposed TRS-Wannier HDF5 outputs and the corresponding SAMB name
table. Those large or generated files should not be copied directly into Git
when they exceed 100 MB.

The expected follow-up file is:

```text
data/processed/multipole_coefficients/multipole_coefficients.csv
```

The generation procedure is documented in
`scripts/workflow/generate_large_files.md`.
