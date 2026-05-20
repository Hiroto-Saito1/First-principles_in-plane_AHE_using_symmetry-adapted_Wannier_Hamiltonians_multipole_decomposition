# PDF Vector Recovery Sources

The band/bond, multipole-coefficient, and minimal-model compact CSV files are
recovered from Matplotlib vector paths embedded in tracked manuscript PDFs or
tracked per-panel source PDFs because the original compact source exports were
not preserved.

Recovery command:

```bash
python scripts/workflow/extract_pdf_vector_data.py
```

Current layout:

- `band_bond/`: per-cutoff source PDFs used to rebuild the recovered band/bond
  curve CSV.
- `multipole_coefficients/`: committed recovered CSV snapshot so routine
  processed-data rebuilds do not need to reparse the manuscript bar PDFs.
- root README only: the minimal-model recovered CSV is still regenerated
  directly from the tracked manuscript PDFs.

This is a fallback provenance path, not a substitute for first-principles
regeneration. The full desired regeneration path is documented in
`scripts/workflow/generate_large_files.md`.

For multipole coefficients, the desired direct path is already scripted even
though the original manuscript HDF5 is not currently available locally:

```bash
python scripts/workflow/build_multipole_hdf5.py --matrix-path Fe_all_35_matrix.py --output multi_matrix.hdf5
python inputs/symwannier/fe_bcc/decompose_ham.py --matrix-path multi_matrix.hdf5 --trs-py-ed
python scripts/workflow/export_multipole_coefficients.py --multi-path trs_py_ed_tb.hdf5 --samb-path Fe_samb.py --output coefficients.csv --mode bar-merged
```

The archived workflow evidence for how the original HDF5 was generated is
captured separately under
`data/source/workflow_manifests/multipole_coefficients/`.
