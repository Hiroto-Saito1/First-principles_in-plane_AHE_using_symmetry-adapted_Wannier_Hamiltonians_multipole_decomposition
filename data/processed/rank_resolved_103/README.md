# Rank-Resolved AHC Data: Fe (103)

This directory contains compact rank-resolved processed data for the bcc Fe
`(103)` magnetization-rotation figures.

Rank-cumulative data are used for:

- `sigma_para_group*.pdf`
- `sigma_perp_group*.pdf`
- `sigma_axis_group*.pdf`

Single-rank data are used for:

- `sigma_para.pdf`
- `sigma_perp.pdf`
- `sigma_axis.pdf`

The CSV files contain AHC tensor components and the projected
`sigma_para`, `sigma_perp`, and `sigma_axis` components at the Fermi level.
The `rank_resolved_ahc.csv` file stores rank-cumulative series, while
`single_rank_ahc.csv` stores single-rank series for ranks 1, 3, 4, and 5
plus the all-component `SW+ED` reference curve.

Immediate committed sources:

- `data/source/production_exports/rank_resolved_103/rank_resolved_ahc.csv`
- `data/source/production_exports/rank_resolved_103/rank_cumulative_energy.csv`
- `data/source/production_exports/rank_resolved_103/single_rank_ahc.csv`

Rebuild command:

```bash
python scripts/workflow/rebuild_processed_data.py
```

The full upstream route requires TRS-Wannier HDF5 files, SAMB rank filters,
magnetization rotation, and WannierBerri AHC calculations; those large
intermediates are documented in `scripts/workflow/generate_large_files.md`.
