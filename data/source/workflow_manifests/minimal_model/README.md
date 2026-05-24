# `minimal_model` Reference-Information Contracts

This directory records the minimum information content required for the
paper-facing minimal-model panels:

- `sigma_axis_model_1st_nn.pdf`
- `sigma_axis_model_2nd_nn.pdf`

The contract does not try to match the final manuscript PDFs byte-for-byte.
Instead, it fixes the paper-facing role of the committed compact model export:

- the plotted quantity is `sigma_n` (`sigma_axis`);
- each parameter sweep keeps its committed set of hopping values; and
- every parameter curve keeps the shared 13-point angle grid
  `0, 15, ..., 180` degrees.

The compact CSV itself is already a direct export from archived minimal-model
AHC outputs, so this contract mainly protects against silent curve loss,
parameter drift, or output-path drift in the paper-facing plot script.
