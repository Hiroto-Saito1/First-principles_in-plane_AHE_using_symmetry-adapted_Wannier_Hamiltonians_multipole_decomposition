# AHC Data: Fe (111)

This directory contains compact processed data for the bcc Fe `(111)`
magnetization-rotation figures:

- `fit_ahc_para.pdf`
- `fit_ahc_perp.pdf`
- `fit_ahc_axis.pdf`

The CSV files contain AHC tensor components, projected AHC components, and
energy-angle data used by the corresponding manuscript panels.

Immediate committed sources:

- `data/source/production_exports/ahc_111/ahc_angle_dependence.csv`
- `data/source/production_exports/ahc_111/fit_ahc_angle_dependence.csv`
- `data/source/production_exports/ahc_111/energy_angle_dependence.csv`

The paper-facing `fit_ahc_*.pdf` plots now read from
`fit_ahc_angle_dependence.csv`, which is a compact export recovered from the
archived `FM_sqa_111/anisotropy/angle_dep_ahc.xml` model source. The broader
diagnostic AHC comparisons still read from `ahc_angle_dependence.csv`, which is
the compact snapshot extracted from `angle_dep_ahc_dft.xml`.

Rebuild command:

```bash
python scripts/workflow/rebuild_processed_data.py
```

No raw DFT, Wannier, HDF5, or WannierBerri working files are stored here.
