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

The multipole-coefficient and minimal-model CSV files were recovered from the
vector data embedded in the exact manuscript PDFs because the original compact
CSV tables were not preserved. The full first-principles regeneration path
still starts from the large outputs documented in
`scripts/workflow/generate_large_files.md`.
