"""Band interpolation utilities for the expanded Wannier helper package."""

from __future__ import annotations

from itertools import chain
from typing import TYPE_CHECKING, Iterable, List

import numpy as np

from .logger import get_logger
from .hamiltonian import HamR

if TYPE_CHECKING:
    from .wannier_system import WannierSystem


logger = get_logger(__name__)


def hamiltonian_at_k(
    ham_r: HamR,
    k: np.ndarray,
    hrs: np.ndarray | None = None,
) -> np.ndarray:
    """Return `H(k)` for a fractional-coordinate k point."""

    matrices = ham_r.hrs if hrs is None else hrs
    phase = np.exp(2j * np.pi * np.einsum("a,ra->r", k, ham_r.irvec)) / ham_r.ndegen
    return np.einsum("r,rab->ab", phase, matrices)


def eigenvalues_on_kmesh(
    ham_r: HamR,
    kpoints: np.ndarray,
    hrs: np.ndarray | None = None,
) -> np.ndarray:
    """Return eigenvalues for all k points on a mesh."""

    kpoints = np.asarray(kpoints, dtype=np.float64)
    values = np.empty((len(kpoints), ham_r.num_wann), dtype=np.float64)
    for ik, k in enumerate(kpoints):
        values[ik] = np.linalg.eigvalsh(hamiltonian_at_k(ham_r, k, hrs=hrs))
    return values


class WanBand:
    """Compatibility wrapper kept for lightweight validation workloads."""

    def __init__(
        self,
        ham_r: HamR,
        kpath: np.ndarray,
        hrs: np.ndarray | None = None,
    ):
        self.num_wann = ham_r.num_wann
        self.kp_list_all = np.asarray(kpath, dtype=np.float64)
        self.ek_all = eigenvalues_on_kmesh(ham_r, self.kp_list_all, hrs=hrs)


def _plot_dependencies():
    import matplotlib as mpl

    mpl.use("Agg", force=True)
    from matplotlib import pyplot as plt

    return mpl, plt


def _seekpath_dependencies():
    from seekpath import get_explicit_k_path
    from pymatgen.core.periodic_table import Element

    return get_explicit_k_path, Element


def _pymatgen_band_dependencies():
    from pymatgen.electronic_structure.core import Magmom
    from pymatgen.symmetry.bandstructure import HighSymmKpath

    return Magmom, HighSymmKpath


def main() -> None:
    from pathlib import Path
    from time import perf_counter

    from .wannier_system import WannierSystem

    base_dir = Path(__file__).parents[2]
    ws = WannierSystem(
        hr_dat=base_dir / "tests" / "Fe_hr.dat",
        nnkp_file=base_dir / "tests" / "Fe.nnkp",
        win_file=base_dir / "tests" / "Fe.win",
    )

    start_time = perf_counter()
    bs = BandStructure(ws, is_projection=True)
    bs.plot_bands_seekpath()
    end_time = perf_counter()
    logger.info("elapsed_time: %s [sec]", end_time - start_time)


