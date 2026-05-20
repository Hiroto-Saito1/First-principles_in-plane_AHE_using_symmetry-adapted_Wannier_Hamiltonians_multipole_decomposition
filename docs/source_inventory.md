# Source Inventory

This document is the single source of truth for **where each manuscript
artifact lives in the local production workspaces and where it should go in
this public repository**. It is intended for the maintainer carrying out the
reorganization described in `plan.md`. It is not a reader-facing document.

The local workspaces referenced here are private. They are listed only so the
maintainer can copy the relevant under-100-MB files into the public layout.

## Local Reference Workspaces

| Symbol | Absolute path |
| --- | --- |
| `PAPER` | `/Users/hirotosaito/Library/CloudStorage/Dropbox/AnacondaProjects/是常研究室/2025/論文/Multipole-decomposition-of-symmetry-adapted-Wannier-Hamiltonian-using-projectability-disentanglement` |
| `SYMWAN` | `/Users/hirotosaito/Library/CloudStorage/Dropbox/AnacondaProjects/是常研究室/2025/github_projects/symwan_proj` |
| `REPO` | this public repository root |

In the tables below, paths are abbreviated with these symbols.

## Top-Level Layout Of Each Workspace

### PAPER

```text
PAPER/
├── body/
│   ├── arXiv/             # canonical manuscript source (main_all.tex)
│   ├── CPC/               # CPC submission variants
│   ├── PRB/               # PRB submission variants
│   ├── English/, Japanese/, elsarticle/
└── figs/
    ├── Fe/
    │   ├── FM_sqa_z/                       # SQA = z (reference set)
    │   ├── FM_sqa_103/                     # SQA = [103]
    │   ├── FM_sqa_111/                     # SQA = [111]
    │   ├── FM_sqa_103_strained_along_103/  # [103] strain
    │   ├── nonmag/                         # not used in manuscript main
    │   └── mae_theory/
    ├── Ni/, Nb/, CH4/, obsolete/           # not used by this manuscript
```

### SYMWAN

```text
SYMWAN/
├── README.md, environment.yml, pytest.ini
├── src/
│   ├── symwannier/                          # 11 modules (~92 KB)
│   ├── wannier_utils/                       # 23 modules + 3 archive (~193 KB)
│   ├── qe-7.4.1_pw2wan/                     # full QE 7.4.1 tree (modified)
│   ├── qe-7.4.1_pw2wan_orig/                # original QE tree (for diff)
│   └── symwannier_orig/                     # original SymWannier (for diff)
└── tests/
    ├── Fe/num_iter_0/
    │   ├── FM_wo_soc_SW/                    # site-symmetry path (non-SOC)
    │   ├── FM_wo_soc_PD/                    # projectability path (non-SOC)
    │   ├── FM_wo_soc_SW_PD/                 # both
    │   ├── band/                            # band-structure example
    │   ├── energy_diff/                     # WannierBerri AHC + multipole
    │   ├── multipie/Fe_all_35/              # MultiPie SAMB input
    │   └── z_coefficients/                  # z coefficient bar plots
    ├── Fe/num_iter_100/                     # comparison case
    └── Ni/                                  # not relevant to manuscript
```

## Manuscript Figure Mapping

The canonical manuscript file is `PAPER/body/arXiv/main_all.tex`. The figure
identifiers (filenames) match `data/processed/figure_inventory.csv` in this
repository.

The mapping is given per figure with: local PDF path, generating script,
generating data, public-repo destination, and reproduction category.

### Definition / Schematic Figures

These are static manuscript schematics. They are **`not_included`** in the
public repo, except where a Python generator exists locally — those should be
upgraded to `reproducible_plot`.

