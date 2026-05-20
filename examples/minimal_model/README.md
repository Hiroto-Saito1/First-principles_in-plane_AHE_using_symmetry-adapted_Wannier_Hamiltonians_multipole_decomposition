# Minimal Two-Orbital Model

This example recovers the archived standalone BCC `p_z`-`d_xy` model used to
build the manuscript minimal-model figures.

Files:

- `model.py`: archived driver recovered from
  `2025/発表/defense/figs/model.py`. It writes a Wannier90-style `hr.dat`
  for the two-orbital model with magnetization rotated in the `(103)` plane.

The manuscript parameters correspond to:

- `eps0 = 0.0`
- `Delta0 = 1.0`
- `Delta = 1.0`
- `t0 = [-1.0, 0.0]`
- `t3 = 0.0`
- `t_pd = 0.0`
- `t_T = [t_T^(1), t_T^(2)]`
- `max_shell = 2`

Example:

```bash
python examples/minimal_model/model.py --psi 90 --out minimal_model_hr.dat
```

This example reconstructs the model Hamiltonian itself. The compact figure
source used by the public repository is exported from archived AHC text
outputs under the maintainer's `bcc_model/` workspace via
`scripts/workflow/export_minimal_model_source.py`. The repository does not yet
wrap the full model-to-AHC recalculation stage that produced those archived
`sigma_ahc_eta1.00meV.txt` files.
