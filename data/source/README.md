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
  compact source export was not preserved.

## Rebuild Command

```bash
python scripts/workflow/rebuild_processed_data.py
```

The command rebuilds all committed processed CSV files from this directory and
from the tracked vector PDFs used for the recovered band/bond,
multipole-coefficient, and minimal-model data.