class BandStructure:
    """Plot or inspect band structures for a ``WannierSystem``."""

    def __init__(
        self,
        ws: "WannierSystem",
        is_projection: bool = False,
        file_prefix: str = "band",
    ):
        self.ws = ws
        self.is_projection = is_projection
        self.file_prefix = file_prefix

    def plot_bands(
        self,
        kpts: np.ndarray,
        kmeshes: Iterable[int],
        klabels: Iterable[str] = (),
    ) -> None:
        kpts_all = [kpts[0]]
        kpts_lin = [0.0]
        tick_locs = [0.0]
        for i in range(len(kpts) - 1):
            kpts_all += [
                (kpts[i + 1] - kpts[i]) * float(j + 1) / kmeshes[i] + kpts[i]
                for j in range(kmeshes[i])
            ]
            d = np.linalg.norm(np.dot(kpts[i + 1] - kpts[i], self.ws.b), ord=2)
            kpts_lin += [
                d * float(j + 1) / kmeshes[i] + kpts_lin[-1] for j in range(kmeshes[i])
            ]
            tick_locs.append(tick_locs[-1] + d)

        self._plot_bands(np.array(kpts_all), np.array(kpts_lin), tick_locs, klabels)

    def _plot_bands(
        self,
        kpoints_frac: np.ndarray,
        kpoints_lin: np.ndarray,
        tick_locs: Iterable[float],
        tick_labels: Iterable[str],
    ) -> None:
        mpl, plt = _plot_dependencies()
        ham_ks = [self.ws.calc_ham_k(kf, diagonalize=True) for kf in kpoints_frac]
        bands = np.array([ham_k.ek for ham_k in ham_ks])

        mpl.rcParams["text.usetex"] = True
        mpl.rcParams["text.latex.preamble"] = "\\usepackage{amssymb} \\usepackage{amsmath}"
        ax = plt.subplot()
        ax.plot(kpoints_lin, bands, ls="-", lw=1, c="k")
        y_min = bands.min() - 0.025 * (bands.max() - bands.min())
        y_max = bands.max() + 0.025 * (bands.max() - bands.min())
        ax.set_ylim([y_min, y_max])
        ax.set_xticks(list(tick_locs))
        ax.set_xticklabels(list(tick_labels))
        ax.set_ylabel("Energy [eV]")
        for loc, label in zip(tick_locs, tick_labels):
            lw = 1 if "/" in label else 0.5
            ax.axvline(loc, color="k", ls="-", lw=lw)
        plt.savefig(self.file_prefix + ".pdf", bbox_inches="tight")
        plt.close()

    def plot_bands_seekpath(self) -> None:
        get_explicit_k_path, Element = _seekpath_dependencies()

        st = self.ws.win.structure
        cell = st.lattice.matrix
        positions = st.frac_coords
        numbers = [Element(s).Z for s in st.species]
        kpath = get_explicit_k_path((cell, positions, numbers))

        new_b = kpath["reciprocal_primitive_lattice"]
        m = np.matmul(new_b, cell.T) / (2 * np.pi)
        kpoints_frac = [
            np.matmul(k, m) for k in kpath["explicit_kpoints_rel"]
        ]
        kpoints_lin = kpath["explicit_kpoints_linearcoord"]

        kpoints_labels = kpath["explicit_kpoints_labels"]
        tick_locs: list[float] = []
        tick_labels: list[str] = []
        for i, label in enumerate(kpoints_labels):
            if not label:
                continue
            label = label.replace("GAMMA", "$\\Gamma$")
            label = label.replace("SIGMA", "$\\Sigma$")
            if "_" in label:
                label = label.replace("_", "$_") + "$"

            if i and kpoints_labels[i - 1]:
                tick_labels[-1] += "/" + label
            else:
                tick_locs.append(kpoints_lin[i])
                tick_labels.append(label)

        self._plot_bands(kpoints_frac, kpoints_lin, tick_locs, tick_labels)

    def plot_bands_pymatgen(self, line_density: int = 50) -> None:
        Magmom, HighSymmKpath = _pymatgen_band_dependencies()

        st = self.ws.win.structure
        has_magmoms = "magmom" in st.site_properties.keys()
        if has_magmoms:
            magmoms = st.site_properties["magmom"]
            if Magmom.have_consistent_saxis(magmoms):
                magmom_saxis = magmoms[0].saxis
            else:
                magmoms, saxis = Magmom.get_consistent_set_and_saxis(magmoms)
                st.site_properties["magmom"] = magmoms
                magmom_saxis = saxis
        else:
            magmom_saxis = None
        hsk = HighSymmKpath(st, has_magmoms=has_magmoms, magmom_axis=magmom_saxis)
        kpoints_cart, klabels = hsk.get_kpoints(line_density=line_density)
        kpoints_lin = self.get_kpoints_lin(kpoints_cart, klabels)
        kpoints_frac = [
            st.lattice.reciprocal_lattice.get_fractional_coords(k) for k in kpoints_cart
        ]

        klabels_nolap, kpoints_lin_nolap, kpoints_frac_nolap = [], [], []
        for i, (label, kpl, kpf) in enumerate(zip(klabels, kpoints_lin, kpoints_frac)):
            if i and label and label == klabels[i - 1]:
                continue
            klabels_nolap.append(label)
            kpoints_lin_nolap.append(kpl)
            kpoints_frac_nolap.append(kpf)

        tick_locs: list[float] = []
        tick_labels: list[str] = []
        for i, label in enumerate(klabels_nolap):
            if not label:
                continue
            label = label.replace("\\Gamma", "$\\Gamma$")
            label = label.replace("\\Sigma", "$\\Sigma$")

            if i and klabels_nolap[i - 1]:
                tick_labels[-1] += "/" + label
            else:
                tick_locs.append(kpoints_lin[i])
                tick_labels.append(label)

        self._plot_bands(kpoints_frac_nolap, kpoints_lin_nolap, tick_locs, tick_labels)

    @staticmethod
    def get_kpoints_lin(kpoints_cart: np.ndarray, klabels: Iterable[str]) -> List[float]:
        kpoints_cart_sep: list[list[np.ndarray]] = []
        kpoints_tmp: list[np.ndarray] = []
        for k, label in zip(kpoints_cart, klabels):
            if not kpoints_tmp and label:
                kpoints_tmp = [k]
                continue
            kpoints_tmp.append(k)
            if kpoints_tmp and label:
                kpoints_cart_sep.append(kpoints_tmp)
                kpoints_tmp = []
        norms_sep = []
        for i, ks in enumerate(kpoints_cart_sep):
            ns = [np.linalg.norm(k - ks[0], ord=2) for k in ks]
            if i:
                ns = [n + norms_sep[-1][-1] for n in ns]
            norms_sep.append(ns)
        return list(chain.from_iterable(norms_sep))


if __name__ == "__main__":
    main()
