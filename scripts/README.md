# Scripts

This directory is reserved for command-line workflows and figure reproduction
scripts.

- `reproduce_figures/`: scripts that generate manuscript figures from
  processed data.
- `reproduce_from_inputs.sh`: top-level lightweight driver. By default it
  rebuilds processed CSV files from committed source snapshots and regenerates
  repository-backed figures, splitting manuscript-style and diagnostic outputs.
- `reproduce_all_figures.sh`: figure-only driver that reads existing
  `data/processed/` files and writes to `results/figures_paper/` plus the
  current AHC/rank-resolved/multipole `results/figures_diagnostics/` outputs.
  It can also generate a paper-vs-reference contact sheet PDF on demand.
- `workflow/`: scripts that prepare or transform Hamiltonian and multipole
  data.
