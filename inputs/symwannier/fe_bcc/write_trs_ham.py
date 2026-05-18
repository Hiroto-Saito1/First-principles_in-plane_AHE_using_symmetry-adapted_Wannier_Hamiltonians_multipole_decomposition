"""Build a TRS-style Fe `tb.dat` by keeping selected magnetization components."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))

from symwan_multipie.wannier_utils.hamiltonian import HamR  # noqa: E402


def reshape_hrs_to_ham_spinor(hrs: np.ndarray) -> np.ndarray:
    nrpts, num_wann, _ = hrs.shape
    spinor = hrs.reshape(nrpts, num_wann // 2, 2, num_wann // 2, 2)
    return np.einsum("ijklm->ikmjl", spinor)


def reshape_ham_spinor_to_hrs(ham_spinor: np.ndarray) -> np.ndarray:
    nrpts, _, _, norb, _ = ham_spinor.shape
    hrs = np.einsum("ijklm->iljmk", ham_spinor)
    return hrs.reshape(nrpts, 2 * norb, 2 * norb)


def su2_rotation(axis: np.ndarray, angle_radians: float) -> np.ndarray:
    sigma_x = np.array([[0.0 + 0.0j, 1.0 + 0.0j], [1.0 + 0.0j, 0.0 + 0.0j]])
    sigma_y = np.array([[0.0 + 0.0j, 0.0 - 1.0j], [0.0 + 1.0j, 0.0 + 0.0j]])
    sigma_z = np.array([[1.0 + 0.0j, 0.0 + 0.0j], [0.0 + 0.0j, -1.0 + 0.0j]])
    unit = axis / np.linalg.norm(axis)
    generator = unit[0] * sigma_x + unit[1] * sigma_y + unit[2] * sigma_z
    return (
        np.cos(angle_radians / 2) * np.eye(2, dtype=np.complex128)
        - 1j * np.sin(angle_radians / 2) * generator
    )


def spinor_to_vector(spinor: np.ndarray) -> np.ndarray:
    vector = np.zeros((4, spinor.shape[2], spinor.shape[3]), dtype=np.complex128)
    vector[0] = 0.5 * (spinor[0, 0] + spinor[1, 1])
    vector[1] = 0.5 * (spinor[0, 1] + spinor[1, 0])
    vector[2] = (spinor[1, 0] - spinor[0, 1]) / (2j)
    vector[3] = 0.5 * (spinor[0, 0] - spinor[1, 1])
    return vector


def vector_to_spinor(vector: np.ndarray) -> np.ndarray:
    spinor = np.zeros((2, 2, vector.shape[1], vector.shape[2]), dtype=np.complex128)
    spinor[0, 0] = vector[0] + vector[3]
    spinor[1, 1] = vector[0] - vector[3]
    spinor[0, 1] = vector[1] - 1j * vector[2]
    spinor[1, 0] = vector[1] + 1j * vector[2]
    return spinor


def extract_component_hamiltonian(ham: HamR, mag_component: str) -> np.ndarray:
    component_indices = {"x": 1, "y": 2, "z": 3}
    ham_spinor = reshape_hrs_to_ham_spinor(ham.hrs)
    unitary_tr = su2_rotation(np.array([0.0, 1.0, 0.0]), np.pi)
    ham_tr = np.einsum(
        "ij,ojklm,kn->oinlm",
        unitary_tr,
        np.conjugate(ham_spinor),
        np.conjugate(unitary_tr.T),
    )
    mag_orig = 0.5 * (ham_spinor - ham_tr)
    mag_extracted = mag_orig.copy()

    if mag_component != "all":
        component_index = component_indices[mag_component]
        for ir in range(ham.nrpts):
            mag_vector = spinor_to_vector(mag_orig[ir])
            selected = np.zeros_like(mag_vector)
            selected[component_index] = mag_vector[component_index]
            mag_extracted[ir] = vector_to_spinor(selected)

    ham_sym = 0.5 * (ham_spinor + ham_tr)
    hopping = np.zeros_like(ham_sym)
    soc = np.zeros_like(ham_sym)
    for ir in range(ham.nrpts):
        vector = spinor_to_vector(ham_sym[ir])
        hopping_vector = np.zeros_like(vector)
        soc_vector = np.zeros_like(vector)
        hopping_vector[0] = vector[0]
        soc_vector[1:4] = vector[1:4]
        hopping[ir] = vector_to_spinor(hopping_vector)
        soc[ir] = vector_to_spinor(soc_vector)

    return reshape_ham_spinor_to_hrs(mag_extracted + hopping + soc)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write a cleaned TRS-style Fe Wannier tb.dat from a source tb.dat."
    )
    parser.add_argument("--input", type=Path, default=Path("pwscf_py_ed_tb.dat"))
    parser.add_argument("--output-tb", type=Path, default=Path("trs_py_ed_tb.dat"))
    parser.add_argument("--output-hr", type=Path, default=None)
    parser.add_argument(
        "--mag-component",
        choices=["x", "y", "z", "all"],
        default="x",
        help="Magnetization component retained when reconstructing the Hamiltonian.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    ham = HamR.from_tb_dat(args.input)
    hrs = extract_component_hamiltonian(ham, args.mag_component)
    rotated = HamR(irvec=ham.irvec, ndegen=ham.ndegen, hrs=hrs, a=ham.a, Amnrs=ham.Amnrs)
    rotated.export_tb_dat(args.output_tb)
    if args.output_hr is not None:
        rotated.export_hr_dat(args.output_hr)
    print(f"Wrote {args.output_tb}")
    if args.output_hr is not None:
        print(f"Wrote {args.output_hr}")


if __name__ == "__main__":
    main()
