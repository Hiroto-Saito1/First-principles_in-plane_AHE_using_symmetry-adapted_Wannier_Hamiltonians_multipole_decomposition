#!/usr/bin/env python3
"""Rotate selected multipole Hamiltonian components and write per-angle TB files."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))

from symwan_multipie import MagRotation  # noqa: E402
from symwan_multipie.wannier_utils.hamiltonian import HamR  # noqa: E402


def load_config(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def compute_axis_angle(v1: np.ndarray, v2: np.ndarray) -> tuple[np.ndarray, float]:
    """Return the axis and degree angle that rotates `v1` onto `v2`."""
    v1 = v1 / np.linalg.norm(v1)
    v2 = v2 / np.linalg.norm(v2)
    axis = np.cross(v1, v2)
    if np.linalg.norm(axis) < 1.0e-10:
        return np.array([0.0, 0.0, 1.0]), 0.0
    axis = axis / np.linalg.norm(axis)
    angle = np.degrees(np.arccos(np.clip(np.dot(v1, v2), -1.0, 1.0)))
    return axis, angle


def parse_csv_list(text: str | None, *, cast=str) -> list | None:
    if text is None:
        return None
    values = [item.strip() for item in text.split(",") if item.strip()]
    return [cast(value) for value in values]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--multi-path", type=Path, required=True, help="Decomposed multipole HDF5 file.")
    parser.add_argument("--samb-path", type=Path, required=True, help="Fe_samb.py metadata file.")
    parser.add_argument("--tb-input", type=Path, required=True, help="Reference tb.dat that supplies `a` and `Amnrs`.")
    parser.add_argument("--plane", choices=["103", "111"], required=True, help="Rotation plane label from rotation_grid.json.")
    parser.add_argument(
        "--config",
        type=Path,
        default=Path(__file__).with_name("rotation_grid.json"),
        help="Rotation-grid JSON file.",
    )
    parser.add_argument("--types", default=None, help="Comma-separated multipole types. Default uses rotation_grid.json.")
    parser.add_argument("--irreps", default=None, help="Comma-separated irreps. Default uses rotation_grid.json.")
    parser.add_argument("--ranks", default=None, help="Comma-separated ranks. Default keeps all ranks.")
    parser.add_argument("--coef-amp-para", type=float, default=1.0)
    parser.add_argument("--phi-start", type=int, default=None)
    parser.add_argument("--phi-stop", type=int, default=None)
    parser.add_argument("--phi-step", type=int, default=None)
    parser.add_argument("--output-prefix", default=None, help="Output file prefix before `_phi{deg}_tb.dat`.")
    return parser.parse_args()


def default_output_prefix(multi_path: Path) -> str:
    stem = multi_path.name
    for suffix in [".hdf5", ".dat.gz", ".dat"]:
        if stem.endswith(suffix):
            stem = stem[: -len(suffix)]
    for suffix in ["_hr", "_tb"]:
        if stem.endswith(suffix):
            stem = stem[: -len(suffix)]
    return stem


def main() -> None:
    args = parse_args()
    config = load_config(args.config)
    plane = next(entry for entry in config["rotation_planes"] if entry["label"] == args.plane)
    filter_config = config["component_filter"]

    types = parse_csv_list(args.types) or filter_config["types"]
    irreps = parse_csv_list(args.irreps) or filter_config["irreps"]
    ranks = parse_csv_list(args.ranks, cast=int)

    phi_start = args.phi_start if args.phi_start is not None else plane["phi_degrees"]["start"]
    phi_stop = args.phi_stop if args.phi_stop is not None else plane["phi_degrees"]["stop"]
    phi_step = args.phi_step if args.phi_step is not None else plane["phi_degrees"]["step"]
    phi_list = list(range(phi_start, phi_stop + 1, phi_step))

    initial_vector = np.array(plane["initial_vector"], dtype=np.float64)
    axis2 = np.array(plane["axis2"], dtype=np.float64)
    axis1, theta = compute_axis_angle(np.array([1.0, 0.0, 0.0]), initial_vector)

    reference = HamR.from_tb_dat(args.tb_input)
    output_prefix = args.output_prefix or default_output_prefix(args.multi_path)

    rotation = MagRotation(
        multi_path=args.multi_path,
        samb_path=args.samb_path,
        filters=[
            {
                "types": types,
                "ranks": ranks,
                "irreps": irreps,
                "axis1": axis1.tolist(),
                "axis2": axis2.tolist(),
                "theta": 0.0,
                "phi": 0.0,
                "coef_amp_para": args.coef_amp_para,
            }
        ],
    )

    try:
        hrs_filtered = rotation.hrs_filtered_list[0]
        for phi in phi_list:
            rotated = rotation.rotate_mag(
                hrs_filtered,
                axis1=axis1.tolist(),
                axis2=axis2.tolist(),
                theta=theta,
                phi=phi,
                coef_amp_para=args.coef_amp_para,
            )
            hrs = rotated + rotation.hrs_other
            output = HamR(
                irvec=reference.irvec,
                ndegen=reference.ndegen,
                hrs=hrs,
                a=reference.a,
                Amnrs=reference.Amnrs,
            )
            path = Path(f"{output_prefix}_phi{phi}_tb.dat")
            output.export_tb_dat(path)
            print(f"Wrote {path}")
    finally:
        rotation.close()


if __name__ == "__main__":
    main()
