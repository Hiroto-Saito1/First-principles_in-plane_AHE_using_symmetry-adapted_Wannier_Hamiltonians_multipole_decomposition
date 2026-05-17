# Data Directory

This directory will contain lightweight processed data used to reproduce the
figures and tables in the manuscript.

Large raw DFT, Wannier, HDF5, and cluster-output files should not be committed
directly to Git. Their location, size, provenance, and publication status must
be recorded in `docs/data_inventory.md`.

Planned subdirectories:

- `processed/`: compact XML, CSV, JSON, or HDF5 summaries used by figure
  scripts.
- external archives: recorded in `docs/data_inventory.md` when available.

