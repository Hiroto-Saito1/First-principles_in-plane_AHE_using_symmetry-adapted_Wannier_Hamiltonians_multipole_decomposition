# Strain Data: Fe (103)

This directory contains compact processed data for volume-preserving uniaxial
strain along `[103]` in bcc Fe.

Included CSV files:

- `strain_plus_ahc.csv`: tensile strain series from 0% to +1%.
- `strain_minus_ahc.csv`: compressive strain series from 0% to -1%.

The source XML files were extracted from:

```text
tests/Fe/FM_sqa_103_strained_along_103/*/angle_dep_ahc_dft.xml
```

The strained DFT and Wannier working directories are not stored. The
generation procedure for the strained cell parameters is documented in
`scripts/workflow/generate_large_files.md`.