| Figure | Local PDF | Generator | Status & destination |
| --- | --- | --- | --- |
| `sigma_vec.pdf` | not located in `figs/` | none found (Keynote/manual) | stays `not_included` |
| `bcc_111.pdf` | `PAPER/figs/Fe/FM_sqa_111/bcc_111.pdf` | `PAPER/figs/Fe/FM_sqa_111/bcc_111.py` (matplotlib 3D, generates programmatically) | now `reproducible_plot`. Public config → `REPO/data/processed/definitions/bcc_planes.json`, public script → `REPO/scripts/reproduce_figures/plot_bcc_planes.py`, output → `REPO/results/figures/definitions/bcc_111.pdf` |
| `bcc_103.pdf` | `PAPER/figs/Fe/FM_sqa_103/bcc_103.pdf` | `PAPER/figs/Fe/FM_sqa_103/bcc_103.py` (matplotlib 3D) | now `reproducible_plot` via the same public JSON/script pair |
| `structure.pdf` | `PAPER/figs/Fe/FM_sqa_103_strained_along_103/structures/structure.pdf` | Keynote (`structure.key`) over `qe2cif.py` + VESTA | stays `not_included` |
| `MP86479.pdf`, `MP86701.pdf`, `MP86672.pdf`, `MP87119.pdf` | `PAPER/figs/Fe/FM_sqa_z/multipole/` | QtDraw (external tool) over MultiPie outputs in `out_trs_ed/` | stays `not_included` (QtDraw drawings) |
| `structure_p20.pdf`, `structure_m20.pdf` | `PAPER/figs/Fe/FM_sqa_103_strained_along_103/structures/` | Keynote (`structure.key`) + VESTA over `scf_p20percent.cif`, `scf_m20percent.cif` | stays `not_included` |

> The `multipole/` directory also has `MP86691.pdf`, `MP86714.pdf`, and
> `Fe_samb.pdf` that are **not** referenced in `arXiv/main_all.tex`. They are
> exploratory.

### `band_bond` (figure: convergence with SAMB bond range)

Now `reproducible_plot` in this repo through tracked per-cutoff vector PDFs
and a repository plotting script. The original local Keynote composite remains
useful provenance only.

| Item | Path / value |
| --- | --- |
| Local composite PDF | `PAPER/figs/Fe/FM_sqa_z/band_bond/band_bond.pdf` |
| Composite source | `PAPER/figs/Fe/FM_sqa_z/band_bond/band_bond.key` (Keynote, manually composed) |
| Per-bond-range band PDFs | `PAPER/figs/Fe/FM_sqa_z/band_bond/band_{1,2,3,4,5,10,20,35}.pdf` |
| Per-bond-range band data | not committed locally; regenerated from `Hamiltonian.h5` (>100 MB) via the multipole bond-range filter |
| Generation recipe | `MultipoleDecomposition` with bond-range filter → reconstructed `H(R)` → diagonalize on band path → band data CSV → matplotlib |
| Public source snapshot | `REPO/data/source/pdf_vector/band_bond/band_{1,2,3,4,5,10,20,35}.pdf` |
| Public processed data | `REPO/data/processed/band_bond/band_bond_curves.csv` |
| Public plotting script | `REPO/scripts/reproduce_figures/plot_band_bond.py` |
| Public reference PDF | `REPO/figures/paper/band_bond.pdf` |

### `bar_ed_all_35`, `bar_ed_wo_q_35` (leading multipole coefficients)

Two canonical bar plots are referenced in the manuscript. Many other bar
variants exist locally as exploratory analyses.

| Item | Path / value |
| --- | --- |
| Local bar PDFs (manuscript) | `PAPER/figs/Fe/FM_sqa_z/theta0_qe-7.2/z_coefficients/bar_ed_all_35.pdf`, `bar_ed_wo_q_35.pdf` |
| Generating script | `PAPER/figs/Fe/FM_sqa_z/theta0_qe-7.2/z_coefficients/plot_bar.py` (also `plot_bar_diff.py` for the `bar_diff_*` variants) |
| Alternative location | `PAPER/figs/Fe/FM_sqa_z/hamiltonian_hdf5_trs/z_coefficients/` has the same PDFs and scripts (`plot_bar.py`, `plot_bar_diff.py`) — needs disambiguation by date / which is canonical |
| Input data | `plot_bar.py` reads the `z_coefficients` dataset from a decomposition HDF5 (the archived defense copy points to `trs_py_ed_tb.hdf5`) plus `Fe_samb.py`; `energy_diff_35_*.out` is present in `theta0_qe-7.2/`, but the compact coefficient HDF5/CSV export is not preserved in the current local figure directories |
| Other exploratory variants | `bar_ed_wo_a1g_t1g_35`, `bar_ed_wo_a1g_t1g_eg_35`, `bar_ed_wo_a1g_t1g_eg_t2g_35`, `bar_ed_wo_q_t1g_35`; `bar_pd_*`, `bar_tb_*`, `bar_diff_*` |
| Current public-repo provenance | `REPO/data/source/pdf_vector/multipole_coefficients/multipole_coefficients.csv` + processed CSV under `REPO/data/processed/multipole_coefficients/`; rebuild no longer needs to reparse the manuscript PDFs. |
| Archived workflow manifest | `REPO/data/source/workflow_manifests/multipole_coefficients/` preserves the recovered source chain, including the `Fe.py` -> `Fe_samb.py` / `Fe_matrix.pkl` -> `Fe_matrix.hdf5` -> `trs_py_ed_tb.hdf5` route and the selected `z_i` labels from `out_trs_ed`. |
| Desired upgrade | recover the original compact coefficient source HDF5/CSV export and replace the PDF-vector provenance path. The public repo now documents the generation route as `Fe_all_35_matrix.py/.pkl -> multi_matrix.hdf5 -> trs_py_ed_tb.hdf5 -> compact coefficient CSV`. |

