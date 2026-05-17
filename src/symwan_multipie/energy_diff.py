"""Reconstruction-error metrics for multipole-decomposed Hamiltonians."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from .mag_rotation import MagRotation
from .wannier_utils.band import eigenvalues_on_kmesh
from .wannier_utils.hamiltonian import HamR


def uniform_kmesh(mesh: tuple[int, int, int] | list[int]) -> np.ndarray:
    """Return fractional k points on a uniform mesh."""

    points = []
    for x in np.linspace(0.0, 1.0, mesh[0], endpoint=False):
        for y in np.linspace(0.0, 1.0, mesh[1], endpoint=False):
            for z in np.linspace(0.0, 1.0, mesh[2], endpoint=False):
                points.append([x, y, z])
    return np.array(points, dtype=np.float64)


class EnergyDiff:
    """Compare an original Hamiltonian with selected multipole reconstruction."""

    def __init__(
        self,
        ham_r: HamR,
        multi_path: Path | str,
        samb_path: Path | str,
        types: list[str] | None = None,
        ranks: list[int] | None = None,
        irreps: list[str] | None = None,
        theta: float = 0.0,
        phi: float = 0.0,
        coef_amp_para: float = 1.0,
        kmesh: tuple[int, int, int] | list[int] = (2, 2, 2),
    ):
        filters = [
            {
                "types": types,
                "ranks": ranks,
                "irreps": irreps,
                "axis1": [0.0, 1.0, 0.0],
                "axis2": [0.0, 0.0, 1.0],
                "theta": theta,
                "phi": phi,
                "coef_amp_para": coef_amp_para,
            }
        ]
        rotation = MagRotation(multi_path=multi_path, samb_path=samb_path, filters=filters)
        try:
            hrs_expanded = rotation.rotated_hamiltonian()
            if not np.array_equal(ham_r.irvec, rotation.irvec):
                raise ValueError("ham_r.irvec and multipole irvec do not match.")
            if not np.array_equal(ham_r.ndegen, rotation.ndegen):
                raise ValueError("ham_r.ndegen and multipole ndegen do not match.")
            self.hrs_irvec_range = self._irvec_range(ham_r.irvec)
            self.hrs_expand_irvec_range = self._irvec_range(rotation.irvec)
            self.energy_diff = self.calc_energy_diff(ham_r, hrs_expanded, kmesh)
            self.max_diff, self.max_irvec = self.calc_hamiltonian_diff(ham_r, hrs_expanded)
        finally:
            rotation.close()

    @staticmethod
    def _irvec_range(irvec: np.ndarray) -> np.ndarray:
        return np.array([(np.min(irvec[:, i]), np.max(irvec[:, i])) for i in range(3)])

    @staticmethod
    def calc_energy_diff(
        ham_r: HamR,
        hrs_expanded: np.ndarray,
        kmesh: tuple[int, int, int] | list[int],
    ) -> float:
        kpoints = uniform_kmesh(kmesh)
        reference = eigenvalues_on_kmesh(ham_r, kpoints, hrs=ham_r.hrs)
        reconstructed = eigenvalues_on_kmesh(ham_r, kpoints, hrs=hrs_expanded)
        return float(np.mean(np.abs(reference - reconstructed)))

    @staticmethod
    def calc_hamiltonian_diff(ham_r: HamR, hrs_expanded: np.ndarray) -> tuple[float, np.ndarray]:
        difference = np.abs(ham_r.hrs - hrs_expanded)
        max_index = np.unravel_index(np.argmax(difference), difference.shape)
        return float(difference[max_index]), ham_r.irvec[max_index[0]]

