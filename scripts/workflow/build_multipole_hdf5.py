#!/usr/bin/env python3
"""Build a compact MultiPie HDF5 basis from a matrix dictionary export."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from symwan_multipie import Multipole  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--matrix-path",
        type=Path,
        required=True,
        help="Path to a MultiPie matrix dictionary such as Fe_all_35_matrix.py or .pkl(.gz).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("multi_matrix.hdf5"),
        help="Output HDF5 path.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    multipole = Multipole(args.matrix_path)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    multipole.write_hdf5(args.output)
    print(
        "Wrote "
        f"{args.output} "
        f"(num_multipole={multipole.num_multipole}, nrpts={multipole.nrpts}, num_wann={multipole.num_wann})"
    )


if __name__ == "__main__":
    main()
