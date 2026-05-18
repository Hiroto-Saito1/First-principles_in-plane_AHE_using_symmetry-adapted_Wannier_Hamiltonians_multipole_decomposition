# Strain Data: Fe (103)

This directory contains compact processed data for volume-preserving uniaxial
strain along `[103]` in bcc Fe.

Included CSV files:

- `strain_plus_ahc.csv`: tensile strain series from 0% to +1%.
- `strain_minus_ahc.csv`: compressive strain series from 0% to -1%.

The CSV files contain strain-resolved AHC tensor components and projected AHC
components for the corresponding manuscript panels. The `strain_percent`
column gives the applied engineering strain in percent.

Immediate committed sources:

- `data/source/production_exports/strain_103/strain_plus_ahc.csv`
- `data/source/production_exports/strain_103/strain_minus_ahc.csv`

Rebuild command:

```bash
python scripts/workflow/rebuild_processed_data.py
```

The strained DFT and Wannier working directories are not stored. The
generation procedure for the strained cell parameters is documented in
`scripts/workflow/generate_large_files.md`.
