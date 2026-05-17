# Manuscript Mapping

This file maps manuscript artifacts to repository data and scripts. It is a
living document and should be updated whenever processed data or figure
scripts are added.

## Current Status

Only the lightweight code and synthetic tests have been added. Manuscript
figure data are still placeholders.

## Planned Figure And Table Mapping

| Manuscript artifact | Repository data | Script or test | Status |
| --- | --- | --- | --- |
| SAMB reconstruction accuracy table | small fixture and future Fe summary | `tests/test_decomposition.py`, future processed table | initial fixture implemented |
| Leading multipole coefficients | `data/processed/` CSV/JSON | future `scripts/reproduce_figures/` script | pending |
| `(111)` AHC angular dependence | `data/processed/fe_111_*` | future figure script | pending |
| `(103)` AHC angular dependence | `data/processed/fe_103_*` | future figure script | pending |
| Rank-resolved AHC contributions | `data/processed/fe_103_rank_*` | future figure script plus `MagRotation` filters | pending |
| `[103]` strain effect | `data/processed/fe_103_strain_*` | future figure script | pending |
| Minimal `p_z`-`d_xy` model | future model output CSV | future standalone model script | pending |

## Code-Level Mapping

| Workflow step | Implemented module |
| --- | --- |
| MultiPie matrix conversion | `symwan_multipie.multipole` |
| Multipole HDF5 partial reading | `symwan_multipie.single_multipole_reader` |
| Hamiltonian decomposition | `symwan_multipie.multipole_decomposition` |
| Magnetization rotation | `symwan_multipie.mag_rotation` |
| Reconstruction error metrics | `symwan_multipie.energy_diff` |
| Minimal Wannier Hamiltonian reader | `symwan_multipie.wannier_utils.hamiltonian` |

