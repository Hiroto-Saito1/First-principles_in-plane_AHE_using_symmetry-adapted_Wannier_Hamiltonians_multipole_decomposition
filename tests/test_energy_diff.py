"""Tests for band-energy reconstruction errors from decomposed Hamiltonians."""

from __future__ import annotations

from symwan_multipie import EnergyDiff, Multipole, MultipoleDecomposition


def test_energy_diff_is_zero_for_complete_fixture(multipie_pickle, fixture_ham, samb_path, tmp_path):
    """Confirm that energy differences vanish when all fixture multipoles are retained."""
    multipole_path = tmp_path / "basis.hdf5"
    multi_path = tmp_path / "multi.hdf5"
    Multipole(multipie_pickle).write_hdf5(multipole_path)
    MultipoleDecomposition(fixture_ham, multipole_path).write_hdf5(multi_path)

    diff = EnergyDiff(fixture_ham, multi_path=multi_path, samb_path=samb_path, kmesh=(1, 1, 1))

    assert diff.max_diff < 1e-14
    assert diff.energy_diff < 1e-14
