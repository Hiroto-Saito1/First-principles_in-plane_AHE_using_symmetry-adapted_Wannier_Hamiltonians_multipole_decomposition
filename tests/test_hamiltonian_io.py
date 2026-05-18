"""Tests for minimal Hamiltonian file IO helpers."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from symwan_multipie.wannier_utils.hamiltonian import HamR


def test_tb_dat_roundtrip_preserves_hamiltonian_and_position_matrices(tmp_path: Path) -> None:
    """Round-trip a tiny tb.dat fixture through the public reader and writer."""
    ham = HamR(
        irvec=np.array([[0, 0, 0]], dtype=np.int64),
        ndegen=np.array([1], dtype=np.int64),
        hrs=np.array([[[1.0 + 0.0j, 0.2 - 0.1j], [0.2 + 0.1j, -0.5 + 0.0j]]]),
        a=np.eye(3, dtype=np.float64),
        Amnrs=np.array(
            [
                [
                    [[0.0 + 0.0j, 0.0 + 0.0j, 0.1 + 0.0j], [0.2 + 0.0j, 0.0 + 0.0j, 0.0 + 0.0j]],
                    [[0.2 + 0.0j, 0.0 + 0.0j, 0.0 + 0.0j], [0.0 + 0.0j, 0.3 + 0.0j, 0.0 + 0.0j]],
                ]
            ],
            dtype=np.complex128,
        ),
    )

    path = tmp_path / "fixture_tb.dat"
    ham.export_tb_dat(path)
    restored = HamR.from_tb_dat(path)

    assert np.allclose(restored.a, ham.a)
    assert np.allclose(restored.hrs, ham.hrs)
    assert np.allclose(restored.Amnrs, ham.Amnrs)