### `fit_ahc_para`, `fit_ahc_perp`, `fit_ahc_axis` ((111) plane)

| Item | Path / value |
| --- | --- |
| Local PDFs | `PAPER/figs/Fe/FM_sqa_111/anisotropy/{fit_ahc_para,fit_ahc_perp,fit_ahc_axis}.pdf` |
| Generating script | `PAPER/figs/Fe/FM_sqa_111/anisotropy/fit_ahc.py` (also `fit_angle_dep.py`, `plot_ahc.py`, `plot_angle_dep.py`) |
| Input data | `PAPER/figs/Fe/FM_sqa_111/anisotropy/angle_dep_ahc.xml` (301 lines); per-method variants `angle_dep_{ed,pd,tb}_{70,80,90}.xml`; k-mesh study `kmesh_dep_{ed,pd,tb}.xml` |
| Driver scripts | `ahc.py` (WannierBerri runner), `rotate_mag.py` (magnetization rotation), `calc_energy.py`, `submit_ahc_all.py` (batch submission), `time.py` |
| Destination | archived settings summarized in `REPO/inputs/wannierberri/fe_bcc_rotation/workflow_snapshots.json`, processed CSV (already present) → `REPO/data/processed/ahc_111/`, plot script (already present) → `REPO/scripts/reproduce_figures/plot_ahc_111.py` |

### `fit_ahc_para_103`, `fit_ahc_perp_103`, `fit_ahc_axis_103` ((103) plane)

| Item | Path / value |
| --- | --- |
| Local PDFs | `PAPER/figs/Fe/FM_sqa_103/anisotropy/{fit_ahc_para,fit_ahc_perp,fit_ahc_axis}.pdf` (note: locally **without** `_103` suffix; renamed in repo) |
| Generating script | `PAPER/figs/Fe/FM_sqa_103/anisotropy/fit_ahc.py` |
| Input data | `PAPER/figs/Fe/FM_sqa_103/anisotropy/angle_dep_ahc.xml` (301 lines) + variants |
| Driver scripts | same family as (111): `ahc.py`, `rotate_mag.py`, `calc_energy.py`, `submit_ahc_all.py`, `plot_ahc.py`, `fit_ahc.py`, `plot_angle_dep.py`, `time.py` |
| Destination | archived settings summarized in `REPO/inputs/wannierberri/fe_bcc_rotation/workflow_snapshots.json`, processed CSV (already) → `REPO/data/processed/ahc_103/`, plot script (already) → `REPO/scripts/reproduce_figures/plot_ahc_103.py` |

### `sigma_para_group{1,2,3}`, `sigma_perp_group{1,2,3}`, `sigma_axis_group{1,2,3}` (rank-cumulative (103))

| Item | Path / value |
| --- | --- |
| Local PDFs | `PAPER/figs/Fe/FM_sqa_103/anisotropy_w_rank3/sigma_{para,perp,axis}_group{1,2,3,4}.pdf` (group4 also exists locally but is not in the manuscript inventory) |
| Generating script | `PAPER/figs/Fe/FM_sqa_103/anisotropy_w_rank3/plot_ahc.py` (group definition embedded; verify exact assignment) |
| Input data | `PAPER/figs/Fe/FM_sqa_103/anisotropy_w_rank3/angle_dep_w_rank{1, 1_2, 1_2_3, 1_2_3_4, 1_2_3_4_5, 1_2_3_4_5_6, 1_2_3_4_5_6_7, 1_2_3_4_5_6_7_8}.xml` + reference `angle_dep_ahc.xml` |
| Destination | archived settings summarized in `REPO/inputs/wannierberri/fe_bcc_rotation/workflow_snapshots.json`, processed CSV (already) → `REPO/data/processed/rank_resolved_103/`, plot script (already) → `REPO/scripts/reproduce_figures/plot_rank_resolved_103.py` |

