# `ahc_103` Production Exports

This directory contains the committed compact source snapshots used to rebuild
the public `(103)` AHC processed CSV files.

- `ahc_angle_dependence.csv` and `energy_angle_dependence.csv` come from the
  lightweight `angle_dep_ahc_dft.xml` / `angle_dep_ed.xml` exports.
- `fit_ahc_angle_dependence.csv` is a curated compact export recovered from the
  archived `FM_sqa_103/anisotropy/angle_dep_ahc.xml` model source used by the
  manuscript-side `fit_ahc.py`.

Rebuild the corresponding processed CSV files with:

```bash
python scripts/workflow/rebuild_processed_data.py
```
