from __future__ import annotations

import numpy as np

from symwan_multipie import Multipole, MultipoleDecomposition


def test_hamiltonian_decomposition_reconstructs_fixture(multipie_pickle, fixture_ham, tmp_path):
    multipole_path = tmp_path / "basis.hdf5"
    Multipole(multipie_pickle).write_hdf5(multipole_path)

    decomposition = MultipoleDecomposition(fixture_ham, multipole_path)
    reconstructed = decomposition.reconstruct()

    assert np.allclose(reconstructed, fixture_ham.hrs, atol=1e-14)
    assert np.allclose(decomposition.z_coefficients.imag, 0.0, atol=1e-14)


def test_decomposition_hdf5_output_is_readable(multipie_pickle, fixture_ham, tmp_path):
    multipole_path = tmp_path / "basis.hdf5"
    output_path = tmp_path / "decomposition.hdf5"
    Multipole(multipie_pickle).write_hdf5(multipole_path)

    decomposition = MultipoleDecomposition(fixture_ham, multipole_path)
    decomposition.write_hdf5(output_path)

    assert output_path.exists()

