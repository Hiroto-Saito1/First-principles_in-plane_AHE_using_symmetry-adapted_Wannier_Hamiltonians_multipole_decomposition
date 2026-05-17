"""Magnetization rotation for selected multipole-decomposed Hamiltonian terms."""

from __future__ import annotations

import gzip
from itertools import product
from pathlib import Path
import re
from typing import Any

import numpy as np

from .single_multipole_reader import SingleMultipoleReader


def load_samb_dict(samb_path: Path | str) -> dict[str, Any]:
    """Load a MultiPie `*_samb.py` dictionary."""

    path = Path(samb_path)
    if path.is_file():
        with open(path, "rt") as fp:
            code = fp.read()
    elif path.with_suffix(path.suffix + ".gz").is_file():
        with gzip.open(path.with_suffix(path.suffix + ".gz"), "rt") as fp:
            code = fp.read()
    else:
        raise FileNotFoundError(path)

    namespace: dict[str, Any] = {}
    exec(code, namespace)
    candidates = {
        name: value
        for name, value in namespace.items()
        if not name.startswith("__") and isinstance(value, dict) and value
    }
    if len(candidates) != 1:
        raise ValueError(f"Expected exactly one SAMB dictionary in {path}.")
    return next(iter(candidates.values()))


def extract_z_names(samb_dict: dict[str, Any]) -> list[str]:
    """Extract Z names from a SAMB dictionary."""

    z_dict = samb_dict["data"]["Z"]
    names: list[str] = []
    for value in z_dict.values():
        if isinstance(value, tuple):
            names.append(str(value[0]))
        else:
            names.append(str(value))
    return names


def parse_z_name(z_name: str) -> dict[str, str | int]:
    """Parse strings such as `M(1,T1g,,0|1,-1)`."""

    match = re.match(r"^([A-Z])\((\d+),([^,)]*)", z_name)
    if not match:
        raise ValueError(f"Invalid Z name: {z_name!r}")
    return {
        "type": match.group(1),
        "rank": int(match.group(2)),
        "irrep": match.group(3),
    }


def su2_rotation(axis: np.ndarray, angle_degrees: float) -> np.ndarray:
    """Spin-1/2 rotation matrix for a normalized axis and angle in degrees."""

    axis = np.asarray(axis, dtype=np.float64)
    norm = np.linalg.norm(axis)
    if norm == 0:
        raise ValueError("Rotation axis must be non-zero.")
    x, y, z = axis / norm
    theta = np.deg2rad(angle_degrees)
    identity = np.eye(2, dtype=np.complex128)
    sigma = (
        x * np.array([[0, 1], [1, 0]], dtype=np.complex128)
        + y * np.array([[0, -1j], [1j, 0]], dtype=np.complex128)
        + z * np.array([[1, 0], [0, -1]], dtype=np.complex128)
    )
    return np.cos(theta / 2) * identity - 1j * np.sin(theta / 2) * sigma


