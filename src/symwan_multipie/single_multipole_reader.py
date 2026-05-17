"""Partial reader for multipole-decomposition HDF5 files."""

from __future__ import annotations

from pathlib import Path

import h5py
import numpy as np

from .multipole import SparseCOO


class SingleMultipoleReader:
    """Read selected multipole components from `MultipoleDecomposition` output."""

    def __init__(self, hdf5_path: Path | str):
        self.hdf5_path = Path(hdf5_path)
        self._open()

    def _open(self) -> None:
        self.h5 = h5py.File(self.hdf5_path, "r")
        self.irvec = self.h5["irvec"][:]
        self.ndegen = self.h5["ndegen"][:]
        self.z_coefficients = self.h5["z_coefficients"]
        self.grp = self.h5["multipole_padded"]
        self.shape = tuple(int(x) for x in self.grp["shape"][:])
        self.coords = self.grp["coords"][:]
        self.data = self.grp["data"][:]
        self.im_order = self.grp["im_order"][:]

        self._im_indices: dict[int, np.ndarray] = {}
        for im in np.unique(self.im_order):
            self._im_indices[int(im)] = np.where(self.im_order == im)[0]

    def close(self) -> None:
        self.h5.close()

    def __enter__(self) -> "SingleMultipoleReader":
        return self

    def __exit__(self, *_exc_info) -> None:
        self.close()

    @property
    def num_multipole(self) -> int:
        return int(self.shape[0])

    @property
    def nrpts(self) -> int:
        return int(self.shape[1])

    @property
    def num_wann(self) -> int:
        return int(self.shape[2])

    def get_z_coefficient(self, im: int) -> np.complex128:
        return np.complex128(self.z_coefficients[im])

    def get_multipole_matrix(self, im: int) -> SparseCOO:
        indices = self._im_indices.get(int(im))
        if indices is None or len(indices) == 0:
            coords = np.empty((3, 0), dtype=np.int64)
            data = np.empty(0, dtype=np.complex128)
        else:
            coords = self.coords[1:, indices]
            data = self.data[indices]
        return SparseCOO(coords=coords, data=data, shape=self.shape[1:])

