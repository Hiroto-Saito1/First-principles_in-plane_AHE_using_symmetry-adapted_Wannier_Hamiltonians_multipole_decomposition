# Figure Reproduction Scripts

Scripts here read from `data/processed/` and write generated figures under
`results/figures/` by default. The exact manuscript PDFs are committed under
`figures/paper/`.

Available scripts:

- `plot_ahc_111.py`
- `plot_ahc_103.py`
- `plot_rank_resolved_103.py`
- `plot_strain_103.py`
- `plot_multipole_coefficients.py`
- `plot_minimal_model.py`

The last two scripts require compact CSV files that still need to be
generated from the large production outputs; see
`scripts/workflow/generate_large_files.md`.
