"""Archived standalone BCC `p_z`-`d_xy` model used for the minimal-model figure."""

import numpy as np
from pathlib import Path
from typing import Dict, Tuple, List, Optional, Union
import argparse


class BCCPDModelHR:
    """
    BCC lattice, p-d two-orbital (with spin) model that can export Wannier90 hr.dat.
    Basis order: (p↑, p↓, d↑, d↓) = orbital (p/d) ⊗ spin
    H = H_on + H_ex + H_hop(sym) + H_MT
    where
      H_on  = eps0 * τ0 ⊗ σ0 + (Δ0/2) * τz ⊗ σ0
      H_ex  = -Δ * τ0 ⊗ (M̂ · σ)
      H_hop = (t0 τ0 + t3 τz + t_pd τx) ⊗ σ0  (applies to all selected neighbors)
      H_MT  = -i t_T τy ⊗ [ (M × d̂) · σ ]   (applies to all selected neighbors; d̂ is bond direction)

    Neighbor range can be configured via class arguments:
      - max_shell: include neighbors up to this shell (1 = 1NN, 2 = 2NN, ...)
      - custom_Rs: alternatively, provide explicit list of R = (n1,n2,n3) in primitive coordinates
    """

    def __init__(
        self,
        eps0: float = 0.0,
        Delta0: float = 0.5,
        Delta: float = 1.0,
        t0: Union[float, List[float]] = 0.5,
        t3: Union[float, List[float]] = 0.1,
        t_pd: Union[float, List[float]] = 0.2,
        t_T: Union[float, List[float]] = 0.10,
        M: Optional[Tuple[float, float, float]] = None,
        max_shell: int = 1,
        custom_Rs: Optional[List[Tuple[int, int, int]]] = None,
        a: float = 1.0,
    ):
        # Parameters (eV)
        self.eps0 = float(eps0)
        self.Delta0 = float(Delta0)
        self.Delta = float(Delta)
        # Neighbor configuration first (needed to size/broadcast hopping params)
        if max_shell < 1:
            raise ValueError("max_shell must be >= 1")
        self.max_shell = int(max_shell)
        self.custom_Rs = list(custom_Rs) if custom_Rs is not None else None

        # Hopping parameters per shell (broadcast scalars to max_shell)
        def _per_shell(x, name: str) -> np.ndarray:
            if isinstance(x, (list, tuple, np.ndarray)):
                arr = np.array(x, dtype=float).ravel()
                if arr.size == 0:
                    raise ValueError(f"{name} must not be empty")
            else:
                arr = np.array([float(x)], dtype=float)
            if arr.size == 1:
                arr = np.repeat(arr, self.max_shell)
            elif arr.size < self.max_shell:
                raise ValueError(
                    f"{name} length {arr.size} < max_shell {self.max_shell}. Provide length 1 or >= max_shell."
                )
            else:
                arr = arr[: self.max_shell]
            return arr.astype(float)

        self.t0_s = _per_shell(t0, "t0")
        self.t3_s = _per_shell(t3, "t3")
        self.tpd_s = _per_shell(t_pd, "t_pd")
        self.tT_s = _per_shell(t_T, "t_T")

        # Lattice parameter (only direction matters for current model)
        self.a = float(a)

        # Magnetization vector
        if M is None:
            self.M = np.array([0.0, 1.0, 0.0], dtype=float)  # default along [010]
        else:
            self.M = np.array(M, dtype=float)

        # Neighbor configuration already set above

        # Pauli matrices
        self.sx = np.array([[0, 1], [1, 0]], dtype=complex)
        self.sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
        self.sz = np.array([[1, 0], [0, -1]], dtype=complex)
        self.s0 = np.eye(2, dtype=complex)

        self.tx = np.array([[0, 1], [1, 0]], dtype=complex)
        self.ty = np.array([[0, -1j], [1j, 0]], dtype=complex)
        self.tz = np.array([[1, 0], [0, -1]], dtype=complex)
        self.t0orb = np.eye(2, dtype=complex)

        # cache for neighbors
        self._nn = None
        self._nn_key = None

    # ---------- utilities ----------
    @staticmethod
    def _unit(v):
        v = np.array(v, dtype=float)
        n = np.linalg.norm(v)
        if n == 0.0:
            return v
        return v / n

    @staticmethod
    def _kron(A, B):
        return np.kron(A, B).astype(complex)

    # ---------- lattice (BCC) ----------
    def _bcc_primitive_vectors(self) -> np.ndarray:
        """Return 3x3 matrix whose rows are primitive vectors a1,a2,a3 (in Cartesian) for BCC.
        a1=(a/2)(-1, 1, 1), a2=(a/2)( 1,-1, 1), a3=(a/2)( 1, 1,-1)
        """
        a = self.a
        return np.array(
            [
                [-1, 1, 1],
                [1, -1, 1],
                [1, 1, -1],
            ],
            dtype=float,
        ) * (a / 2.0)

    def _cart_from_R(self, R: Tuple[int, int, int]) -> np.ndarray:
        a123 = self._bcc_primitive_vectors()
        n = np.array(R, dtype=float)
        # rows are a1,a2,a3; r = n1*a1 + n2*a2 + n3*a3
        return n @ a123

    def bcc_neighbors(self) -> List[Tuple[Tuple[int, int, int], np.ndarray, int]]:
        """
        General neighbor generator. Returns list of (R=(n1,n2,n3), d_hat, shell_idx) for BCC up to max_shell
        or for explicitly provided custom_Rs. d_hat is the unit vector of the Cartesian bond direction.
        """
        key = (
            self.a,
            self.max_shell,
            None if self.custom_Rs is None else tuple(self.custom_Rs),
        )
        if self._nn is not None and self._nn_key == key:
            return self._nn

        out: List[Tuple[Tuple[int, int, int], np.ndarray, int]] = []

        if self.custom_Rs is not None:
            # group custom_Rs by distance and assign shell indices
            by_dist: Dict[float, List[Tuple[int, int, int]]] = {}
            for R in self.custom_Rs:
                if tuple(R) == (0, 0, 0):
                    continue
                r = self._cart_from_R(tuple(R))
                d2 = float(np.dot(r, r))
                if d2 == 0.0:
                    continue
                by_dist.setdefault(d2, []).append(tuple(R))
            shells = sorted(by_dist.keys())[: self.max_shell]
            out = []
            for s_idx, d2 in enumerate(shells, start=1):
                for R in by_dist[d2]:
                    r = self._cart_from_R(R)
                    d_hat = self._unit(r)
                    out.append((R, d_hat, s_idx))
            # Deduplicate by R while preserving order
            seen = set()
            out_unique: List[Tuple[Tuple[int, int, int], np.ndarray, int]] = []
            for R, d, s_idx in out:
                if R not in seen:
                    seen.add(R)
                    out_unique.append((R, d, s_idx))
            self._nn = out_unique
            self._nn_key = key
            return self._nn

        # Auto-enumerate by shells
        # Increase nmax until we can identify at least max_shell unique distances
        target_shells = self.max_shell
        nmax = max(2, 2 * target_shells)
        max_attempt = 20  # safety
        shells: List[float] = []
        by_dist: Dict[float, List[Tuple[int, int, int]]] = {}
        attempt = 0
        while attempt < max_attempt:
            attempt += 1
            by_dist.clear()
            # enumerate R within [-nmax, nmax] for each n1,n2,n3
            for n1 in range(-nmax, nmax + 1):
                for n2 in range(-nmax, nmax + 1):
                    for n3 in range(-nmax, nmax + 1):
                        if n1 == 0 and n2 == 0 and n3 == 0:
                            continue
                        R = (n1, n2, n3)
                        r = self._cart_from_R(R)
                        d2 = float(np.dot(r, r))
                        if d2 == 0.0:
                            continue
                        by_dist.setdefault(d2, []).append(R)
            # unique shells sorted by distance
            shells = sorted(by_dist.keys())
            if len(shells) >= target_shells:
                break
            nmax += 1

        if len(shells) < target_shells:
            raise RuntimeError(
                f"Unable to find {target_shells} shells within search range; found {len(shells)}."
            )

        selected_dists = set(shells[:target_shells])
        # collect all R for selected shells
        out = []
        for s_idx, d2 in enumerate(sorted(selected_dists), start=1):
            for R in by_dist[d2]:
                r = self._cart_from_R(R)
                d_hat = self._unit(r)
                out.append((R, d_hat, s_idx))

        # cache and return
        self._nn = out
        self._nn_key = key
        return out

    # ---------- magnetization setters ----------
    def set_M_by_angle_in_103(self, psi_deg: float):
        """
        Set M to rotate within the (103) plane:
          M(psi) = cos psi * e010 + sin psi * e301,  e301 = (3,0,1)/||...||
        """
        e010 = np.array([0.0, -1.0, 0.0])
        e301 = self._unit(np.array([3.0, 0.0, -1.0]))
        self.M = np.cos(np.deg2rad(psi_deg)) * e010 + np.sin(np.deg2rad(psi_deg)) * e301

    def set_M(self, Mx: float, My: float, Mz: float):
        """Set magnetization vector directly."""
        self.M = np.array([Mx, My, Mz], dtype=float)

    # ---------- Hamiltonian terms (4x4 blocks) ----------
    def H_on(self) -> np.ndarray:
        """Onsite term H_on at R=0 (no exchange)."""
        return self.eps0 * self._kron(
            self.t0orb, self.s0
        ) + 0.5 * self.Delta0 * self._kron(self.tz, self.s0)

    def H_ex(self) -> np.ndarray:
        """Onsite exchange term H_ex at R=0."""
        Mhat = self._unit(self.M)
        S = Mhat[0] * self.sx + Mhat[1] * self.sy + Mhat[2] * self.sz
        return (-self.Delta) * self._kron(self.t0orb, S)

    def H_hop_symmetric(self, shell_idx: int) -> np.ndarray:
        """
        Direction-independent part used on bonds of a given shell:
            (t0[s] τ0 + t3[s] τz + t_pd[s] τx) ⊗ σ0
        """
        s = shell_idx - 1
        return self._kron(
            self.t0_s[s] * self.t0orb
            + self.t3_s[s] * self.tz
            + self.tpd_s[s] * self.tx,
            self.s0,
        )

    def H_MT_on_bond(self, d_hat: np.ndarray, shell_idx: int) -> np.ndarray:
        """
        Magnetic-toroidal p-d hopping on a specific bond direction d_hat:
            H_MT(d) = -i t_T[s] τy ⊗ [ (M × d_hat) · σ ]
        """
        C = np.cross(self.M, d_hat)  # M × d_hat
        S = C[0] * self.sx + C[1] * self.sy + C[2] * self.sz  # (σ · (M × d_hat))
        s = shell_idx - 1
        return (-1j * self.tT_s[s]) * self._kron(self.ty, S)

    def H_onsite_total(self) -> np.ndarray:
        """Return onsite 4x4 block (H_on + H_ex)."""
        return self.H_on() + self.H_ex()

    def H_bond_total(self, d_hat: np.ndarray, shell_idx: int) -> np.ndarray:
        """Return total bond 4x4 block (symmetric + MT) for a specific shell."""
        return self.H_hop_symmetric(shell_idx) + self.H_MT_on_bond(d_hat, shell_idx)

    # ---------- assembly of H(R) ----------
    def assemble_HR(
        self,
    ) -> Tuple[Dict[Tuple[int, int, int], np.ndarray], List[Tuple[int, int, int]]]:
        """
        Build H(R) up to selected neighbors. Returns (HR, R_list).
        HR is a dict mapping R=(n1,n2,n3) to a 4x4 complex matrix.
        """
        HR: Dict[Tuple[int, int, int], np.ndarray] = {}
        nn = self.bcc_neighbors()
        R_list = [(0, 0, 0)] + [R for (R, _, _) in nn]

        # Onsite
        HR[(0, 0, 0)] = self.H_onsite_total()

        # bonds (per selected neighbor list)
        for R, d_hat, shell_idx in nn:
            HR[R] = self.H_bond_total(d_hat, shell_idx)

        # Enforce Hermiticity: H(-R) = H(R)^\dagger (average if both exist)
        for R, H in list(HR.items()):
            Rm = (-R[0], -R[1], -R[2])
            if Rm in HR:
                HR[R] = 0.5 * (H + HR[Rm].conj().T)
                HR[Rm] = HR[R].conj().T

        return HR, R_list

    # ---------- hr.dat writer ----------
    @staticmethod
    def _fmt_line(R, i, j, val: complex) -> str:
        return f"{R[0]:6d}{R[1]:6d}{R[2]:6d}{i:6d}{j:6d}{val.real:22.16f}{val.imag:22.16f}\n"

    def write_hr_dat(
        self,
        filename: str,
        HR: Dict[Tuple[int, int, int], np.ndarray],
        R_list: List[Tuple[int, int, int]],
    ):
        """
        Write Wannier90-like hr.dat file:
          num_wann
          nrpts
          ndegen(=1) ... up to 15 per line
          R1 R2 R3 i j Re Im
        """
        num_wann = next(iter(HR.values())).shape[0]
        nrpts = len(R_list)
        ndegen = [1] * nrpts

        with open(filename, "w") as f:
            f.write("Generated by BCCPDModelHR\n")
            f.write(f"{num_wann:10d}\n")
            f.write(f"{nrpts:10d}\n")
            for k in range(0, nrpts, 15):
                block = ndegen[k : k + 15]
                f.write("".join([f"{x:5d}" for x in block]) + "\n")
            for R in R_list:
                H = HR[R]
                for i in range(num_wann):
                    for j in range(num_wann):
                        f.write(self._fmt_line(R, i + 1, j + 1, H[i, j]))


