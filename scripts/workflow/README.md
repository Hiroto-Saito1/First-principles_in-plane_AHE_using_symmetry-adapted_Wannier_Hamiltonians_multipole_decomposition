# Workflow Scripts

Scripts added here should perform reusable data transformations, such as:

- converting MultiPie matrix files to HDF5,
- decomposing Wannier Hamiltonians,
- rotating selected multipole components,
- summarizing AHC outputs.

Current scripts:

- `build_multipole_hdf5.py`: converts a MultiPie matrix dictionary export
  such as `Fe_all_35_matrix.py` or `Fe_all_35_matrix.pkl` into the compact
  `multi_matrix.hdf5` basis used by the public decomposition workflow.
- `export_minimal_model_source.py`: condenses archived minimal-model
  `sigma_ahc_eta1.00meV.txt` outputs into the compact CSV used by the figure
  plotting script.
- `export_multipole_coefficients.py`: extracts a compact coefficient CSV from
  a decomposition HDF5 that contains `z_coefficients` plus the corresponding
  `Fe_samb.py` label table.
- `rebuild_processed_data.py`: rebuilds all committed processed CSV files from
  `data/source/` production export snapshots and fallback PDF-vector sources or
  source snapshots.
- `extract_processed_data.py`: extracts compact CSV/JSON
  processed data from small XML summaries produced by the paper workflows.
- `extract_pdf_vector_data.py`: recovers compact CSV data from the Matplotlib
  vector paths embedded in manuscript PDFs when the original compact CSV is
  missing; it is now mainly used for the band/bond fallback.
- `strain_103_cell.py`: prints volume-preserving `[103]` strained bcc Fe cell
  parameters for Quantum ESPRESSO.
- `generate_large_files.md`: records generation procedures for large files
  that should not be committed to Git.
