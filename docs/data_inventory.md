# Data Inventory

This file tracks data that are included in the repository and data products
that must be regenerated. Files larger than 100 MB should not be committed to
Git. For those files, this repository should provide the generation procedure
rather than the file itself.

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

The default policy is:

- Commit compact processed data and metadata needed to reproduce manuscript
  figures.
- Do not commit files larger than 100 MB.
- Do not use Git LFS or an external archive by default for files larger than
  100 MB.
- For each file larger than 100 MB, document how to generate it from smaller
  committed inputs or from the documented first-principles workflow.

Each large generated file entry should include the expected path, source
workflow, command sequence, required software versions, expected approximate
size, and checksum if a generated local copy is available.

## Large Generated Files To Document

| File class | Store in Git? | Required documentation |
| --- | --- | --- |
| Raw Quantum ESPRESSO work directories | No | input templates, pseudopotentials, k meshes, cutoffs, run order |
| Wannier intermediate files | No if >100 MB | SymWannier/TRS-Wannier commands and source inputs |
| Multipole HDF5 matrices | No if >100 MB | MultiPie generation command and conversion command |
| Rank-resolved rotated Hamiltonians | No if >100 MB | filter settings and `MagRotation` command |
| WannierBerri AHC intermediate outputs | No if >100 MB | AHC command, Fermi level, k mesh, adaptive settings |
