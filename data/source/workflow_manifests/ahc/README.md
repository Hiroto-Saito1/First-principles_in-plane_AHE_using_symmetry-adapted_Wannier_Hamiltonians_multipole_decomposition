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
compact sources, and how many finite points are required before a generated
paper-facing panel can be treated as manuscript-reproducible.

Archived manuscript-side `fit_ahc.py` scripts indicate that the `fit_ahc*.pdf`
panels are built from the first `angle_dep_ahc.xml` series plus an analytic fit
curve. The broader DFT overlay belongs to the archived `plot_ahc.py` scripts
and their separate `angle_dep_ahc_dft.xml` input, not to the `fit_ahc*.pdf`
contract itself.

That means the committed compact source snapshots under
`data/source/production_exports/ahc_{111,103}/` are already sufficient for the
paper-facing `fit_ahc` panels: they contain the full `SW+ED` series required by
the archived fit scripts. The diagnostic AHC plots under
`results/figures_diagnostics/` remain the place where `Wan90`, `SW+PD`, and
other implementation-comparison series are shown.
