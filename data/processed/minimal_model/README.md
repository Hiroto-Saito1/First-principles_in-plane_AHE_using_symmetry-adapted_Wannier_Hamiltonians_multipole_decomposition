# Minimal Model Data

```text
data/processed/minimal_model/model_sigma_axis.csv
```

This CSV contains the angular scans shown in the minimal two-orbital model
figures:

- `sigma_axis_model_1st_nn.pdf`
- `sigma_axis_model_2nd_nn.pdf`

The table is rebuilt from the committed direct source export
`data/source/production_exports/minimal_model/model_sigma_axis.csv`, which was
cut from archived `sigma_ahc_eta1.00meV.txt` outputs for the minimal BCC
model. The recovery/export helper is:

`scripts/workflow/export_minimal_model_source.py`

The archived Hamiltonian generator itself is committed as
`examples/minimal_model/model.py`.

Columns:

- `scan`: `first_nn` for the first-nearest-neighbor magnetic-toroidal hopping
  scan or `second_nn` for the second-nearest-neighbor scan.
- `parameter_value`: scanned hopping parameter value.
- `phi_deg`: magnetization rotation angle in degrees.
- `sigma_axis`: plotted out-of-plane AHC value in S/cm.
- `source_tree`: archived source subtree under `bcc_model/`.
- `source_file`: archived AHC text file relative to that source subtree.
