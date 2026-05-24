# `rank_resolved_103` Reference-Information Contracts

This directory records the minimum information content required for the
paper-facing `(103)` rank-resolved AHC panels:

- `sigma_para_group1.pdf`
- `sigma_perp_group1.pdf`
- `sigma_axis_group1.pdf`
- `sigma_para_group2.pdf`
- `sigma_perp_group2.pdf`
- `sigma_axis_group2.pdf`
- `sigma_para_group3.pdf`
- `sigma_perp_group3.pdf`
- `sigma_axis_group3.pdf`
- `sigma_para.pdf`
- `sigma_perp.pdf`
- `sigma_axis.pdf`

The contract does not attempt byte-identical PDF reproduction. Instead, it
records which committed compact CSV series must remain visible in the
paper-facing output, how those series map onto manuscript-style multipole
labels, and how many finite angle samples each curve must retain.

For the cumulative panels, the paper-facing plots intentionally keep only the
three two-curve groupings exposed by `plot_rank_resolved_103.py`, together with
the `SW+ED` reference curve labeled as `all ranks`. Higher cumulative cutoffs
and `w_rankNone` remain outside the paper-facing contract.

For the single-rank panels, the paper-facing plots keep the four manuscript
roles `M1`, `M3`, `T4`, and `M5`, again with the shared `all ranks`
reference curve.