### `sigma_para`, `sigma_perp`, `sigma_axis` (single-rank (103))

| Item | Path / value |
| --- | --- |
| Local PDFs | `PAPER/figs/Fe/FM_sqa_103/anisotropy_w_rank3/{sigma_para,sigma_perp,sigma_axis}.pdf` |
| Generating script | same `plot_ahc.py` as above |
| Input data | same `angle_dep_w_rank*.xml` files |
| Destination | merged with rank-cumulative under `REPO/data/processed/rank_resolved_103/single_rank_ahc.csv` and `REPO/scripts/reproduce_figures/plot_rank_resolved_103.py` |

### `sigma_plus_strain_sigma_axis`, `sigma_minus_strain_sigma_axis` ([103] strain)

| Item | Path / value |
| --- | --- |
| Local PDFs | `PAPER/figs/Fe/FM_sqa_103_strained_along_103/sigma_plus_strain_sigma_axis.pdf`, `sigma_minus_strain_sigma_axis.pdf` (and `_para`, `_perp`, `_xy`, `_yz`, `_zx` variants) |
| Generating script | `PAPER/figs/Fe/FM_sqa_103_strained_along_103/strain_103.py` |
| Structure inputs | `PAPER/figs/Fe/FM_sqa_103_strained_along_103/structures/{scf.cif, scf_20percent.cif, scf_m20percent.cif, scf.in, strain.py, qe2cif.py}` |
| Destination | archived strain workflow summarized in `REPO/inputs/wannierberri/fe_bcc_strain_103/strain_manifest.json`, public deformation helper → `REPO/scripts/workflow/strain_103_cell.py`, DFT template → `REPO/inputs/dft/fe_bcc_strain_103/`, processed CSV (already) → `REPO/data/processed/strain_103/`, plot script (already) → `REPO/scripts/reproduce_figures/plot_strain_103.py` |

### `sigma_axis_model_1st_nn`, `sigma_axis_model_2nd_nn` (minimal p_z-d_xy model)

| Item | Path / value |
| --- | --- |
| Manuscript references | `PAPER/body/arXiv/main_all.tex` lines ~1275, 1281; same in CPC/PRB |
| Archived generator | `2025/発表/defense/figs/model.py` |
| Archived direct outputs | `2025/doctoral_thesis/hirotosaito/tests/bcc_model/{1st_nn_t2_0,2nd_nn_t1_0.2}/t_T_*/psi_*/sigma_ahc_eta1.00meV.txt` |
| Current public-repo provenance | direct compact export in `REPO/data/source/production_exports/minimal_model/model_sigma_axis.csv` + archived example in `REPO/examples/minimal_model/model.py` |
| Destination | `model.py` → `REPO/examples/minimal_model/model.py`; compact export helper → `REPO/scripts/workflow/export_minimal_model_source.py`; processed CSV → `REPO/data/processed/minimal_model/` |

## DFT / Wannier Input Files

The SOC + magnetization-rotation production inputs are scattered across the
paper workspace. The under-100-MB files needed for `REPO/inputs/dft/` and
`REPO/inputs/wannier/` are:

| File | Local path | Notes |
| --- | --- | --- |
| `scf.in` (collinear nspin=2, Fe BCC, m=3.0) | `PAPER/figs/Fe/FM_sqa_z/hamiltonian_hdf5_trs/energy_diff1/symwannier/scf.in` (identical to `energy_diff2/symwannier/scf.in`) | uses `pseudo_dir = /home/koretsune/PWSCF/pseudo_psl031`; reference pseudo `Fe.pbe-spn-rrkjus_psl.0.2.1.UPF` |
| `nscf.in` | same dir | |
| `pwscf.win` | same dir | `spinors = .true.`, `num_bands = 50`, `num_wann = 18`, `mp_grid: 8 8 8`, explicit k-list embedded |
| `pw2wan.in` | same dir | |
| `scf.in` (strain workflow) | `PAPER/figs/Fe/FM_sqa_103_strained_along_103/structures/scf.in` | for [103] strain DFT |
| `strain.py`, `qe2cif.py` | same dir | strain cell generator + cif converter |
| `scf.cif`, `scf_20percent.cif`, `scf_m20percent.cif` | same dir | strained cells |
| Wannier90 path | `energy_diff1/wannier90/{scf.in,nscf.in,pwscf.win,pw2wan.in}` | alternative path, same SCF settings |

