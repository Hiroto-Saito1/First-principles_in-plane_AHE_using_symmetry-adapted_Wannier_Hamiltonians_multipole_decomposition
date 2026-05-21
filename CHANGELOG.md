# Changelog

All notable repository-facing updates to this public reproducibility package
are recorded here.

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
