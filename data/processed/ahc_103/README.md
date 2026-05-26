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
- `data/source/production_exports/ahc_103/fit_ahc_angle_dependence.csv`
- `data/source/production_exports/ahc_103/fit_ahc_dft_angle_dependence.csv`
- `data/source/production_exports/ahc_103/energy_angle_dependence.csv`

The paper-facing `fit_ahc_*_103.pdf` plots now read from two committed compact
sources:

- `fit_ahc_angle_dependence.csv` for the archived `angle_dep_ahc.xml` model
  series
- `fit_ahc_dft_angle_dependence.csv` for the archived `plot_ahc.py` DFT
  overlay role, recovered from the `SW+ED` branch of
  `angle_dep_ahc_dft.xml`

The broader diagnostic AHC comparisons still read from `ahc_angle_dependence.csv`,
which keeps the full `SW+ED` / `Wan90` / `SW+PD` implementation comparison.

Rebuild command:

```bash
python scripts/workflow/rebuild_processed_data.py
```

No raw DFT, Wannier, HDF5, or WannierBerri working files are stored here.