> **Caveat**: the `pseudo_dir` value is a hard-coded private absolute path
> (`/home/koretsune/PWSCF/pseudo_psl031`). It must be replaced with a
> repository-relative or `$PSEUDO_DIR` placeholder when copied into `inputs/`.

> **Caveat**: these inputs are `nspin = 2` (collinear) without explicit
> `noncolin = .true.` / `lspinorb = .true.`. If the manuscript main results
> require fully relativistic SOC inputs, those production inputs may live in
> a different local directory not surfaced here. **Open question** — verify
> whether SOC inputs exist elsewhere (e.g. `PAPER/figs/Fe/FM_sqa_z/theta0_qe-7.2/`
> root or a non-listed sibling).

There are also non-SOC validation inputs in `SYMWAN/tests/Fe/num_iter_0/`:

| Path | Purpose |
| --- | --- |
| `SYMWAN/tests/Fe/num_iter_0/FM_wo_soc_SW/{scf.in,nscf.in,pw2wan.in,pwscf.win,submit.sh}` | site-symmetry path |
| `SYMWAN/tests/Fe/num_iter_0/FM_wo_soc_PD/{scf.in,...}` | projectability disentanglement |
| `SYMWAN/tests/Fe/num_iter_0/FM_wo_soc_SW_PD/{scf.in,...}` | both |

These belong in `REPO/examples/fe_bcc_non_soc/{SW,PD,SW_PD}/` to provide a
small running example distinct from the production SOC workflow.

## SymWannier / TRS-Wannier Driver

| Item | Local path | Destination |
| --- | --- | --- |
| `energy_diff_fe.py` (MPI-aware Hamiltonian rebuild + accuracy log) | `PAPER/figs/Fe/FM_sqa_z/hamiltonian_hdf5_trs/energy_diff/energy_diff_fe.py` | `REPO/inputs/symwannier/fe_bcc/energy_diff_fe.py` |
| `submit_energy_diff.sh` (PBS, runs `energy_diff_fe.py` four times with rank filters) | same dir | `REPO/inputs/symwannier/fe_bcc/submit_energy_diff.sh` |
| `plot_energy_diff.py` | `SYMWAN/tests/Fe/num_iter_0/energy_diff/plot_energy_diff.py` (28K, equivalent) | `REPO/scripts/workflow/plot_energy_diff.py` or `REPO/inputs/symwannier/fe_bcc/` |
| `energy_diff_35_all.out` and rank-filtered `energy_diff_35_a1g_t1g[_eg[_t2g]].out` | `PAPER/figs/Fe/FM_sqa_z/{theta0_qe-7.2,hamiltonian_hdf5_trs/energy_diff,...}` | `REPO/data/source/energy_diff/` |

## MultiPie / SAMB Input

| Item | Local path | Destination |
| --- | --- | --- |
| `Fe.py` (22 lines, group 229, sites Fe s/p/d, bond shells 1-35, spinful) | `SYMWAN/tests/Fe/num_iter_0/multipie/Fe_all_35/Fe.py` | `REPO/inputs/multipie/fe_bcc/Fe.py` |
| `Fe_model.py` | same dir | `REPO/inputs/multipie/fe_bcc/Fe_model.py` |
| `submit_samb.sh` (PBS, runs MultiPie + `samb2tex.py` for selected z indices: 86479, 86449, …) | same dir | `REPO/inputs/multipie/fe_bcc/submit_samb.sh` |
| `out_ed/`, `out_pd/`, `out_trs_ed/` (MultiPie outputs) | `PAPER/figs/Fe/FM_sqa_z/multipole/{out_ed,out_pd,out_trs_ed}/` | reference only; not copied — outputs are regenerated by MultiPie |

> The `submit_samb.sh` references `SRC_DIR=/home/hirotosaito/github_projects/symwan_multipie/src/`.
> This must be replaced with a relative path resolved from the repository.

## WannierBerri AHC Driver

The AHC + magnetization-rotation workflow is shared across `(111)`, `(103)`,
`(103)_w_rank3`, and `_strained_along_103`. Each workflow directory has:

| Script | Role |
| --- | --- |
| `ahc.py` | WannierBerri runner (consumes rotated Hamiltonian for each angle, writes per-angle AHC) |
| `rotate_mag.py` | magnetization rotation (uses `src/symwan_multipie/mag_rotation.py` or its predecessor) |
| `calc_energy.py` | reconstruction-error sanity check |
| `submit_ahc_all.py` | batch-submission orchestrator (Python script that builds PBS jobs) |
| `fit_ahc.py`, `fit_angle_dep.py` | fitting routines for plotting |
| `plot_ahc.py`, `plot_angle_dep.py`, `plot_kmesh_dep.py` | plotting routines |
| `time.py` | timing utility |

