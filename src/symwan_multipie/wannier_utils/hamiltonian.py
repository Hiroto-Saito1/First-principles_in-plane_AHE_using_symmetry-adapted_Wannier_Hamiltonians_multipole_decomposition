"""Minimal Wannier90 Hamiltonian reader."""

from __future__ import annotations

from dataclasses import dataclass
import gzip
from itertools import product
from pathlib import Path

import numpy as np


def _open_text_or_gzip(path: Path):
    if path.is_file():
        return open(path, "rt")
    gz_path = path.with_suffix(path.suffix + ".gz")
    if gz_path.is_file():
        return gzip.open(gz_path, "rt")
    raise FileNotFoundError(path)


@dataclass
class HamR:
    """Real-space Wannier Hamiltonian.

    Attributes:
        irvec: Wigner-Seitz grid vectors, shape `(nrpts, 3)`.
        ndegen: degeneracy factors, shape `(nrpts,)`.
        hrs: Hamiltonian matrices, shape `(nrpts, num_wann, num_wann)`.
        a: optional lattice vectors for `wannier_tb.dat` output.
        Amnrs: optional position matrices for `wannier_tb.dat` output.
    """

    irvec: np.ndarray
    ndegen: np.ndarray
    hrs: np.ndarray
    a: np.ndarray | None = None
    Amnrs: np.ndarray | None = None

    def __post_init__(self) -> None:
        self.irvec = np.asarray(self.irvec, dtype=np.int64)
        self.ndegen = np.asarray(self.ndegen, dtype=np.int64)
        self.hrs = np.asarray(self.hrs, dtype=np.complex128)
        self.nrpts = int(self.hrs.shape[0])
        self.num_wann = int(self.hrs.shape[1])
        self.ir0 = self._find_origin()
        if self.irvec.shape != (self.nrpts, 3):
            raise ValueError("irvec must have shape (nrpts, 3).")
        if self.ndegen.shape != (self.nrpts,):
            raise ValueError("ndegen must have shape (nrpts,).")
        if self.hrs.shape[2] != self.num_wann:
            raise ValueError("hrs must have shape (nrpts, num_wann, num_wann).")

    @classmethod
    def from_hr_dat(cls, path: Path | str, is_reorder: bool = False) -> "HamR":
        with _open_text_or_gzip(Path(path)) as fp:
            fp.readline()
            num_wann = int(fp.readline())
            nrpts = int(fp.readline())
            ndegen: list[int] = []
            while len(ndegen) < nrpts:
                ndegen.extend(int(x) for x in fp.readline().split())

            irvec = np.zeros((nrpts, 3), dtype=np.int64)
            hrs = np.zeros((nrpts, num_wann, num_wann), dtype=np.complex128)
            for ir, (m, n) in product(range(nrpts), product(range(num_wann), repeat=2)):
                parts = fp.readline().split()
                if len(parts) != 7:
                    raise ValueError(f"Malformed hr.dat line for R index {ir}.")
                rx, ry, rz, row, col, real, imag = parts
                if m == 0 and n == 0:
                    irvec[ir] = [int(rx), int(ry), int(rz)]
                row_i = int(row) - 1
                col_i = int(col) - 1
                if is_reorder:
                    row_i = row_i // 2 + (num_wann // 2) * (row_i % 2)
                    col_i = col_i // 2 + (num_wann // 2) * (col_i % 2)
                hrs[ir, row_i, col_i] = float(real) + 1j * float(imag)
        return cls(irvec=irvec, ndegen=np.array(ndegen[:nrpts]), hrs=hrs)

    @classmethod
    def from_tb_dat(cls, path: Path | str, is_reorder: bool = False) -> "HamR":
        with _open_text_or_gzip(Path(path)) as fp:
            fp.readline()
            a = np.array([[float(x) for x in fp.readline().split()] for _ in range(3)])
            num_wann = int(fp.readline())
            nrpts = int(fp.readline())
            ndegen: list[int] = []
            while len(ndegen) < nrpts:
                ndegen.extend(int(x) for x in fp.readline().split())

            irvec = np.zeros((nrpts, 3), dtype=np.int64)
            hrs = np.zeros((nrpts, num_wann, num_wann), dtype=np.complex128)
            for ir in range(nrpts):
                fp.readline()
                irvec[ir] = [int(x) for x in fp.readline().split()]
                for _ in range(num_wann * num_wann):
                    row, col, real, imag = fp.readline().split()
                    row_i = int(row) - 1
                    col_i = int(col) - 1
                    if is_reorder:
                        row_i = row_i // 2 + (num_wann // 2) * (row_i % 2)
                        col_i = col_i // 2 + (num_wann // 2) * (col_i % 2)
                    hrs[ir, row_i, col_i] = float(real) + 1j * float(imag)

            Amnrs = np.zeros((nrpts, num_wann, num_wann, 3), dtype=np.complex128)
            for ir in range(nrpts):
                fp.readline()
                fp.readline()
                for _ in range(num_wann * num_wann):
                    row, col, axr, axi, ayr, ayi, azr, azi = fp.readline().split()
                    row_i = int(row) - 1
                    col_i = int(col) - 1
                    Amnrs[ir, row_i, col_i] = [
                        float(axr) + 1j * float(axi),
                        float(ayr) + 1j * float(ayi),
                        float(azr) + 1j * float(azi),
                    ]
        return cls(irvec=irvec, ndegen=np.array(ndegen[:nrpts]), hrs=hrs, a=a, Amnrs=Amnrs)

    def _find_origin(self) -> int:
        matches = np.where(np.all(self.irvec == 0, axis=1))[0]
        return int(matches[0]) if len(matches) else -1

    def export_hr_dat(self, path: Path | str) -> None:
        with open(path, "w") as fp:
            fp.write("created by symwan_multipie\n")
            fp.write(f"{self.num_wann}\n")
            fp.write(f"{self.nrpts}\n")
            for start in range(0, self.nrpts, 15):
                fp.write(" ".join(str(x) for x in self.ndegen[start : start + 15]) + "\n")
            for ir in range(self.nrpts):
                for row, col in product(range(self.num_wann), repeat=2):
                    value = self.hrs[ir, row, col]
                    fp.write(
                        f"{self.irvec[ir, 0]:5d}{self.irvec[ir, 1]:5d}"
                        f"{self.irvec[ir, 2]:5d}{row + 1:5d}{col + 1:5d}"
                        f"{value.real:20.12e}{value.imag:20.12e}\n"
                    )

