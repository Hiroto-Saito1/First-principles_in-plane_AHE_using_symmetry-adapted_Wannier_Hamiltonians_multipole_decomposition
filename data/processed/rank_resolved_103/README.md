# Rank-Resolved AHC Data: Fe (103)

This directory contains compact rank-cumulative processed data for the bcc Fe
`(103)` magnetization-rotation figures:

- `sigma_para_group*.pdf`
- `sigma_perp_group*.pdf`
- `sigma_axis_group*.pdf`

The main source files are:

```text
tests/Fe/FM_sqa_103/theta0_qe-7.2/hamiltonian_hdf5_trs/anisotropy_w_rank3/angle_dep_ahc.xml
tests/Fe/FM_sqa_103/theta0_qe-7.2/hamiltonian_hdf5_trs/anisotropy_w_rank3/angle_dep_w_rank*.xml
tests/Fe/FM_sqa_103/theta0_qe-7.2/hamiltonian_hdf5_trs/anisotropy/angle_dep_ahc.xml
```

The exact manuscript PDFs for the single-rank comparison
`sigma_para.pdf`, `sigma_perp.pdf`, and `sigma_axis.pdf` are included under
`figures/paper/`. Compact single-rank CSV extraction is still a follow-up
because the manuscript PDFs were generated from additional rank-filtered AHC
outputs rather than the rank-cumulative XML alone.
