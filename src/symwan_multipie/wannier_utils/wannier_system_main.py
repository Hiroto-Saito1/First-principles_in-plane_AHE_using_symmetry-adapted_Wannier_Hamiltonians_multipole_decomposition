#!/usr/bin/env python

import numpy as np
import itertools
from .hamiltonian import HamR, HamK
from .nnkp import Nnkp
from .win import Win


class WannierSystem(object):
    """
    All information from Wannier90.

    Attributes
    ----------
    use_ws_dist:
    one_shot: whether the process was one-shot calculation.
    ham_r: Wannier-based tight-binding Hamiltonian in real space.
    nnkp: Nnkp instance.
    win: Win instance.
    num_wann: the number of wannier orbitals.
    a: real-space lattice vectors.
    b: reciprocal-space lattice vectors.
    natom: the number of atoms in a unit cell.
    volume: volume of a unit cell.
    """

    def __init__(
        self,
        file_tb="",
        file_hr="",
        file_nnkp="",
        file_win="",
        one_shot=False,
        reorder=False,
        use_ws_dist=False,
    ):
        """
        Parameters
        ----------
        file_tb: Path of prefix_tb.dat.
        file_hr: Path of prefix_hr.dat.
        file_nnkp: Path of prefix.nnkp.
        file_win: Path of prefix.win.
        reorder (bool): whether to reorder Hamiltonian (for VASP, Wannier90 ver.1, etc.).
        use_ws_dist (bool): whether to calculate distance using WS cell. See also Wannier90 manual
        """
        self.one_shot = one_shot
        self.use_ws_dist = use_ws_dist
        if file_tb or file_hr:
            self.ham_r = HamR(file_tb=file_tb, file_hr=file_hr, reorder=reorder)

        if file_nnkp:
            self.nnkp = Nnkp(file_nnkp=file_nnkp)

        if file_win:
            self.win = Win(file_win=file_win)

        if self.use_ws_dist:
            self._convert_hr()

    def calc_hk(self, k, rc=None, diagonalize=True):
        return HamK(self.ham_r, k, rc=rc, diagonalize=diagonalize)

    def set_sym(self, magmoms=None):
        """
        set symmetry operations of system.
        ==> self.s_ops  : symmetry operations of space group
            self.ms_ops : symmetry operations of magnetic space group
        structure is read from win file
        magnetic moment by magmoms

        Parameters
        ----------
        magmoms : None, "x", "y", "z", or [nsites, 3] numpy array
        """
        from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
        from .mag_sym import get_magnetic_space_group

        if not hasattr(self, "win"):
            raise ValueError("win file is not specified.")

        s = self.win.structure()
        sp = SpacegroupAnalyzer(s)
        self.s_ops = sp.get_space_group_operations()
        print("# symmetry")
        if magmoms == None:
            magmoms = [[0, 0, 0]] * len(s.sites)
            print("# with no magnetic moment")
        else:
            if magmoms == "x" or magmoms == "y" or magmoms == "z":
                m = {"x": [1, 0, 0], "y": [0, 1, 0], "z": [0, 0, 1]}
                m_crys = self.b @ np.array(m[magmoms])
                print(
                    "# with magnetic moment in crystal coords = {0[0]:12.4f} {0[1]:12.4f} {0[2]:12.4f}".format(
                        m_crys
                    )
                )
                magmoms = [m_crys] * len(s.sites)
            else:
                print("# with magnetic moment = ", magmoms)
        self.ms_ops = get_magnetic_space_group(self.s_ops, s.sites, magmoms)
        print("# num of symmetry: {}".format(len(self.ms_ops)))
        # for op in self.ms_ops:
        #    print(op.rotation_matrix)
        #    print(op.time_reversal)

    def merge(self, ws_add, orig_weight, add_weight):
        """
        Update Hamiltonian by merging original with the given other Hamiltonian.

        Parameters
        ----------
        ws_add: WannierSystem for the other Hamiltonian.
        orig_weight: superposition weight of original Hamiltonian.
        add_weight: superposition weight of the other Hamiltonian.
        """
        assert self.num_wann == ws_add.num_wann, "Different numbers of Wanier orbitals"
        self.ham_r.ham_r *= orig_weight
        self.ham_r.ham_r += ws_add.ham_r.ham_r * add_weight

    @property
    def num_wann(self):
        if hasattr(self, "ham_r"):
            return self.ham_r.num_wann
        elif hasattr(self, "win"):
            return self.win.num_wann
        elif hasattr(self, "nnkp"):
            return self.nnkp.num_wann
        else:
            raise ValueError("num_wann is not defined!")

    @property
    def a(self):
        if hasattr(self, "nnkp"):
            return self.nnkp.a
        elif hasattr(self, "ham_r") and hasattr(self.ham_r.a):
            return self.ham_r.a
        else:
            raise ValueError("a is not defined!")

    @property
    def b(self):
        if hasattr(self, "nnkp"):
            return self.nnkp.b
        elif hasattr(self, "ham_r") and hasattr(self.ham_r.b):
            return self.ham_r.b
        else:
            raise ValueError("b is not defined!")

    @property
    def natom(self):
        if hasattr(self, "nnkp"):
            return self.nnkp.natom
        else:
            raise ValueError("natom is not defined!")

    @property
    def volume(self):
        return np.abs(np.dot(self.a[0, :], np.cross(self.a[1, :], self.a[2, :])))

    def _calc_irvec(self, rd):
        """
        rd = r[1] - r[0]
        """
        real_metric = np.einsum("ij,lj->il", self.nnkp.a, self.nnkp.a)
        mp_grid = self.win.mp_grid
        ilist = np.array(list(itertools.product(range(-2, 3), repeat=3)))
        mp_list = np.array(
            list(
                itertools.product(
                    range(-mp_grid[0], mp_grid[0] + 1),
                    range(-mp_grid[1], mp_grid[1] + 1),
                    range(-mp_grid[2], mp_grid[2] + 1),
                )
            )
        )
        rd = np.array(rd)
        # all the possible vectors for transfer. size [npos,3]
        pos = rd[None, :] + mp_list
        # distance from Wannier on superlattice (LxMxN). size R_list[npos,LMN,3], dist[npos,LMN]
        R_list = (
            pos[:, None, :]
            - np.einsum("na,a->na", ilist, mp_grid, optimize=True)[None, :, :]
        )
        dist = np.einsum("ija,ab,ijb->ij", R_list, real_metric, R_list, optimize=True)
        # dist[:,62] = dist[:, i1=i2=i3=0]
        dist0 = dist[:, 62]
        dist_min = np.min(dist, axis=1)
        ind = np.where(dist0 - dist_min < 1e-5)
        ndeg = np.sum(np.abs(dist - dist0[:, None]) < 1e-5, axis=1)
        irvec = mp_list[ind]
        ndegen = ndeg[ind]

        assert (
            np.sum(1 / np.array(ndegen)) - np.product(mp_grid) < 1e-8
        ), "error in finding Wigner-Seitz points"
        return np.array(irvec), np.array(ndegen)

    def _convert_hr(self):
        """
        Convert HamR using WS distance
        """
        mp_grid = self.win.mp_grid
        ham_r0 = np.zeros(
            [mp_grid[0], mp_grid[1], mp_grid[2], self.num_wann, self.num_wann],
            dtype=np.complex128,
        )
        Amn_r0 = np.zeros(
            [mp_grid[0], mp_grid[1], mp_grid[2], self.num_wann, self.num_wann, 3],
            dtype=np.complex128,
        )
        for ir in range(self.ham_r.nrpts):
            r = np.mod(self.ham_r.irvec[ir] + mp_grid, mp_grid)
            ham_r0[r[0], r[1], r[2], :, :] = self.ham_r.ham_r[:, :, ir]
            if hasattr(self.ham_r, "Amn_r"):
                Amn_r0[r[0], r[1], r[2], :, :, :] = self.ham_r.Amn_r[:, :, ir, :]

        nrpairs = list(itertools.product(range(self.nnkp.natom), repeat=2))
        irvec_list = []
        ndegen_list = []
        for i, (nr1, nr2) in enumerate(nrpairs):
            rd = np.array(self.nnkp.atom_pos_r[nr2]) - np.array(
                self.nnkp.atom_pos_r[nr1]
            )
            irvec, ndegen = self._calc_irvec(rd)
            irvec_list.append(irvec)
            ndegen_list.append(ndegen)

        irvec = np.unique(np.concatenate(irvec_list), axis=0)
        nrpts = len(irvec)
        ham_r = np.zeros([self.num_wann, self.num_wann, nrpts], dtype=np.complex128)
        Amn_r = np.zeros([self.num_wann, self.num_wann, nrpts, 3], dtype=np.complex128)

        nir = (
            (2 * mp_grid[1] + 1) * (2 * mp_grid[2] + 1) * (irvec[:, 0] + mp_grid[0])
            + (2 * mp_grid[2] + 1) * (irvec[:, 1] + mp_grid[1])
            + (irvec[:, 2] + mp_grid[2])
        )
        sorted_arg = np.argsort(nir)
        irvec = irvec[sorted_arg]

        for i, (nr1, nr2) in enumerate(nrpairs):
            orb1 = [
                x for pos in self.nnkp.atom_pos[nr1] for x in self.nnkp.atom_orb[pos]
            ]
            orb2 = [
                x for pos in self.nnkp.atom_pos[nr2] for x in self.nnkp.atom_orb[pos]
            ]
            ir1 = 0
            for r, ndeg in zip(irvec_list[i], ndegen_list[i]):
                while not np.allclose(irvec[ir1], r):
                    ir1 += 1
                s = np.mod(r + mp_grid, mp_grid)
                for m, n in itertools.product(orb1, orb2):
                    ham_r[m, n, ir1] = ham_r0[s[0], s[1], s[2], m, n] / ndeg
                if hasattr(self.ham_r, "Amn_r"):
                    for m, n in itertools.product(orb1, orb2):
                        Amn_r[m, n, ir1, :] = Amn_r0[s[0], s[1], s[2], m, n, :] / ndeg

        self.ham_r.nrpts = nrpts
        self.ham_r.irvec = irvec
        self.ham_r.ham_r = ham_r
        self.ham_r.ndegen = np.ones([nrpts])
        if hasattr(self.ham_r, "Amn_r"):
            self.ham_r.Amn_r = Amn_r
