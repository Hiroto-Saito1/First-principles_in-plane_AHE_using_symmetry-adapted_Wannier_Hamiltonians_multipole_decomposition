# Minimal Model Production Export

This directory stores the compact source export for the manuscript minimal
two-orbital `p_z`-`d_xy` model figure.

The CSV in this directory is not a PDF-vector recovery. It is exported from
archived model AHC text outputs:

- `bcc_model/1st_nn_t2_0/t_T_*/psi_*/sigma_ahc_eta1.00meV.txt`
- `bcc_model/2nd_nn_t1_0.2/t_T_*/psi_*/sigma_ahc_eta1.00meV.txt`

using:

```bash
python scripts/workflow/export_minimal_model_source.py \
  --source-root /path/to/bcc_model \
  --output data/source/production_exports/minimal_model/model_sigma_axis.csv
```

`sigma_axis` is the anomalous Hall conductivity vector projected onto the
normal of the `(103)` rotation plane, using the same convention as the
archived `fermi_ahc_plot.py` helper:

```text
sigma_vec = (sigma_yz, sigma_zx, sigma_xy)
n_hat = (1, 0, 3) / sqrt(10)
sigma_axis = sigma_vec . n_hat
```

Columns:

- `scan`: `first_nn` for the `t_T^(1)` scan at fixed `t_T^(2)=0`, or
  `second_nn` for the `t_T^(2)` scan at fixed `t_T^(1)=0.2`.
- `parameter_value`: scanned magnetic-toroidal hopping amplitude.
- `phi_deg`: magnetization angle in the `(103)` plane.
- `sigma_axis`: out-of-plane AHC in S/cm.
- `source_tree`: archived source subdirectory under `bcc_model/`.
- `source_file`: source text file relative to that subdirectory.
