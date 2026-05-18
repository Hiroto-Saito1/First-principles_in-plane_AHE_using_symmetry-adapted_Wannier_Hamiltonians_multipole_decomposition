# Minimal Model Data

```text
data/processed/minimal_model/model_sigma_axis.csv
```

This CSV contains the angular scans shown in the minimal two-orbital model
figures:

- `sigma_axis_model_1st_nn.pdf`
- `sigma_axis_model_2nd_nn.pdf`

The table was recovered from the Matplotlib vector paths embedded in the
committed manuscript PDFs using
`scripts/workflow/extract_pdf_vector_data.py`. The model Hamiltonian and
parameters are described in the manuscript; a standalone recalculation script
can replace this recovered table later if the original model workflow is
curated.

Columns:

- `scan`: `first_nn` for the first-nearest-neighbor magnetic-toroidal hopping
  scan or `second_nn` for the second-nearest-neighbor scan.
- `parameter_value`: scanned hopping parameter value.
- `phi_deg`: magnetization rotation angle in degrees.
- `sigma_axis`: plotted out-of-plane AHC value in S/cm.
- `source_pdf`: manuscript PDF used for vector-data recovery.
