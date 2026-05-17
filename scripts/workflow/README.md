# Workflow Scripts

Scripts added here should perform reusable data transformations, such as:

- converting MultiPie matrix files to HDF5,
- decomposing Wannier Hamiltonians,
- rotating selected multipole components,
- summarizing AHC outputs.

Current scripts:

- `extract_processed_data.py`: extracts compact CSV/JSON
  processed data from small XML summaries produced by the paper workflows.
- `strain_103_cell.py`: prints volume-preserving `[103]` strained bcc Fe cell
  parameters for Quantum ESPRESSO.
- `generate_large_files.md`: records generation procedures for large files
  that should not be committed to Git.
