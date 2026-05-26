# `ahc_111` Production Exports

This directory contains the committed compact source snapshots used to rebuild
the public `(111)` AHC processed CSV files.

- `ahc_angle_dependence.csv` and `energy_angle_dependence.csv` come from the
  lightweight `angle_dep_ahc_dft.xml` / `angle_dep_ed.xml` exports.
- `fit_ahc_angle_dependence.csv` is a curated compact export recovered from the
  archived `FM_sqa_111/anisotropy/angle_dep_ahc.xml` model source used by the
  manuscript-side `fit_ahc.py`.
- `fit_ahc_dft_angle_dependence.csv` is a curated compact export of the
  `SW+ED` branch from `ahc_angle_dependence.csv`, promoted to the paper-facing
  `DFT` role because archived `plot_ahc.py` overlays that branch as the DFT
  comparison.

Rebuild the corresponding processed CSV files with:

```bash
python scripts/workflow/rebuild_processed_data.py
```