class MagRotation:
    """Rotate selected decomposed Hamiltonian components in spin space."""

    def __init__(
        self,
        multi_path: Path | str,
        samb_path: Path | str,
        filters: list[dict[str, Any]] | None = None,
    ):
        self.reader = SingleMultipoleReader(multi_path)
        self.z_coefficients = self.reader.z_coefficients[:]
        self.irvec = self.reader.irvec
        self.ndegen = self.reader.ndegen
        self.nrpts = self.reader.nrpts
        self.num_multipole = self.reader.num_multipole
        self.num_wann = self.reader.num_wann
        if self.num_wann % 2:
            raise ValueError("Spin rotation requires an even number of Wannier functions.")

        self.z_names = extract_z_names(load_samb_dict(samb_path))
        if len(self.z_names) != self.num_multipole:
            raise ValueError("Number of Z names does not match HDF5 multipole count.")

        if filters is None:
            filters = [
                {
                    "types": None,
                    "ranks": None,
                    "irreps": None,
                    "axis1": [0.0, 1.0, 0.0],
                    "axis2": [0.0, 0.0, 1.0],
                    "theta": 0.0,
                    "phi": 0.0,
                    "coef_amp_para": 1.0,
                }
            ]

        self.filtered_indices_list: list[np.ndarray] = []
        self.hrs_filtered_list: list[np.ndarray] = []
        self.hrs_filtered_rotated_list: list[np.ndarray] = []
        selected: set[int] = set()

        for spec in filters:
            indices = self.filter_z_indices(
                types=spec.get("types"),
                ranks=spec.get("ranks"),
                irreps=spec.get("irreps"),
            )
            selected.update(int(i) for i in indices)
            self.filtered_indices_list.append(indices)
            hrs_filtered = self.divide_hrs(indices)
            self.hrs_filtered_list.append(hrs_filtered)
            self.hrs_filtered_rotated_list.append(
                self.rotate_mag(
                    hrs_filtered,
                    axis1=spec.get("axis1", [0.0, 1.0, 0.0]),
                    axis2=spec.get("axis2", [0.0, 0.0, 1.0]),
                    theta=spec.get("theta", 0.0),
                    phi=spec.get("phi", 0.0),
                    coef_amp_para=spec.get("coef_amp_para", 1.0),
                )
            )

        other_indices = np.array(sorted(set(range(self.num_multipole)) - selected))
        self.hrs_other = self.divide_hrs(other_indices)

    def close(self) -> None:
        self.reader.close()

    def filter_z_indices(
        self,
        *,
        types: list[str] | None = None,
        ranks: list[int] | None = None,
        irreps: list[str] | None = None,
    ) -> np.ndarray:
        """Return indices satisfying all provided filters."""

        indices: list[int] = []
        for idx, z_name in enumerate(self.z_names):
            parsed = parse_z_name(z_name)
            if types is not None and parsed["type"] not in types:
                continue
            if ranks is not None and parsed["rank"] not in ranks:
                continue
            if irreps is not None and parsed["irrep"] not in irreps:
                continue
            indices.append(idx)
        return np.array(indices, dtype=np.int64)

    def divide_hrs(self, indices: np.ndarray) -> np.ndarray:
        """Build the Hamiltonian contribution from selected multipole indices."""

        selected = set(int(i) for i in indices)
        hrs = np.zeros((self.nrpts, self.num_wann, self.num_wann), dtype=np.complex128)
        for im in selected:
            component = self.reader.get_multipole_matrix(im).todense()
            hrs += self.z_coefficients[im] * component
        return hrs

    def rotate_mag(
        self,
        hrs_filtered: np.ndarray,
        axis1: list[float] | np.ndarray = [0.0, 1.0, 0.0],
        axis2: list[float] | np.ndarray = [0.0, 0.0, 1.0],
        theta: float = 0.0,
        phi: float = 0.0,
        coef_amp_para: float = 1.0,
    ) -> np.ndarray:
        """Rotate a selected Hamiltonian contribution by two spin rotations."""

        spinor = coef_amp_para * hrs_filtered.reshape(
            self.nrpts, self.num_wann // 2, 2, self.num_wann // 2, 2
        )
        rotation1 = su2_rotation(np.asarray(axis1), theta)
        rotation2 = su2_rotation(np.asarray(axis2), phi)
        rotated = np.einsum(
            "ij,rljmk,kn->rlimn",
            rotation1,
            spinor,
            rotation1.conj().T,
            optimize=True,
        )
        rotated = np.einsum(
            "ij,rljmk,kn->rlimn",
            rotation2,
            rotated,
            rotation2.conj().T,
            optimize=True,
        )
        return rotated.reshape(self.nrpts, self.num_wann, self.num_wann)

    def rotated_hamiltonian(self) -> np.ndarray:
        """Return the full rotated Hamiltonian."""

        return sum(self.hrs_filtered_rotated_list) + self.hrs_other

    def write_rotated_hr(self, path: Path | str) -> None:
        """Write the rotated Hamiltonian in Wannier90 `hr.dat` format."""

        hrs = self.rotated_hamiltonian()
        with open(path, "w") as fp:
            fp.write("created by symwan_multipie.mag_rotation\n")
            fp.write(f"{self.num_wann}\n")
            fp.write(f"{self.nrpts}\n")
            for start in range(0, self.nrpts, 15):
                fp.write(" ".join(str(x) for x in self.ndegen[start : start + 15]) + "\n")
            for ir, (row, col) in product(range(self.nrpts), product(range(self.num_wann), repeat=2)):
                value = hrs[ir, row, col]
                fp.write(
                    f"{self.irvec[ir, 0]:5d}{self.irvec[ir, 1]:5d}{self.irvec[ir, 2]:5d}"
                    f"{row + 1:5d}{col + 1:5d}{value.real:20.12e}{value.imag:20.12e}\n"
                )
