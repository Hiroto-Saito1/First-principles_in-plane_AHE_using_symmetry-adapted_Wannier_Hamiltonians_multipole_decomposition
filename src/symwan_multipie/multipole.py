"""Read MultiPie multipole matrices and write a compact HDF5 representation."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import gzip
import pickle
from pathlib import Path
from typing import Any, Iterable

import h5py
import numpy as np


@dataclass(frozen=True)
class SparseCOO:
    """Small COO container used to avoid a runtime dependency on pydata/sparse."""

    coords: np.ndarray
    data: np.ndarray
    shape: tuple[int, ...]

    @property
    def nnz(self) -> int:
        return int(self.data.size)

    def todense(self) -> np.ndarray:
        dense = np.zeros(self.shape, dtype=self.data.dtype)
        if self.nnz:
            dense[tuple(self.coords)] = self.data
        return dense


def _open_text_or_gzip(path: Path):
    if path.is_file():
        return open(path, "rt")
    gz_path = path.with_suffix(path.suffix + ".gz")
    if gz_path.is_file():
        return gzip.open(gz_path, "rt")
    raise FileNotFoundError(path)


def _open_binary_or_gzip(path: Path):
    if path.is_file():
        return open(path, "rb")
    gz_path = path.with_suffix(path.suffix + ".gz")
    if gz_path.is_file():
        return gzip.open(gz_path, "rb")
    raise FileNotFoundError(path)


def _load_python_dict(path: Path) -> dict[str, Any]:
    with _open_text_or_gzip(path) as fp:
        code = fp.read()
    namespace: dict[str, Any] = {}
    exec(code, namespace)
    candidates = {
        name: value
        for name, value in namespace.items()
        if not name.startswith("__") and isinstance(value, dict) and value
    }
    if len(candidates) != 1:
        raise ValueError(
            f"Expected exactly one non-empty dictionary in {path}, "
            f"found {list(candidates)}."
        )
    return next(iter(candidates.values()))


def load_matrix_dict(path: Path | str) -> dict[str, Any]:
    """Load a MultiPie matrix dictionary from `.pkl`, `.pkl.gz`, `.py`, or `.py.gz`."""

    matrix_path = Path(path)
    if ".pkl" in matrix_path.name:
        with _open_binary_or_gzip(matrix_path) as fp:
            value = pickle.load(fp)
    else:
        value = _load_python_dict(matrix_path)
    if not isinstance(value, dict) or "matrix" not in value:
        raise ValueError(f"{matrix_path} does not contain a valid matrix dictionary.")
    return value


def value_to_complex(value: Any) -> np.complex128:
    """Convert numeric or symbolic MultiPie matrix entries to complex values."""

    if isinstance(value, (int, float, complex, np.number)):
        return np.complex128(value)
    text = str(value).replace("I", "j")
    try:
        return np.complex128(complex(text))
    except ValueError:
        pass
    try:
        from sympy import sympify

        return np.complex128(sympify(value))
    except Exception as exc:
        raise ValueError(f"Failed to convert {value!r} to a complex value.") from exc


class Multipole:
    """Convert a MultiPie multipole matrix dictionary to a sparse COO array."""

    def __init__(self, matrix_path: Path | str):
        self.matrix_path = Path(matrix_path)
        self.matrix_dict = load_matrix_dict(self.matrix_path)
        self.names, self.multipole = self._read_matrix(self.matrix_dict)

    @property
    def irvec(self) -> np.ndarray:
        return self._irvec

    @property
    def nrpts(self) -> int:
        return int(len(self._irvec))

    @property
    def num_wann(self) -> int:
        return int(self.multipole.shape[2])

    @property
    def num_multipole(self) -> int:
        return int(self.multipole.shape[0])

    def _read_matrix(self, matrix_dict: dict[str, Any]) -> tuple[list[str], SparseCOO]:
        matrix_entries = matrix_dict["matrix"]
        if not isinstance(matrix_entries, dict) or not matrix_entries:
            raise ValueError("matrix_dict['matrix'] must be a non-empty dictionary.")

        unique_irvec: set[tuple[int, int, int]] = set()
        max_wann = -1
        for elements in matrix_entries.values():
            for key in elements:
                i, j, k, row, col = key
                unique_irvec.add((int(i), int(j), int(k)))
                max_wann = max(max_wann, int(row), int(col))

        self._irvec = np.array(sorted(unique_irvec), dtype=np.int64)
        irvec_index = {tuple(vec): idx for idx, vec in enumerate(self._irvec)}
        num_wann = max_wann + 1
        num_multipole = len(matrix_entries)

        coords: list[list[int]] = [[], [], [], []]
        data: list[np.complex128] = []
        names: list[str] = []
        for im, (name, elements) in enumerate(matrix_entries.items()):
            names.append(str(name))
            for key, value in elements.items():
                i, j, k, row, col = key
                complex_value = value_to_complex(value)
                if complex_value == 0:
                    continue
                coords[0].append(im)
                coords[1].append(irvec_index[(int(i), int(j), int(k))])
                coords[2].append(int(row))
                coords[3].append(int(col))
                data.append(complex_value)

        sparse = SparseCOO(
            coords=np.array(coords, dtype=np.int64),
            data=np.array(data, dtype=np.complex128),
            shape=(num_multipole, self.nrpts, num_wann, num_wann),
        )
        return names, sparse

    def get_component(self, index: int) -> SparseCOO:
        """Return one multipole component as `(nrpts, num_wann, num_wann)`."""

        mask = self.multipole.coords[0] == index
        coords = self.multipole.coords[1:, mask]
        data = self.multipole.data[mask]
        return SparseCOO(coords, data, self.multipole.shape[1:])

    def write_hdf5(self, hdf5_path: Path | str) -> None:
        """Write the multipole matrix to HDF5.

        HDF5 schema:
        - `/multipole_matrix/coords`: COO coordinates `(im, ir, row, col)`.
        - `/multipole_matrix/data`: non-zero matrix values.
        - `/multipole_matrix/shape`: full sparse array shape.
        - `/multipole_matrix/irvec`: lattice-vector list for the `ir` axis.
        - `/multipole_matrix/multipole_index`: start offsets for each `im`.
        - `/multipole_matrix/names`: original MultiPie dictionary keys.
        """

        coords = self.multipole.coords
        data = self.multipole.data
        shape = np.array(self.multipole.shape, dtype=np.int64)
        pointers = self._component_pointers(coords[0], self.num_multipole)

        with h5py.File(hdf5_path, "w") as h5:
            grp = h5.create_group("multipole_matrix")
            grp.create_dataset("coords", data=coords)
            grp.create_dataset("data", data=data)
            grp.create_dataset("shape", data=shape)
            grp.create_dataset("irvec", data=self.irvec)
            grp.create_dataset("multipole_index", data=pointers)
            string_dtype = h5py.string_dtype(encoding="utf-8")
            grp.create_dataset("names", data=np.array(self.names, dtype=object), dtype=string_dtype)

    @staticmethod
    def _component_pointers(multipole_indices: Iterable[int], num_multipole: int) -> np.ndarray:
        indices = np.asarray(list(multipole_indices), dtype=np.int64)
        pointers = np.empty(num_multipole + 1, dtype=np.int64)
        for im in range(num_multipole):
            pointers[im] = np.searchsorted(indices, im, side="left")
        pointers[num_multipole] = len(indices)
        return pointers


def _default_output_path(matrix_path: Path) -> Path:
    name = matrix_path.name
    for suffix in (".pkl.gz", ".py.gz", ".pkl", ".py"):
        if name.endswith(suffix):
            return matrix_path.with_name(name[: -len(suffix)] + ".hdf5")
    return matrix_path.with_suffix(".hdf5")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "matrix_path",
        type=Path,
        help="Path to a MultiPie matrix dictionary such as Fe_matrix.pkl or Fe_all_35_matrix.py.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional output HDF5 path. Defaults to <matrix_path>.hdf5.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output = args.output or _default_output_path(args.matrix_path)
    multipole = Multipole(args.matrix_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    multipole.write_hdf5(output)
    print(
        f"Wrote {output} "
        f"(num_multipole={multipole.num_multipole}, nrpts={multipole.nrpts}, num_wann={multipole.num_wann})"
    )


if __name__ == "__main__":
    main()
