# Changelog

All notable repository-facing updates to this public reproducibility package
are recorded here.

## v0.1.3 - 2026-05-26

- restored the paper-facing `(103)` rank-resolved figures to the committed
  reference vocabulary (`w/ rank ...` and `all`) together with the archived
  marker and linestyle roles;
- restored the paper-facing `fit_ahc` visual roles so the six `(111)`/`(103)`
  panels now use reference-style `model`, `DFT`, and `fitting` encodings on
  top of the already recovered compact sources;
- centralized paper, diagnostic, and contact-sheet dependency tracking in
  `scripts/workflow/figure_dependencies.py` and taught
  `scripts/reproduce_all_figures.sh --check` to validate mode-specific
  requirements instead of one blended file list;
- corrected the `fit_ahc` figure-inventory notes so they explicitly record the
  committed DFT compact inputs used by the paper-facing panels;
- expanded regression coverage for reference-facing figure roles and
  dependency-failure paths, raising the default suite to 70 passing tests.

## v0.1.2 - 2026-05-26

- split generated outputs into manuscript-facing
  `results/figures_paper/` and diagnostic
  `results/figures_diagnostics/` trees, and added a contact-sheet workflow for
  reviewing generated paper plots against committed `figures/paper/`
  references;
- recovered archived `fit_ahc` compact sources for both the `model` and `DFT`
  paper roles, so the paper-facing `(111)` and `(103)` `fit_ahc` panels are
  again backed by committed compact exports plus explicit contracts;
- added paper-facing reference-information contracts for the remaining plot
  families, including rank-resolved `(103)`, `[103]` strain, minimal-model
  scans, band/bond convergence, multipole bar plots, and the `(111)`/`(103)`
  geometric definition figures;
- strengthened `scripts/reproduce_all_figures.sh --check` so it now guards the
  recovered `fit_ahc` sources and the current paper-facing contract manifests;
- hardened public-path hygiene, added a dedicated
  `docs/redistribution_status.md` note for the copied archived module trees,
  and removed avoidable Python 3.13 `SyntaxWarning` output from archived
  `wannier_utils` docstrings while adding regression coverage for that check.

## v0.1.1 - 2026-05-21

- marked the public reproducibility reorganization as complete on `main`;
- added release-facing documentation, including this changelog and
  `docs/README.md`;
- fixed `HamK.get_minus_d_fermi` so it stores eigenvalues rather than the tuple
  returned by `numpy.linalg.eigh`;
- clarified the package dependency boundary between the lightweight public API
  and `.[workflow]` optional dependencies;
- clarified the public mixed-license policy: repository-authored code under
  MIT, documentation/data/figure artifacts under CC BY 4.0, and copied
  archived module trees temporarily excluded pending upstream confirmation;
- removed `docs/source_inventory.md` and the extra
  `Yourmanuscript BN15047 Saito.pdf` artifact from the public release set;
- updated `README.md`, `CITATION.cff`, and `plan.md` so the public reuse scope
  matches the current repository policy.

## v0.1.0 - 2026-05-21

Initial public reproducibility package for the manuscript
_First-principles analysis of in-plane anomalous Hall effect using
symmetry-adapted Wannier Hamiltonians and multipole decomposition_
([arXiv:2601.05689](https://arxiv.org/abs/2601.05689)).

### Included in this release

- compact processed figure data for the manuscript's repository-backed plots;
- plotting scripts for `(111)` and `(103)` AHC, rank-resolved `(103)` AHC,
  `[103]` strain, multipole-coefficient bars, minimal-model scans, and the
  recovered band/bond convergence figure;
- curated production input templates and workflow manifests for DFT,
  Wannier90, SymWannier/TRS-Wannier, MultiPie/SAMB, and WannierBerri;
- the public `symwan_multipie` Python package, including archived
  `symwannier/` and main `wannier_utils/` modules plus lightweight workflow
  helpers;
- archived regeneration recipes for large intermediate artifacts that are not
  stored in Git, including the documented `Fe_all_35` multipole rebuild path;
- lightweight regression tests, figure smoke tests for the non-heavy plotting
  scripts, and GitHub Actions CI coverage for the default reproducibility
  checks.

### Known limitations carried into v0.1.0

- files larger than 100 MB are intentionally not tracked in Git;
- the committed multipole-coefficient CSV remains a recovered compact snapshot,
  although the full archived rebuild route is documented;
- the intentionally heavier `bcc` 3D plane plots and `band_bond` redraw are
  excluded from the default figure smoke tests, but their processed data,
  plotting scripts, and inventory entries are still checked.

### Suggested citation scope

Use this release when citing the first public reproducibility package that
matches the repository state described in `plan.md`, `docs/workflow.md`, and
the default CI workflow under `.github/workflows/tests.yml`.