These should be copied (deduplicated where identical) into:

| Source | Destination |
| --- | --- |
| `PAPER/figs/Fe/FM_sqa_111/anisotropy/` | summarized in `REPO/inputs/wannierberri/fe_bcc_rotation/workflow_snapshots.json` |
| `PAPER/figs/Fe/FM_sqa_103/anisotropy/` | summarized in `REPO/inputs/wannierberri/fe_bcc_rotation/workflow_snapshots.json` |
| `PAPER/figs/Fe/FM_sqa_{111,103}/anisotropy_w_rank{2,3}/` | summarized in `REPO/inputs/wannierberri/fe_bcc_rotation/workflow_snapshots.json` |
| `PAPER/figs/Fe/FM_sqa_103_strained_along_103/` (driver `strain_103.py`) | `REPO/inputs/wannierberri/fe_bcc_strain_103/` |

> Many of these scripts have hard-coded absolute paths to private Hamiltonian
> files. The maintainer must rewrite paths to use a repository-relative
> `HAMILTONIAN_PATH` env var or argparse argument before committing.

## Python Package Modules

### From `SYMWAN/src/symwannier/` → `REPO/src/symwan_multipie/symwannier/`

| Module | Size | Role |
| --- | --- | --- |
| `wannierize.py` | 41 KB | Wannierization main (CLI: `-S` site-symmetry, `-P` projectability) |
| `expand_wannier_inputs.py` | 1.8 KB | IBZ → full BZ symmetry expansion |
| `sym.py` | 13 KB | symmetry operations |
| `cli.py` | 1.0 KB | command-line dispatch |
| `win.py`, `nnkp.py`, `amn.py`, `mmn.py`, `eig.py` | 1.5–12 KB | Wannier90 I/O readers/writers |
| `io_utils.py` | 0.9 KB | I/O helpers |
| `timedata.py` | 2.2 KB | timing |
| `__init__.py` | empty | namespace marker (no re-export) |

Total: 11 files, ~92 KB. All <100 MB. Move verbatim; adjust imports
(`from symwannier.X` → `from symwan_multipie.symwannier.X` or keep relative).

### From `SYMWAN/src/wannier_utils/` → `REPO/src/symwan_multipie/wannier_utils/`

23 main files (~193 KB total) + 3 archive files. Key modules:

| Module | Size | Role |
| --- | --- | --- |
| `wannier_system.py` | 9.4 KB | Hamiltonian system base class |
| `hamiltonian.py` | 18 KB | Hamiltonian I/O + manipulation |
| `band.py` | 7.8 KB | band-structure computation |
| `berry.py` | 5.1 KB | Berry curvature |
| `dos.py` | 17 KB | DOS computation |
| `exchange.py`, `exchange_input.py` | 25 KB + 2.7 KB | exchange interactions |
| `mag_sym.py` | 7.7 KB | magnetic symmetry |
| `fourier.py` | 5.0 KB | FT helpers |
| `boltz.py` | 5.3 KB | Boltzmann transport |
| `mp_points.py` | 4.7 KB | Monkhorst-Pack grids |
| `parallel.py` | 5.7 KB | MPI helpers |
| `phys_matrix.py` | 3.9 KB | physical-matrix utilities |
| `cpa.py` | 6.4 KB | CPA |
| `nnkp.py`, `win.py` | 4.1 KB, 6.3 KB | Wannier I/O |
| `wannier_kmesh.py` | 1.5 KB | k-mesh utilities |
| `mymodule.py` | 1.8 KB | misc |
| `wannier_system_main.py` | 9.2 KB | CLI front-end |
| `temperature_spir.py` | 2.0 KB | SpiR temperature mapping |
| `green.py` | 2.2 KB | Green's function |
| `logger.py` | 1.0 KB | logging |
| `__init__.py` | 90 B | logging setup |

Archive subdir (skip unless needed): `ham_kmesh.py`, `temperature_ir2.py`,
`Jij.py`.

The current `REPO/src/symwan_multipie/wannier_utils/` has only `band.py` and
`hamiltonian.py`. **Diff against the symwan_proj versions before overwriting**
— the public-repo copy may have local fixes worth preserving.

