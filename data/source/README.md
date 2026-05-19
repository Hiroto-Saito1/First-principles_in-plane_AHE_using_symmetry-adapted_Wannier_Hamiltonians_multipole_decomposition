# Source Data For Processed CSV Files

This directory contains the committed small source files used to rebuild
`data/processed/` without running DFT, Wannier90, SymWannier, MultiPie, or
WannierBerri.

## Source Classes

- `production_exports/`: compact CSV exports from the production workflow.
  These are small summaries of expensive calculations. The full path from DFT
  inputs to these exports is documented in `scripts/workflow/generate_large_files.md`.
- `pdf_vector/`: metadata for CSV files recovered from the vector data embedded
  in manuscript PDFs or committed per-panel source PDFs when the original
  compact source export was not preserved. This tree can contain both the
  tracked source PDFs and compact recovered CSV snapshots derived from them.

## Rebuild Command

```bash
python scripts/workflow/rebuild_processed_data.py
```

The command rebuilds all committed processed CSV files from this directory and
from the tracked vector PDFs used for the recovered band/bond,
multipole-coefficient, and minimal-model data. Multipole coefficients now
rebuild from a committed recovered source snapshot under `data/source/pdf_vector/`,
while `band_bond` and the minimal model are still re-extracted from vector PDFs.

When the original workflow HDF5 is available, the direct coefficient route is:

```text
Fe_all_35_matrix.py or .pkl
  -> multi_matrix.hdf5
  -> decomposition HDF5 with z_coefficients
  -> compact coefficient CSV
```

The public wrappers for those steps are
`scripts/workflow/build_multipole_hdf5.py`,
`inputs/symwannier/fe_bcc/decompose_ham.py`, and
`scripts/workflow/export_multipole_coefficients.py`.
