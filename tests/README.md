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
  committed under `figures/paper/`, represented in the figure inventory, and
  kept below the 100 MB Git policy threshold.
- `test_processed_figure_data.py`: validates compact processed CSV data for
  the band/bond convergence curves, `(111)` and `(103)` AHC curves,
  rank-cumulative `(103)` data, tensile/compressive `[103]` strain series,
  recovered multipole coefficients, and archived minimal-model scans.
- `test_inputs.py`: checks that curated first-principles input groups have
  reader-facing README files, preserve the key rotation/AHC settings in JSON
  manifests, and do not embed private absolute paths.

## Running

```bash
python -m pip install -e ".[test]"
pytest
```
