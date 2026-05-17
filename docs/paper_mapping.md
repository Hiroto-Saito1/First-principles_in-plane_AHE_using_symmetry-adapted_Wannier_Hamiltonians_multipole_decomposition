# Manuscript Mapping

This file maps manuscript artifacts to repository data and scripts. It is a
living document and should be updated whenever processed data or figure
scripts are added.

Manuscript preprint: [arXiv:2601.05689](https://arxiv.org/abs/2601.05689).

## Current Status

The exact PDF files referenced by `main_all.tex` are included under
`figures/paper/`. Repository-local reproduction scripts generate equivalent
data figures under `results/figures/`, while static assets remain committed as
reference PDFs. Compact CSV/JSON data and plotting scripts have been added for
the primary AHC, rank-cumulative, and strain figures. The complete
machine-readable inventory is:

```text
data/processed/figure_inventory.csv
```

## Figure And Table Mapping

| Manuscript artifact | Repository data | Script or test | Category |
| --- | --- | --- | --- |
| SAMB reconstruction accuracy table | small fixture and future Fe summary | `tests/test_decomposition.py`, future processed table | workflow/data follow-up |
| All manuscript PDF figures | `figures/paper/` | `tests/test_paper_figures.py` | reference PDFs |
| Static schematics and structure figures | `figures/paper/`, `data/processed/static_schematics/README.md` | inventory checks | `static_asset` |
| Leading multipole coefficients | target CSV under `data/processed/multipole_coefficients/` | `scripts/reproduce_figures/plot_multipole_coefficients.py` | `workflow_required` |
| `(111)` AHC angular dependence | `data/processed/ahc_111/` | `scripts/reproduce_figures/plot_ahc_111.py` | `reproducible_plot` |
| `(103)` AHC angular dependence | `data/processed/ahc_103/` | `scripts/reproduce_figures/plot_ahc_103.py` | `reproducible_plot` |
| Rank-cumulative AHC contributions | `data/processed/rank_resolved_103/` | `scripts/reproduce_figures/plot_rank_resolved_103.py` | `reproducible_plot` |
| Single-rank AHC contributions | target CSV under `data/processed/rank_resolved_103/` | `scripts/reproduce_figures/plot_rank_resolved_103.py` | `workflow_required` |
| `[103]` strain effect | `data/processed/strain_103/` | `scripts/reproduce_figures/plot_strain_103.py` | `reproducible_plot` |
| Minimal `p_z`-`d_xy` model | target CSV under `data/processed/minimal_model/` | `scripts/reproduce_figures/plot_minimal_model.py` | `workflow_required` |

## Code-Level Mapping

| Workflow step | Implemented module |
| --- | --- |
| MultiPie matrix conversion | `symwan_multipie.multipole` |
| Multipole HDF5 partial reading | `symwan_multipie.single_multipole_reader` |
| Hamiltonian decomposition | `symwan_multipie.multipole_decomposition` |
| Magnetization rotation | `symwan_multipie.mag_rotation` |
| Reconstruction error metrics | `symwan_multipie.energy_diff` |
| Minimal Wannier Hamiltonian reader | `symwan_multipie.wannier_utils.hamiltonian` |
