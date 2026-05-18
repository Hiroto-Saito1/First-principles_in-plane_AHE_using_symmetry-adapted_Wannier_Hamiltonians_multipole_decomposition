"""Compute Fe reconstruction errors from decomposed SymWannier Hamiltonians."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys
import time


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))

from symwan_multipie import EnergyDiff  # noqa: E402
from symwan_multipie.wannier_utils.hamiltonian import HamR  # noqa: E402


IRREPS_ALL = ["A1g", "A1u", "A2g", "A2u", "Eg", "Eu", "T1g", "T1u", "T2g", "T2u"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare original and multipole-reconstructed Fe Wannier Hamiltonians."
    )
    parser.add_argument(
        "exclude_irreps",
        nargs="*",
        help="Irreps removed from the reconstruction. If omitted, use the full basis.",
    )
    parser.add_argument("--wan-ed-tb", type=Path, default=Path("pwscf_tb.dat"))
    parser.add_argument("--wan-ed-hdf5", type=Path, default=Path("pwscf_tb.hdf5"))
    parser.add_argument("--symwan-ed-tb", type=Path, default=Path("pwscf_py_ed_tb.dat"))
    parser.add_argument("--symwan-ed-hdf5", type=Path, default=Path("pwscf_py_ed_tb.hdf5"))
    parser.add_argument("--symwan-trs", type=Path, default=Path("trs_py_ed_tb.dat"))
    parser.add_argument("--symwan-trs-hdf5", type=Path, default=Path("trs_py_ed_tb.hdf5"))
    parser.add_argument("--samb-path", type=Path, required=True)
    parser.add_argument("--kmesh", nargs=3, type=int, default=[8, 8, 8])
    return parser.parse_args()


def load_hamiltonian(path: Path) -> HamR:
    if path.name.endswith("_tb.dat") or path.name.endswith("_tb.dat.gz"):
        return HamR.from_tb_dat(path)
    return HamR.from_hr_dat(path)


def run_case(label: str, ham_path: Path, multi_path: Path, samb_path: Path, irreps: list[str] | None, kmesh: list[int]) -> None:
    start = time.perf_counter()
    result = EnergyDiff(
        ham_r=load_hamiltonian(ham_path),
        multi_path=multi_path,
        samb_path=samb_path,
        irreps=irreps,
        coef_amp_para=0.0,
        kmesh=kmesh,
    )
    elapsed = time.perf_counter() - start
    print(f"{label}: {result.energy_diff * 1.0e3:.6f} meV")
    print(f"  max_diff: {result.max_diff * 1.0e3:.6f} meV at {result.max_irvec.tolist()}")
    print(f"  irvec_range: {result.hrs_irvec_range.tolist()}")
    print(f"  expanded_irvec_range: {result.hrs_expand_irvec_range.tolist()}")
    print(f"  elapsed: {elapsed:.2f} s")


def main() -> None:
    args = parse_args()
    excluded = args.exclude_irreps
    if excluded:
        invalid = sorted(set(excluded) - set(IRREPS_ALL))
        if invalid:
            raise SystemExit(f"Unknown irreps: {', '.join(invalid)}")
        irreps = [irrep for irrep in IRREPS_ALL if irrep not in excluded]
    else:
        irreps = None

    run_case(
        "wan_ed",
        args.wan_ed_tb,
        args.wan_ed_hdf5,
        args.samb_path,
        irreps,
        args.kmesh,
    )
    run_case(
        "symwan_ed",
        args.symwan_ed_tb,
        args.symwan_ed_hdf5,
        args.samb_path,
        irreps,
        args.kmesh,
    )
    run_case(
        "symwan_trs",
        args.symwan_trs,
        args.symwan_trs_hdf5,
        args.samb_path,
        irreps,
        args.kmesh,
    )


if __name__ == "__main__":
    main()
