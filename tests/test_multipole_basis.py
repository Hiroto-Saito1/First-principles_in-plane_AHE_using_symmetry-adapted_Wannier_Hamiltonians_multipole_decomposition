"""Tests for loading and validating the synthetic multipole basis fixture."""

from __future__ import annotations

import numpy as np

from symwan_multipie import Multipole


def test_multipole_hdf5_roundtrip(multipie_pickle, tmp_path):
    """Verify that a MultiPie-style pickle can be loaded and written as HDF5."""
    multipole = Multipole(multipie_pickle)
    assert multipole.num_multipole == 4
    assert multipole.nrpts == 1
    assert multipole.num_wann == 2

    hdf5_path = tmp_path / "multipole_matrix.hdf5"
    multipole.write_hdf5(hdf5_path)

    reloaded = Multipole(multipie_pickle)
    assert hdf5_path.exists()
    assert np.array_equal(reloaded.irvec, np.array([[0, 0, 0]]))


def test_multipole_orthonormality(multipie_pickle):
    """Check that the fixture multipole matrices are orthonormal under trace overlap."""
    multipole = Multipole(multipie_pickle)
    dense = multipole.multipole.todense()
    overlap = np.einsum("arij,brij->ab", np.conjugate(dense), dense)
    assert np.allclose(overlap, np.eye(4), atol=1e-14)
