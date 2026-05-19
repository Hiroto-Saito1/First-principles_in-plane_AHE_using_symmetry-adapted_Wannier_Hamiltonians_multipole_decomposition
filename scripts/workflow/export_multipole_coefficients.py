#!/usr/bin/env python3
"""Export compact multipole-coefficient CSV tables from a decomposition HDF5."""

from __future__ import annotations

import argparse
import csv
import gzip
from pathlib import Path
import sys
from typing import Any

import h5py
import numpy as np


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))


def open_text_or_gzip(path: Path):
    if path.is_file():
        return open(path, "rt", encoding="utf-8")
    gz_path = path.with_suffix(path.suffix + ".gz")
    if gz_path.is_file():
        return gzip.open(gz_path, "rt", encoding="utf-8")
    raise FileNotFoundError(path)


def load_samb_dict(path: Path) -> dict[str, Any]:
    with open_text_or_gzip(path) as handle:
        code = handle.read()
    namespace: dict[str, Any] = {}
    exec(code, namespace)
    candidates = {
        name: value
        for name, value in namespace.items()
        if not name.startswith("__") and isinstance(value, dict) and value
    }
    if len(candidates) != 1:
        raise ValueError(
            f"Expected exactly one non-empty dictionary in {path}, found {list(candidates)}."
        )
    return next(iter(candidates.values()))


def parse_label(entry: Any) -> str:
    if isinstance(entry, tuple) and entry:
        return str(entry[0])
    return str(entry)


def normalize_index(key: Any) -> str:
    text = str(key)
    if text.startswith("z_"):
        return text[2:]
    if text.startswith("z"):
        return text[1:]
    return text


def load_entries(multi_path: Path, samb_path: Path) -> list[dict[str, str | float]]:
    samb = load_samb_dict(samb_path)
    z_dict = samb["data"]["Z"]
    with h5py.File(multi_path, "r") as h5:
        coefficients = h5["z_coefficients"][:]
    if len(z_dict) != len(coefficients):
        raise ValueError(
            f"Coefficient count mismatch: samb has {len(z_dict)} labels, "
            f"HDF5 has {len(coefficients)} coefficients."
        )

    entries: list[dict[str, str | float]] = []
    for (key, label_entry), coefficient in zip(z_dict.items(), coefficients, strict=True):
        entries.append(
            {
                "index": normalize_index(key),
                "name": parse_label(label_entry),
                "coefficient_ev": float(np.real(coefficient)),
                "abs_coefficient_ev": float(abs(np.real(coefficient))),
                "imag_coefficient_ev": float(np.imag(coefficient)),
            }
        )
    return entries


def merged_bar_entries(entries: list[dict[str, str | float]], top: int) -> list[dict[str, str | float]]:
    ranked = sorted(entries, key=lambda entry: float(entry["abs_coefficient_ev"]), reverse=True)
    merged: dict[str, dict[str, str | float]] = {}
    for selection, subset in [
        (f"all_top{top}", ranked[:top]),
        (
            f"non_q_top{top}",
            [entry for entry in ranked if not str(entry["name"]).startswith("Q")][:top],
        ),
    ]:
        for entry in subset:
            key = str(entry["index"])
            if key not in merged:
                merged[key] = {**entry, "selection": selection}
            else:
                merged[key]["selection"] = f"{merged[key]['selection']};{selection}"
    return sorted(merged.values(), key=lambda entry: str(entry["index"]))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--multi-path", type=Path, required=True, help="Decomposition HDF5 with z_coefficients.")
    parser.add_argument("--samb-path", type=Path, required=True, help="Fe_samb.py or Fe_samb.py.gz.")
    parser.add_argument("--output", type=Path, required=True, help="Output CSV path.")
    parser.add_argument(
        "--mode",
        choices=["all", "bar-merged"],
        default="bar-merged",
        help="Export all coefficients or the manuscript bar-plot merged top list.",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=20,
        help="Number of coefficients used for each bar-plot selection in bar-merged mode.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    entries = load_entries(args.multi_path, args.samb_path)
    if args.mode == "bar-merged":
        entries = merged_bar_entries(entries, args.top)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "index",
                "name",
                "coefficient_ev",
                "abs_coefficient_ev",
                "imag_coefficient_ev",
                "selection",
                "source_hdf5",
                "source_samb",
            ],
        )
        writer.writeheader()
        for entry in entries:
            row = {
                "index": str(entry["index"]),
                "name": str(entry["name"]),
                "coefficient_ev": f"{float(entry['coefficient_ev']):.8f}",
                "abs_coefficient_ev": f"{float(entry['abs_coefficient_ev']):.8f}",
                "imag_coefficient_ev": f"{float(entry['imag_coefficient_ev']):.8f}",
                "selection": str(entry.get("selection", "all")),
                "source_hdf5": args.multi_path.name,
                "source_samb": args.samb_path.name,
            }
            writer.writerow(row)
    print(f"Wrote {args.output} ({len(entries)} rows)")


if __name__ == "__main__":
    main()
