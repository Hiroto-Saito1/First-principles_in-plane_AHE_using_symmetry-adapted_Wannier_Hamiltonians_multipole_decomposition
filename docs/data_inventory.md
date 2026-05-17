# Data Inventory

This file tracks data that are included in the repository or referenced from
external locations. Large raw data should be listed here rather than committed
directly to Git.

## Included Data

| Path | Status | Description |
| --- | --- | --- |
| `tests/fixtures/` | generated at test time | Synthetic two-orbital fixture for HDF5 conversion, multipole decomposition, magnetization rotation, and energy-difference tests. |
| `data/processed/` | placeholder | Future location for compact manuscript figure data. |

## Old Repository Reference

The old repository is a read-only source for reconstruction:

```text
/Users/hirotosaito/Library/CloudStorage/Dropbox/AnacondaProjects/是常研究室/2024/github_projects/symwan_multipie
```

It contains reusable code, CH4/Nb/Ni/Fe examples, DFT outputs, Wannier outputs,
AHC summaries, and large HDF5 files. These files must be curated before any
subset is copied into this repository.

## Data To Curate

| Manuscript item | Candidate source | Planned repository form |
| --- | --- | --- |
| SAMB decomposition accuracy | old `tests/CH4` and Fe HDF5 outputs | small fixture tests plus a compact table |
| Leading multipole coefficients | old Fe `z_coefficients` outputs | CSV/JSON table under `data/processed/` |
| `(111)` AHC angular dependence | old `tests/Fe/FM_sqa_111` | processed XML/CSV and figure script |
| `(103)` AHC angular dependence | old `tests/Fe/FM_sqa_103` | processed XML/CSV and figure script |
| Rank-resolved AHC | old Fe `anisotropy_w_rank*` directories | compact summary data and filter metadata |
| `[103]` strain effect | old `tests/Fe/FM_sqa_103_strained_along_103` | strain-resolved processed data |
| Minimal `p_z`-`d_xy` model | manuscript/model scripts | standalone Python model and output CSV |

## Large Data Policy

Large files should be handled by one of the following mechanisms:

- external archive such as Zenodo,
- Git LFS if small enough and intentionally versioned,
- documented "available upon request" status.

Each external dataset should include checksum, size, source path, generation
script, and corresponding manuscript figure or table.

