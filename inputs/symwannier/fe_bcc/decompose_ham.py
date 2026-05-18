"""Decompose Fe Wannier Hamiltonians into the 35-shell SAMB basis."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys
import time


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))

from symwan_multipie import MultipoleDecomposition  # noqa: E402
from symwan_multipie.wannier_utils.hamiltonian import HamR  # noqa: E402


INITIAL_KET = [
    "(s,U)@Fe_1",
    "(s,D)@Fe_1",
    "(px,U)@Fe_1",
    "(px,D)@Fe_1",
    "(py,U)@Fe_1",
    "(py,D)@Fe_1",
    "(pz,U)@Fe_1",
    "(pz,D)@Fe_1",
    "(du,U)@Fe_1",
    "(du,D)@Fe_1",
    "(dv,U)@Fe_1",
    "(dv,D)@Fe_1",
    "(dyz,U)@Fe_1",
    "(dyz,D)@Fe_1",
    "(dzx,U)@Fe_1",
    "(dzx,D)@Fe_1",
    "(dxy,U)@Fe_1",
    "(dxy,D)@Fe_1",
]

FINAL_KET = [
    "(s,U)@Fe_1",
    "(s,D)@Fe_1",
    "(pz,U)@Fe_1",
    "(pz,D)@Fe_1",
    "(px,U)@Fe_1",
    "(px,D)@Fe_1",
    "(py,U)@Fe_1",
    "(py,D)@Fe_1",
    "(du,U)@Fe_1",
    "(du,D)@Fe_1",
    "(dzx,U)@Fe_1",
    "(dzx,D)@Fe_1",
    "(dyz,U)@Fe_1",
    "(dyz,D)@Fe_1",
    "(dv,U)@Fe_1",
    "(dv,D)@Fe_1",
    "(dxy,U)@Fe_1",
    "(dxy,D)@Fe_1",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Decompose Fe Wannier Hamiltonians into a precomputed MultiPie basis."
    )
    parser.add_argument("--matrix-path", type=Path, required=True, help="Path to MultiPie HDF5 basis.")
    parser.add_argument("--symwan-pd", action="store_true", help="Decompose pwscf_py_pd_tb.dat.")
    parser.add_argument("--symwan-ed", action="store_true", help="Decompose pwscf_py_ed_tb.dat.")
    parser.add_argument("--trs-py-ed", action="store_true", help="Decompose trs_py_ed_tb.dat.")
    parser.add_argument("--wan-orig", action="store_true", help="Decompose pwscf_tb.dat.")
    return parser.parse_args()


def run_case(label: str, input_path: Path, output_path: Path, matrix_path: Path) -> None:
    if not input_path.exists() and not input_path.with_suffix(input_path.suffix + ".gz").exists():
        raise FileNotFoundError(input_path)

    start = time.perf_counter()
    ham = HamR.from_tb_dat(input_path)
    decomposition = MultipoleDecomposition(
        ham_r=ham,
        multipole_path=matrix_path,
        initial_ket=INITIAL_KET,
        final_ket=FINAL_KET,
    )
    decomposition.write_hdf5(output_path)
    elapsed = time.perf_counter() - start
    print(f"[{label}] wrote {output_path} in {elapsed:.2f} s")


def main() -> None:
    args = parse_args()
    selected = [
        args.symwan_pd,
        args.symwan_ed,
        args.trs_py_ed,
        args.wan_orig,
    ]
    if not any(selected):
        raise SystemExit("Select at least one target: --symwan-pd, --symwan-ed, --trs-py-ed, or --wan-orig.")

    cases = [
        ("symwan_pd", args.symwan_pd, Path("pwscf_py_pd_tb.dat"), Path("pwscf_py_pd_tb.hdf5")),
        ("symwan_ed", args.symwan_ed, Path("pwscf_py_ed_tb.dat"), Path("pwscf_py_ed_tb.hdf5")),
        ("trs_py_ed", args.trs_py_ed, Path("trs_py_ed_tb.dat"), Path("trs_py_ed_tb.hdf5")),
        ("wan_orig", args.wan_orig, Path("pwscf_tb.dat"), Path("pwscf_tb.hdf5")),
    ]
    for label, enabled, input_path, output_path in cases:
        if enabled:
            run_case(label, input_path, output_path, args.matrix_path)


if __name__ == "__main__":
    main()
