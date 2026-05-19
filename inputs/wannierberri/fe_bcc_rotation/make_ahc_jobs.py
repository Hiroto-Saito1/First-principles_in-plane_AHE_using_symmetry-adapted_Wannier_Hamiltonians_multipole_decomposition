#!/usr/bin/env python3
"""Create local per-angle WannierBerri AHC run folders.

The helper scans for rotated Fe tight-binding files named
`trs_py_ed_phi*_tb.dat`, `trs_py_pd_phi*_tb.dat`, or `trs_tb_phi*_tb.dat` and
writes a small `run_ahc.sh` wrapper for each selected angle.
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


PREFIXES = {
    "trs_py_ed_phi": "ed_phi",
    "trs_py_pd_phi": "pd_phi",
    "trs_tb_phi": "tb_phi",
}


def parse_phi(path: Path) -> tuple[str, int] | None:
    """Return the workflow prefix and angle encoded in a rotated TB filename."""
    name = path.name
    for file_prefix, job_prefix in PREFIXES.items():
        if not name.startswith(file_prefix) or not name.endswith("_tb.dat"):
            continue
        phi_text = name.removeprefix(file_prefix).removesuffix("_tb.dat")
        try:
            return job_prefix, int(phi_text)
        except ValueError:
            return None
    return None


def selected(phi: int, step: int) -> bool:
    """Select the AHC summary angles used by the manuscript plots."""
    return 0 <= phi <= 180 and phi % step == 0


def prepare_jobs(tb_dir: Path, template: Path, step: int, target: str) -> list[Path]:
    """Create local per-angle AHC run folders and return the prepared directories."""

    if not template.is_file():
        raise FileNotFoundError(f"Missing AHC template: {template}")

    prepared: list[Path] = []
    for tb_file in sorted(tb_dir.glob("*_phi*_tb.dat")):
        parsed = parse_phi(tb_file)
        if parsed is None:
            continue
        prefix, phi = parsed
        if prefix != target or not selected(phi, step):
            continue

        run_dir = tb_dir / f"{prefix}{phi}"
        run_dir.mkdir(exist_ok=True)
        shutil.copy2(template, run_dir / "ahc_template.py")
        wrapper = run_dir / "run_ahc.sh"
        wrapper.write_text(
            "#!/usr/bin/env bash\n"
            "set -euo pipefail\n"
            f"python ahc_template.py ../{tb_file.name} \"$@\"\n",
            encoding="utf-8",
        )
        wrapper.chmod(0o755)
        prepared.append(run_dir)
        print(f"Prepared {run_dir}")

    return prepared


def main() -> None:
    """Create job folders without submitting them to a cluster scheduler."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tb-dir", type=Path, default=Path("."))
    parser.add_argument(
        "--template",
        type=Path,
        default=Path(__file__).with_name("ahc_template.py"),
    )
    parser.add_argument("--step", type=int, default=5)
    parser.add_argument("--target", choices=["ed_phi", "pd_phi", "tb_phi"], default="ed_phi")
    args = parser.parse_args()
    prepare_jobs(args.tb_dir, args.template, args.step, args.target)


if __name__ == "__main__":
    main()
