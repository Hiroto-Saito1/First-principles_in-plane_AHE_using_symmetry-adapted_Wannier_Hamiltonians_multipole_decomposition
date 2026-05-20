# Multipole Coefficient Recovery Snapshot

This directory stores the compact recovered coefficient table used to rebuild
the manuscript multipole-bar processed CSV without reparsing the figure PDFs on
every rebuild:

- `multipole_coefficients.csv`

The values in this snapshot still originate from the vector data embedded in
the manuscript coefficient PDFs. The original first-principles compact export
or source HDF5 was not found in the current local reconstruction workspaces, so
this remains a labeled fallback provenance path rather than a direct workflow
export.

Recovery tooling remains available:

```bash
python scripts/workflow/extract_pdf_vector_data.py --target multipole
```

Until the original compact source is recovered, the default rebuild path uses
this committed snapshot:

```bash
python scripts/workflow/rebuild_processed_data.py
```

The intended direct workflow, once the corresponding generated HDF5 is
available again, is:

```bash
python scripts/workflow/build_multipole_hdf5.py --matrix-path Fe_all_35_matrix.py --output multi_matrix.hdf5
python inputs/symwannier/fe_bcc/decompose_ham.py --matrix-path multi_matrix.hdf5 --trs-py-ed
python scripts/workflow/export_multipole_coefficients.py --multi-path trs_py_ed_tb.hdf5 --samb-path Fe_samb.py --output multipole_coefficients.csv --mode bar-merged
```

The archive-side evidence for how that source HDF5 was built is committed
under `data/source/workflow_manifests/multipole_coefficients/`.
