#!/usr/bin/env python3
"""Compute angle-dependent total-energy summaries from rotated Fe TB files."""

from __future__ import annotations

import argparse
from glob import glob
from pathlib import Path
import re
import xml.dom.minidom as minidom
import xml.etree.ElementTree as ET

import numpy as np


ROOT = Path(__file__).resolve().parents[3]
import sys

sys.path.insert(0, str(ROOT / "src"))

from symwan_multipie.wannier_utils.band import WanBand  # noqa: E402
from symwan_multipie.wannier_utils.hamiltonian import HamR  # noqa: E402


def uniform_kmesh(mesh: tuple[int, int, int] | list[int]) -> np.ndarray:
    points = []
    for x in np.linspace(0.0, 1.0, mesh[0], endpoint=False):
        for y in np.linspace(0.0, 1.0, mesh[1], endpoint=False):
            for z in np.linspace(0.0, 1.0, mesh[2], endpoint=False):
                points.append([x, y, z])
    return np.array(points, dtype=np.float64)


def total_energy(eigenvalues: np.ndarray, num_electrons: int) -> float:
    flat = np.sort(eigenvalues.reshape(-1), kind="heapsort")
    return float(np.sum(flat[: num_electrons * len(eigenvalues)]) / len(eigenvalues))


def pretty_write_xml(root: ET.Element, path: Path) -> None:
    xml_str = ET.tostring(root, encoding="utf-8")
    pretty = minidom.parseString(xml_str).toprettyxml(indent="  ")
    path.write_text(pretty, encoding="utf-8")


def calc_kmesh_dep(tb_dir: Path, prefix: str, output_path: Path, num_electrons: int, kmesh_init: list[int], max_iter: int) -> None:
    ham_0 = HamR.from_tb_dat(tb_dir / f"{prefix}_phi0_tb.dat")
    ham_45 = HamR.from_tb_dat(tb_dir / f"{prefix}_phi45_tb.dat")
    root = ET.Element("kmesh_dep")
    mesh = list(kmesh_init)
    for index in range(max_iter):
        kpoints = uniform_kmesh(mesh)
        energy_0 = total_energy(WanBand(ham_0, kpoints, ham_0.hrs).ek_all, num_electrons)
        energy_45 = total_energy(WanBand(ham_45, kpoints, ham_45.hrs).ek_all, num_electrons)
        iteration = ET.SubElement(root, "iteration", index=str(index))
        ET.SubElement(iteration, "kmesh").text = str(mesh)
        ET.SubElement(iteration, "energy_diff").text = str(energy_45 - energy_0)
        pretty_write_xml(root, output_path)
        mesh = [value + 10 for value in mesh]


def calc_angle_dep(tb_dir: Path, prefix: str, output_path: Path, num_electrons: int, kmesh: list[int]) -> None:
    kpoints = uniform_kmesh(kmesh)
    pattern = str(tb_dir / f"{prefix}_phi*_tb.dat")
    phi_pattern = re.compile(r"_phi([0-9.]+)_tb\.dat$")
    entries: list[tuple[float, Path]] = []
    for file_name in glob(pattern):
        match = phi_pattern.search(file_name)
        if match is None:
            continue
        entries.append((float(match.group(1)), Path(file_name)))
    entries.sort(key=lambda item: item[0])

    root = ET.Element("angle_dep")
    for phi, path in entries:
        ham = HamR.from_tb_dat(path)
        energy = total_energy(WanBand(ham, kpoints, ham.hrs).ek_all, num_electrons)
        angle = ET.SubElement(root, "angle", phi=str(phi))
        ET.SubElement(angle, "energy").text = str(energy)
    pretty_write_xml(root, output_path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tb-dir", type=Path, default=Path("."))
    parser.add_argument("--prefix", required=True, help="Prefix such as trs_py_ed, trs_py_pd, or trs_tb.")
    parser.add_argument("--num-electrons", type=int, default=8)
    parser.add_argument("--kmesh-dep", action="store_true", help="Write phi=0 vs phi=45 k-mesh convergence XML.")
    parser.add_argument("--angle-dep", action="store_true", help="Write all-angle energy XML.")
    parser.add_argument("--kmesh-output", type=Path, default=None)
    parser.add_argument("--angle-output", type=Path, default=None)
    parser.add_argument("--kmesh-init", nargs=3, type=int, default=[10, 10, 10])
    parser.add_argument("--angle-kmesh", nargs=3, type=int, default=[90, 90, 90])
    parser.add_argument("--max-iter", type=int, default=100)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.kmesh_dep and not args.angle_dep:
        raise SystemExit("Select at least one mode: --kmesh-dep and/or --angle-dep.")

    if args.kmesh_dep:
        output = args.kmesh_output or Path(f"kmesh_dep_{args.prefix}.xml")
        calc_kmesh_dep(args.tb_dir, args.prefix, output, args.num_electrons, args.kmesh_init, args.max_iter)
        print(f"Wrote {output}")

    if args.angle_dep:
        output = args.angle_output or Path(f"angle_dep_{args.prefix}.xml")
        calc_angle_dep(args.tb_dir, args.prefix, output, args.num_electrons, args.angle_kmesh)
        print(f"Wrote {output}")


if __name__ == "__main__":
    main()
