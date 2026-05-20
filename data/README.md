# Data Directory

This directory will contain lightweight processed data used to reproduce the
figures and tables in the manuscript.

Large raw DFT, Wannier, HDF5, and cluster-output files should not be committed
directly to Git. Any file larger than 100 MB should be documented by its
generation procedure instead of stored in the repository.

Planned subdirectories:

- `processed/`: compact XML, CSV, JSON, or HDF5 summaries used by figure
  scripts.
- generation procedures for >100 MB files: recorded in
  `docs/data_inventory.md` or workflow documents.

Current processed data include:

- `processed/figure_inventory.csv`: complete list of figure files referenced
  by `main_all.tex`.
- `processed/definitions/`: compact JSON configuration for the `(111)` and
  `(103)` plane-definition figures.
- `processed/ahc_111/`: compact Fe `(111)` AHC and energy-angle data.
- `processed/ahc_103/`: compact Fe `(103)` AHC and energy-angle data.
- `processed/rank_resolved_103/`: compact rank-cumulative Fe `(103)` AHC and
  energy data.
- `processed/strain_103/`: compact tensile and compressive `[103]` strain AHC
  data.
- `processed/multipole_coefficients/`: tracked generation target backed by a
  recovered compact snapshot.
- `processed/minimal_model/`: direct compact export of archived minimal-model
  AHC outputs.
