# Figure Reproduction Scripts

Scripts here read from `data/processed/` and write generated figures under
`results/figures/` by default. The exact manuscript PDFs are committed under
`figures/paper/`.

To regenerate every figure that currently has committed compact data, run:

```bash
./scripts/reproduce_all_figures.sh
```

This produces scientifically equivalent repository-local plots. It does not
attempt byte-identical reproduction of the final manuscript PDFs.

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
