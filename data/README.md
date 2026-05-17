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
