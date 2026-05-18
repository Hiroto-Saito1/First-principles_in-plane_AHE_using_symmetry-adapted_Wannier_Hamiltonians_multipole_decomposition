# Scripts

This directory is reserved for command-line workflows and figure reproduction
scripts.

- `reproduce_figures/`: scripts that generate manuscript figures from
  processed data.
- `reproduce_from_inputs.sh`: top-level lightweight driver. By default it
  rebuilds processed CSV files from committed source snapshots and regenerates
  repository-backed figures.
- `reproduce_all_figures.sh`: figure-only driver that reads existing
  `data/processed/` files.
- `workflow/`: scripts that prepare or transform Hamiltonian and multipole
  data.
