"""Shared fixtures for lightweight multipole-decomposition tests."""

from __future__ import annotations

import pickle
from pathlib import Path

import numpy as np
import pytest

from symwan_multipie.wannier_utils.hamiltonian import HamR


SQRT2_INV = 1 / np.sqrt(2)


def pauli_basis() -> list[np.ndarray]:
    """Return a normalized two-orbital Pauli basis used as a complete SAMB fixture."""
    identity = SQRT2_INV * np.array([[1, 0], [0, 1]], dtype=np.complex128)
    sigma_z = SQRT2_INV * np.array([[1, 0], [0, -1]], dtype=np.complex128)
    sigma_x = SQRT2_INV * np.array([[0, 1], [1, 0]], dtype=np.complex128)
    sigma_y = SQRT2_INV * np.array([[0, -1j], [1j, 0]], dtype=np.complex128)
    return [identity, sigma_z, sigma_x, sigma_y]


def matrix_dict_from_basis() -> dict:
    """Build a MultiPie-like sparse matrix dictionary from the Pauli fixture basis."""
    entries = {}
    labels = ["z_000", "z_001", "z_002", "z_003"]
    for label, matrix in zip(labels, pauli_basis()):
        elements = {}
        for row in range(2):
            for col in range(2):
                value = matrix[row, col]
                if value != 0:
                    elements[(0, 0, 0, row, col)] = value
        entries[label] = elements
    return {"matrix": entries}


def write_samb(path: Path) -> None:
    """Write a minimal SAMB metadata file with labels used by rotation filters."""
    path.write_text(
        """
fixture_samb = {
    "data": {
        "Z": {
            "z_000": "Q(0,A1g,,0|0,0)",
            "z_001": "M(1,T1g,,0|1,0)",
            "z_002": "Q(2,Eg,,0|1,0)",
            "z_003": "T(4,T1g,,0|1,0)",
        }
    }
}
""".lstrip(),
        encoding="utf-8",
    )


@pytest.fixture
def multipie_pickle(tmp_path: Path) -> Path:
    """Create a temporary MultiPie-style pickle containing the fixture basis."""
    path = tmp_path / "fixture_matrix.pkl"
    with path.open("wb") as fp:
        pickle.dump(matrix_dict_from_basis(), fp)
    return path


@pytest.fixture
def samb_path(tmp_path: Path) -> Path:
    """Create a temporary SAMB metadata file for type, rank, and irrep filtering."""
    path = tmp_path / "fixture_samb.py"
    write_samb(path)
    return path


@pytest.fixture
def fixture_ham() -> HamR:
    """Return a Hermitian one-cell Hamiltonian expanded in the complete fixture basis."""
    basis = pauli_basis()
    hrs = 1.25 * basis[0] - 0.5 * basis[1] + 0.3 * basis[2] + 0.2 * basis[3]
    return HamR(
        irvec=np.array([[0, 0, 0]], dtype=np.int64),
        ndegen=np.array([1], dtype=np.int64),
        hrs=hrs.reshape(1, 2, 2),
    )