### Already in `REPO/src/symwan_multipie/` (do not overwrite)

| Module | Origin |
| --- | --- |
| `multipole.py` | not in symwan_proj (developed in public repo) |
| `multipole_decomposition.py` | not in symwan_proj |
| `single_multipole_reader.py` | not in symwan_proj |
| `mag_rotation.py` | not in symwan_proj |
| `energy_diff.py` | not in symwan_proj as a module (only `energy_diff_fe.py` test) |

## Modified Quantum ESPRESSO 7.4.1

| Item | Local path | Destination |
| --- | --- | --- |
| Modified `pw2wannier90.f90` | `SYMWAN/src/qe-7.4.1_pw2wan/PP/src/pw2wannier90.f90` (279 KB) | not committed; diff extracted |
| Original `pw2wannier90.f90` | `SYMWAN/src/qe-7.4.1_pw2wan_orig/PP/src/pw2wannier90.f90` (278 KB) | not committed |
| Generated patch | `REPO/docs/qe_patch/pw2wannier90.patch` (to be produced via `diff -u`) |
| Patch README | `REPO/docs/qe_patch/README.md` — describes upstream commit hash, build steps |

Modification summary (for the patch header):

- adds `irr_bz` flag for irreducible-BZ + `atom_proj` co-existence;
- new subroutine `compute_amn_with_atomproj` (re-allocates `natomwfc`-shaped
  arrays);
- removes obsolete `atom_proj_sym` flag;
- fixes non-collinear spinor initialization in `atom_proj`;
- moves projector phase convention into `rotmat`;
- redirects `irr_bz` merges to `iamn`.

## Pseudopotentials

Not redistributed. Recorded only:

| Element | Pseudo name (from scf.in) | Source |
| --- | --- | --- |
| Fe | `Fe.pbe-spn-rrkjus_psl.0.2.1.UPF` | PS Library (PSlibrary) — link in `REPO/inputs/dft/README.md` |

The hard-coded `pseudo_dir = /home/koretsune/PWSCF/pseudo_psl031` in all
`scf.in` / `nscf.in` files must be rewritten before commit.

## Workflow Stage → Destination Summary

| Stage | Local source (PAPER + SYMWAN) | Destination in `REPO/` |
| --- | --- | --- |
| DFT (unstrained SOC) | `PAPER/figs/Fe/FM_sqa_z/hamiltonian_hdf5_trs/energy_diff{1,2}/symwannier/{scf,nscf,pw2wan}.in` + `pwscf.win` | `inputs/dft/fe_bcc_unstrained/` + `inputs/wannier/fe_bcc_unstrained/` |
| DFT (strain) | `PAPER/figs/Fe/FM_sqa_103_strained_along_103/structures/{scf.in, strain.py, qe2cif.py, scf*.cif}` | `inputs/dft/fe_bcc_strain_103/` + `scripts/workflow/strain_103_cell.py` |
| DFT (non-SOC reference) | `SYMWAN/tests/Fe/num_iter_0/FM_wo_soc_*/` | `examples/fe_bcc_non_soc/{SW,PD,SW_PD}/` |
| Wannier90 | `PAPER/.../symwannier/pwscf.win, pw2wan.in` | `inputs/wannier/fe_bcc_unstrained/` |
| SymWannier / TRS-Wannier | `PAPER/figs/Fe/FM_sqa_z/hamiltonian_hdf5_trs/energy_diff/{energy_diff_fe.py, submit_energy_diff.sh}` | `inputs/symwannier/fe_bcc/` |
| MultiPie / SAMB | `SYMWAN/tests/Fe/num_iter_0/multipie/Fe_all_35/{Fe.py, Fe_model.py, submit_samb.sh}` | `inputs/multipie/fe_bcc/` |
| Magnetization rotation + WannierBerri (111) | `PAPER/figs/Fe/FM_sqa_111/anisotropy/{ahc.py, rotate_mag.py, calc_energy.py, submit_ahc_all.py, angle_dep_*.xml, kmesh_dep_*.xml}` | `inputs/wannierberri/fe_bcc_rotation/` + `inputs/wannierberri/fe_bcc_rotation/workflow_snapshots.json` |
| Magnetization rotation + WannierBerri (103) | `PAPER/figs/Fe/FM_sqa_103/anisotropy/` (same set) | `inputs/wannierberri/fe_bcc_rotation/` + `inputs/wannierberri/fe_bcc_rotation/workflow_snapshots.json` |
| Rank-resolved (103) | `PAPER/figs/Fe/FM_sqa_103/anisotropy_w_rank3/{plot_ahc.py, angle_dep_w_rank*.xml, ahc.py, ...}` | `inputs/wannierberri/fe_bcc_rotation/workflow_snapshots.json` |
| Strain workflow | `PAPER/figs/Fe/FM_sqa_103_strained_along_103/strain_103.py` + `structures/` | `inputs/wannierberri/fe_bcc_strain_103/` + `inputs/dft/fe_bcc_strain_103/` + `scripts/workflow/strain_103_cell.py` |
| Extract (CSV) | (existing) `scripts/workflow/extract_*.py` + new ones to read local XML | `scripts/workflow/` (extend) |
| Figures | (existing) `scripts/reproduce_figures/plot_*.py` + `plot_bcc_planes.py`, `plot_band_bond.py` | `scripts/reproduce_figures/` |

