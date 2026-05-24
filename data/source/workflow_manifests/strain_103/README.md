# `strain_103` Reference-Information Contracts

This directory records the minimum information content required for the
paper-facing `[103]` strain-response panels:

- `sigma_plus_strain_sigma_axis.pdf`
- `sigma_minus_strain_sigma_axis.pdf`

The contract does not try to reproduce the final manuscript PDFs byte-for-byte.
Instead, it fixes the paper-facing role of these plots:

- the committed `SW+ED` angular series are the source of truth;
- the plotted quantity is `sigma_n` (`sigma_axis_s_cm`);
- each committed strain branch keeps six strain values; and
- each strain curve keeps the shared 13-point angle grid
  `0, 15, ..., 180` degrees.

The diagnostic `Wan90` and `SW+PD` entries remain in the compact CSV snapshots,
but they are not part of the paper-facing strain contract.
