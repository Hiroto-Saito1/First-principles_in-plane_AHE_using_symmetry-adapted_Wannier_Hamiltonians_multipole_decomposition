# Data Inventory

This file tracks data that are included in the repository and data products
that must be regenerated. Files larger than 100 MB should not be committed to
Git. For those files, this repository should provide the generation procedure
rather than the file itself.

## Included Data

| Path | Status | Description |
| --- | --- | --- |
| `tests/fixtures/` | generated at test time | Synthetic two-orbital fixture for HDF5 conversion, multipole decomposition, magnetization rotation, and energy-difference tests. |
| `figures/paper/` | included | Exact PDF files referenced by `main_all.tex`, copied from the paper build directory. |
| `data/processed/figure_inventory.csv` | included | Complete inventory of manuscript figure files, reproducibility level, data path, and plotting script. |
| `data/processed/ahc_111/` | included | Compact CSV/JSON data for Fe `(111)` AHC angular dependence and energy-angle data. |
| `data/processed/ahc_103/` | included | Compact CSV/JSON data for Fe `(103)` AHC angular dependence and energy-angle data. |
| `data/processed/rank_resolved_103/` | included | Compact rank-cumulative AHC and energy data for Fe `(103)`. |
| `data/processed/strain_103/` | included | Compact strain-dependent Fe `(103)` AHC data for tensile and compressive `[103]` strain. |
| `data/processed/multipole_coefficients/` | documented target | Exact paper PDFs are included, but compact coefficient CSV extraction still depends on generated HDF5 outputs. |
| `data/processed/minimal_model/` | documented target | Exact paper PDFs are included, but compact minimal-model CSV extraction is still pending. |

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

## Reproducibility Levels

| Level | Meaning | Current examples |
| --- | --- | --- |
| 1 | Reproducible from compact files committed to Git | `(111)` AHC, `(103)` AHC, rank-cumulative AHC, strain AHC |
| 2 | Exact PDF is committed, but compact processed data extraction is incomplete | single-rank AHC and minimal-model figures |
| 3 | Requires generated large Hamiltonian, HDF5, Wannier, or AHC intermediate files | band convergence and multipole-coefficient extraction |

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

Concrete regeneration notes are maintained in
`scripts/workflow/generate_large_files.md`.

## Large Generated Files To Document

| File class | Store in Git? | Required documentation |
| --- | --- | --- |
| Raw Quantum ESPRESSO work directories | No | input templates, pseudopotentials, k meshes, cutoffs, run order |
| Wannier intermediate files | No if >100 MB | SymWannier/TRS-Wannier commands and source inputs |
| Multipole HDF5 matrices | No if >100 MB | MultiPie generation command and conversion command |
| Rank-resolved rotated Hamiltonians | No if >100 MB | filter settings and `MagRotation` command |
| WannierBerri AHC intermediate outputs | No if >100 MB | AHC command, Fermi level, k mesh, adaptive settings |
