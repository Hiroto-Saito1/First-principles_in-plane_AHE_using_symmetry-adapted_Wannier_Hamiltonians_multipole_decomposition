"""Band interpolation utilities for small test and validation workloads."""

from __future__ import annotations

import numpy as np

from .hamiltonian import HamR


def hamiltonian_at_k(ham_r: HamR, k: np.ndarray, hrs: np.ndarray | None = None) -> np.ndarray:
    """Return `H(k)` for fractional-coordinate k."""

    matrices = ham_r.hrs if hrs is None else hrs
    phase = np.exp(2j * np.pi * np.einsum("a,ra->r", k, ham_r.irvec)) / ham_r.ndegen
    return np.einsum("r,rab->ab", phase, matrices)


def eigenvalues_on_kmesh(ham_r: HamR, kpoints: np.ndarray, hrs: np.ndarray | None = None) -> np.ndarray:
    """Return eigenvalues for all k points."""

    kpoints = np.asarray(kpoints, dtype=np.float64)
    values = np.empty((len(kpoints), ham_r.num_wann), dtype=np.float64)
    for ik, k in enumerate(kpoints):
        values[ik] = np.linalg.eigvalsh(hamiltonian_at_k(ham_r, k, hrs=hrs))
    return values


class WanBand:
    """Compatibility wrapper for the old `WanBand` interface."""

    def __init__(self, ham_r: HamR, kpath: np.ndarray, hrs: np.ndarray | None = None):
        self.num_wann = ham_r.num_wann
        self.kp_list_all = np.asarray(kpath, dtype=np.float64)
        self.ek_all = eigenvalues_on_kmesh(ham_r, self.kp_list_all, hrs=hrs)