## Large Files (>100 MB) — Document Only

| Class | Approximate local path | Expected size | Regeneration recipe |
| --- | --- | --- | --- |
| `Hamiltonian.h5` (TRS-Wannier full) | `PAPER/figs/Fe/FM_sqa_z/hamiltonian_hdf5_trs/Hamiltonian.h5` (not currently present in the local tree per `find -size +100M` — likely already pruned; regenerate from QE + Wannier + SymWannier) | up to several GB | run `wannierize -P` then `MultipoleDecomposition` to produce HDF5 |
| Full QE SCF/NSCF save directories | `PAPER/figs/Fe/FM_sqa_z/theta0_qe-7.2/work/` (typical) | up to several GB | run `scf.in` then `nscf.in` |
| WannierBerri AHC intermediate outputs | per-angle WB workspaces | up to hundreds of MB each | run `ahc.py` |
| Modified QE 7.4.1 full tree | `SYMWAN/src/qe-7.4.1_pw2wan/` | >100 MB | apply `docs/qe_patch/pw2wannier90.patch` to upstream QE 7.4.1 |

These four classes are the only ones expected to exceed the 100 MB limit.

## Open Questions To Resolve Before Phase B

1. **SOC (fully relativistic) DFT inputs**: The `scf.in` files surfaced in
   `hamiltonian_hdf5_trs/energy_diff{1,2}/` use `nspin = 2` (collinear).
   Verify whether the production runs that fed the manuscript AHC were
   `nspin = 4` + `lspinorb = .true.`, and if so locate those inputs.
2. **Disambiguation between `theta0_qe-7.2/z_coefficients/` and
   `hamiltonian_hdf5_trs/z_coefficients/`**: both contain identical-looking
   `bar_ed_all_35.pdf` and `plot_bar.py`. Which is canonical for the
   manuscript?
3. **`SYMWAN/src/wannier_utils/{band,hamiltonian}.py` vs current public-repo
   versions**: take a unified diff before overwriting.

## Hard-Coded Paths To Rewrite During Copy

| File class | Hard-coded value | Replacement |
| --- | --- | --- |
| All `scf.in` / `nscf.in` | `pseudo_dir = /home/koretsune/PWSCF/pseudo_psl031` | `$PSEUDO_DIR` / repository-relative placeholder |
| `submit_samb.sh` | `SRC_DIR=/home/hirotosaito/github_projects/symwan_multipie/src/` | resolved from `inputs/multipie/fe_bcc/README.md` |
| `submit_energy_diff.sh` | `~/miniconda3/envs/h5py-mpi/` | template note; user must adapt |
| `conftest.py` (SYMWAN) | `WORKFLOW_TMP_ROOT = /home2/hirotosaito/tmp` | not migrated — public-repo tests stay synthetic |
| Driver scripts (`ahc.py`, `rotate_mag.py`, …) | private absolute paths to Hamiltonian HDF5 / Wannier dirs | `HAMILTONIAN_PATH` env var or argparse |

## License Notes

| Component | License | Repo handling |
| --- | --- | --- |
| Quantum ESPRESSO 7.4.1 (and modified tree) | GPL-2.0 | patch only, with upstream source URL |
| Wannier90 | GPL-2.0 | external dependency (link in README) |
| MultiPie | check upstream | external dependency |
| WannierBerri | check upstream | external dependency |
| Pseudopotentials (PSlibrary) | PSlibrary terms | not redistributed; documented link |
| `symwannier`, `wannier_utils` | not explicitly stated upstream | match `REPO/LICENSE`; confirm with Koretsune-sensei before publication |
