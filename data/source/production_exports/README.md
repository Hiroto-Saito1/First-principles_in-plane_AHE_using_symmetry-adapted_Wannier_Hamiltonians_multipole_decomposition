# Production Export Source Snapshots

These CSV files are small production-workflow exports that are used as the
immediate source for `data/processed/`.

They are not raw DFT, Wannier, HDF5, or WannierBerri outputs. Those upstream
objects are too large or too workflow-specific for Git, so their regeneration
recipe is maintained in `scripts/workflow/generate_large_files.md`.

The export files are intentionally stored separately from `data/processed/` so
the processed CSVs can be rebuilt and checked rather than treated as unexplained
endpoints.

## Source Mapping

| Source files | Output files | Units and notes |
| --- | --- | --- |
| `ahc_111/ahc_angle_dependence.csv`, `ahc_111/energy_angle_dependence.csv` | `data/processed/ahc_111/*.csv` | AHC values are in S/cm; angles are in degrees; energy values are relative eV summaries from the production rotation workflow. |
| `ahc_103/ahc_angle_dependence.csv`, `ahc_103/energy_angle_dependence.csv` | `data/processed/ahc_103/*.csv` | AHC values are in S/cm; angles are in degrees; tensor and projected components follow the manuscript `(103)` basis. |
| `rank_resolved_103/rank_resolved_ahc.csv`, `rank_resolved_103/rank_cumulative_energy.csv`, `rank_resolved_103/single_rank_ahc.csv` | `data/processed/rank_resolved_103/*.csv` | Rank-cumulative and single-rank AHC values are in S/cm; energy summaries are in eV. |
| `strain_103/strain_plus_ahc.csv`, `strain_103/strain_minus_ahc.csv` | `data/processed/strain_103/*.csv` | Strain is engineering strain in percent; AHC values are in S/cm. |
| `minimal_model/model_sigma_axis.csv` | `data/processed/minimal_model/model_sigma_axis.csv` | Compact direct export from archived minimal-model AHC text outputs; `sigma_axis` is the projection onto the `(103)` plane normal in S/cm. |

Rebuild command:

```bash
python scripts/workflow/rebuild_processed_data.py --skip-pdf-vector
```