if __name__ == "__main__":
    # Example usage:
    # Build model, rotate M in the (103) plane by psi (degrees) passed via command-line, assemble HR, and write hr.dat next to this file.
    parser = argparse.ArgumentParser(
        description="Generate hr.dat from BCC p-d model with M rotated in (103) plane."
    )
    parser.add_argument(
        "--psi",
        "-p",
        type=float,
        default=13.0,
        help="Rotation angle psi (degrees) in the (103) plane. Default: 13.0",
    )
    parser.add_argument(
        "--out",
        "-o",
        type=str,
        default=None,
        help="Output hr.dat filename (default: test_hr.dat next to this file)",
    )
    args = parser.parse_args()

    model = BCCPDModelHR(
        eps0=0.0,
        Delta0=1.0,
        Delta=1.0,
        t0=[-1.0, 0.0],
        t3=0.0,
        t_pd=0.0,
        t_T=[0.2, 0.14],
        max_shell=2,
    )
    model.set_M_by_angle_in_103(psi_deg=args.psi)
    HR, R_list = model.assemble_HR()
    out = Path(__file__).with_name(args.out if args.out is not None else "test_hr.dat")
    model.write_hr_dat(str(out), HR, R_list)
    print(
        f"Wrote {out} with {len(R_list)} R-points and {next(iter(HR.values())).shape[0]} Wannier functions. "
        f"Used psi_deg={args.psi}"
    )
