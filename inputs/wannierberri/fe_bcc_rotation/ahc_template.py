#!/usr/bin/env python3
"""Run a portable WannierBerri AHC calculation for one Fe TB file.

The production workflow used per-angle copies of this calculation. This
template keeps the numerical settings from that workflow but removes private
paths and cluster-specific assumptions.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import wannierberri as wberri


def parse_args() -> argparse.Namespace:
    """Parse the tight-binding input and lightweight runtime options."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tb_file", type=Path, help="Rotated *_tb.dat file.")
    parser.add_argument("--num-cpus", type=int, default=1)
    parser.add_argument("--fermi-energy", type=float, default=17.4112)
    parser.add_argument("--fout-name", default="Fe")
    return parser.parse_args()


def main() -> None:
    """Evaluate AHC on the manuscript WannierBerri grid."""
    args = parse_args()
    if not args.tb_file.is_file():
        raise SystemExit(f"Missing TB file: {args.tb_file}")

    parallel = wberri.Parallel(num_cpus=args.num_cpus)
    system = wberri.System_tb(tb_file=str(args.tb_file))
    efermi = np.linspace(args.fermi_energy - 3.0, args.fermi_energy + 3.0, 1000)
    grid = wberri.Grid(system, NK=[100, 100, 100])
    calculators = {
        "ahc": wberri.calculators.static.AHC(
            Efermi=efermi,
            tetra=True,
            kwargs_formula={"external_terms": False},
        )
    }
    wberri.run(
        system,
        grid=grid,
        calculators=calculators,
        parallel=parallel,
        adpt_num_iter=20,
        adpt_fac=50,
        fout_name=args.fout_name,
        restart=False,
        file_Klist="Klist_ahc.pickle",
        print_Kpoints=True,
    )


if __name__ == "__main__":
    main()

