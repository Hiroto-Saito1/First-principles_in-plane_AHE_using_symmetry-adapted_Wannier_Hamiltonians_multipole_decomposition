#!/usr/bin/env python3
"""Prepare and optionally execute per-angle WannierBerri AHC runs."""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess

from make_ahc_jobs import prepare_jobs


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tb-dir", type=Path, default=Path("."))
    parser.add_argument(
        "--template",
        type=Path,
        default=Path(__file__).with_name("ahc_template.py"),
    )
    parser.add_argument(
        "--targets",
        nargs="*",
        choices=["ed_phi", "pd_phi", "tb_phi"],
        default=["ed_phi", "pd_phi", "tb_phi"],
        help="Target rotated TB prefixes to prepare.",
    )
    parser.add_argument("--step", type=int, default=5)
    parser.add_argument("--execute", action="store_true", help="Run each generated run_ahc.sh locally after preparing it.")
    parser.add_argument("--num-cpus", type=int, default=1, help="Passed through to ahc_template.py when --execute is used.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    prepared: list[Path] = []
    for target in args.targets:
        prepared.extend(prepare_jobs(args.tb_dir, args.template, args.step, target))

    if args.execute:
        for run_dir in prepared:
            wrapper = run_dir / "run_ahc.sh"
            subprocess.run(
                ["bash", wrapper.name, "--num-cpus", str(args.num_cpus)],
                cwd=run_dir,
                check=True,
            )


if __name__ == "__main__":
    main()
