# Manuscript Mapping

This file maps manuscript artifacts to repository data and scripts. It is a
living document and should be updated whenever processed data or figure
scripts are added.

## Current Status

The exact PDF files referenced by `main_all.tex` are included under
`figures/paper/`. Compact CSV/JSON data and plotting scripts have been added
for the primary AHC, rank-cumulative, and strain figures. The complete
machine-readable inventory is:

```text
data/processed/figure_inventory.csv
```

## Planned Figure And Table Mapping

| Manuscript artifact | Repository data | Script or test | Status |
| --- | --- | --- | --- |
| SAMB reconstruction accuracy table | small fixture and future Fe summary | `tests/test_decomposition.py`, future processed table | initial fixture implemented |
| All manuscript PDF figures | `figures/paper/` | `tests/test_paper_figures.py` | exact PDFs included |
| Leading multipole coefficients | `figures/paper/bar_ed_*.pdf`; target CSV under `data/processed/multipole_coefficients/` | `scripts/reproduce_figures/plot_multipole_coefficients.py` | exact PDFs included; compact CSV pending |
| `(111)` AHC angular dependence | `data/processed/ahc_111/` | `scripts/reproduce_figures/plot_ahc_111.py` | processed data included |
| `(103)` AHC angular dependence | `data/processed/ahc_103/` | `scripts/reproduce_figures/plot_ahc_103.py` | processed data included |
| Rank-resolved AHC contributions | `data/processed/rank_resolved_103/` | `scripts/reproduce_figures/plot_rank_resolved_103.py` | rank-cumulative data included |
| `[103]` strain effect | `data/processed/strain_103/` | `scripts/reproduce_figures/plot_strain_103.py` | processed data included |
| Minimal `p_z`-`d_xy` model | `figures/paper/sigma_axis_model_*.pdf`; target CSV under `data/processed/minimal_model/` | `scripts/reproduce_figures/plot_minimal_model.py` | exact PDFs included; compact CSV pending |

## Code-Level Mapping

| Workflow step | Implemented module |
| --- | --- |
| MultiPie matrix conversion | `symwan_multipie.multipole` |
| Multipole HDF5 partial reading | `symwan_multipie.single_multipole_reader` |
| Hamiltonian decomposition | `symwan_multipie.multipole_decomposition` |
| Magnetization rotation | `symwan_multipie.mag_rotation` |
| Reconstruction error metrics | `symwan_multipie.energy_diff` |
| Minimal Wannier Hamiltonian reader | `symwan_multipie.wannier_utils.hamiltonian` |
