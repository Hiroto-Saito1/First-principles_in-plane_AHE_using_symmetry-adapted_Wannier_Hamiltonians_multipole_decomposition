from __future__ import annotations

import numpy as np

from symwan_multipie import MagRotation, Multipole, MultipoleDecomposition


def test_filter_z_indices(multipie_pickle, fixture_ham, samb_path, tmp_path):
    multipole_path = tmp_path / "basis.hdf5"
    multi_path = tmp_path / "multi.hdf5"
    Multipole(multipie_pickle).write_hdf5(multipole_path)
    MultipoleDecomposition(fixture_ham, multipole_path).write_hdf5(multi_path)

    rotation = MagRotation(multi_path=multi_path, samb_path=samb_path)
    try:
        assert rotation.filter_z_indices(types=["M"], ranks=[1], irreps=["T1g"]).tolist() == [1]
        assert rotation.filter_z_indices(types=["T"], ranks=[4], irreps=["T1g"]).tolist() == [3]
    finally:
        rotation.close()


def test_spin_rotation_maps_sigma_z_to_sigma_x(multipie_pickle, samb_path, tmp_path):
    multipole_path = tmp_path / "basis.hdf5"
    multi_path = tmp_path / "multi.hdf5"
    Multipole(multipie_pickle).write_hdf5(multipole_path)

    sigma_z = np.array([[[1, 0], [0, -1]]], dtype=np.complex128)
    from symwan_multipie.wannier_utils.hamiltonian import HamR

    ham = HamR(irvec=np.array([[0, 0, 0]]), ndegen=np.array([1]), hrs=sigma_z)
    MultipoleDecomposition(ham, multipole_path).write_hdf5(multi_path)

    rotation = MagRotation(
        multi_path=multi_path,
        samb_path=samb_path,
        filters=[
            {
                "types": ["M"],
                "ranks": [1],
                "irreps": ["T1g"],
                "axis1": [0.0, 1.0, 0.0],
                "axis2": [0.0, 0.0, 1.0],
                "theta": 90.0,
                "phi": 0.0,
            }
        ],
    )
    try:
        expected = np.array([[[0, 1], [1, 0]]], dtype=np.complex128)
        assert np.allclose(rotation.rotated_hamiltonian(), expected, atol=1e-14)
    finally:
        rotation.close()

