# `fit_ahc` Reference-Information Contracts

This directory records the minimum information content required for the
paper-facing AHC angular-dependence panels:

- `fit_ahc_para.pdf`
- `fit_ahc_perp.pdf`
- `fit_ahc_axis.pdf`
- `fit_ahc_para_103.pdf`
- `fit_ahc_perp_103.pdf`
- `fit_ahc_axis_103.pdf`

The contract file does not try to enforce byte-identical PDF reproduction.
Instead, it records which series must be present, how they map onto committed
compact sources, how their role identity is verified, and how many finite
points are required before a generated paper-facing panel can be treated as
manuscript-reproducible.

Archived manuscript-side `fit_ahc.py` scripts indicate that the `fit_ahc*.pdf`
panels are built from the first `angle_dep_ahc.xml` series plus an analytic fit
curve. The broader DFT overlay belongs to the archived `plot_ahc.py` scripts
and their separate `angle_dep_ahc_dft.xml` input, not to the `fit_ahc*.pdf`
contract itself.

At the moment, both planes are backed by committed archived-model compact
exports:

- `(103)` uses `data/source/production_exports/ahc_103/fit_ahc_angle_dependence.csv`,
  recovered from `PAPER_ROOT/figs/Fe/FM_sqa_103/anisotropy/angle_dep_ahc.xml`.
- `(111)` uses `data/source/production_exports/ahc_111/fit_ahc_angle_dependence.csv`,
  recovered from
  `SYMWAN_ROOT/tests/Fe/FM_sqa_111/theta0_qe-7.2/hamiltonian_hdf5_trs/anisotropy/angle_dep_ahc.xml`.

The diagnostic AHC plots under `results/figures_diagnostics/` remain the place
where `Wan90`, `SW+PD`, and other implementation-comparison series are shown.
