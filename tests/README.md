# Test Suite

The default tests are lightweight checks for the public data-availability
repository. They use synthetic Hamiltonian fixtures and compact processed
figure data, so they do not require the full DFT, SymWannier, MultiPie,
WannierBerri, MPI, or cluster calculation directories.

## Files

- `conftest.py`: builds the shared two-orbital Pauli-basis fixture, a small
  SAMB label file, and a synthetic `HamR` Hamiltonian used by the package
  tests.
- `test_multipole_basis.py`: verifies MultiPie-style sparse matrix loading,
  HDF5 writing, and orthonormality of the fixture multipole basis.
- `test_decomposition.py`: checks that a Hamiltonian decomposed in the complete
  fixture basis reconstructs the original matrix and writes readable HDF5
  output.
- `test_mag_rotation.py`: checks SAMB metadata filtering and a simple analytic
  spin-rotation case that maps `sigma_z` to `sigma_x`.
- `test_energy_diff.py`: verifies that reconstruction-based band-energy
  differences vanish for the complete synthetic fixture.
- `test_paper_figures.py`: ensures every PDF referenced by `main_all.tex` is
  committed under `figures/paper/`, represented in the figure inventory, kept
  below the 100 MB Git policy threshold, and that the lighter repository plot
  scripts can emit non-empty PDFs in a smoke-test environment.
- `test_processed_figure_data.py`: validates compact processed CSV data for
  the band/bond convergence curves, `(111)` and `(103)` AHC curves,
  rank-cumulative `(103)` data, tensile/compressive `[103]` strain series,
  recovered multipole coefficients, and archived minimal-model scans.
- `test_inputs.py`: checks that curated first-principles input groups have
  reader-facing README files, preserve the key rotation/AHC settings in JSON
  manifests, and do not embed private absolute paths.
- `test_package_layout.py`: verifies that the copied `symwannier/` and
  `wannier_utils/` module sets are present under `src/`, use repo-local
  imports, and preserve the lightweight `HamK` / helper import surface.

## Running

```bash
python -m pip install -e ".[test]"
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 pytest -q
```

The default suite matches the lightweight CI path. It includes figure smoke
tests for the non-heavy plotting scripts and excludes the intentionally heavier
`bcc` 3D plane plots and `band_bond` redraw from the default smoke route.

The package-layout tests also enforce the current dependency boundary:
top-level imports and the lightweight `wannier_utils` surface must work
without the workflow-only dependencies, while modules such as
`symwan_multipie.wannier_utils.win` are allowed to require
`pip install -e ".[workflow]"`.
