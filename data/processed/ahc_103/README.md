# AHC Data: Fe (103)

This directory contains compact processed data for the bcc Fe `(103)`
magnetization-rotation figures:

- `fit_ahc_para_103.pdf`
- `fit_ahc_perp_103.pdf`
- `fit_ahc_axis_103.pdf`

The CSV files contain AHC tensor components, projected AHC components, and
energy-angle data used by the corresponding manuscript panels.

Immediate committed sources:

- `data/source/production_exports/ahc_103/ahc_angle_dependence.csv`
- `data/source/production_exports/ahc_103/energy_angle_dependence.csv`

Rebuild command:

```bash
python scripts/workflow/rebuild_processed_data.py
```

No raw DFT, Wannier, HDF5, or WannierBerri working files are stored here.
