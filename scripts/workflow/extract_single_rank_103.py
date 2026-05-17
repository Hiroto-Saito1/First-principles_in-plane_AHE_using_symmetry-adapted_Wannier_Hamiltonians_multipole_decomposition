#!/usr/bin/env python3
"""Extract compact single-rank Fe (103) AHC data from workflow XML files."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
import xml.etree.ElementTree as ET


COMPONENTS = [
    "sigma_xy",
    "sigma_yz",
    "sigma_zx",
    "sigma_para",
    "sigma_perp",
    "sigma_axis",
]


def parse_angle_dep_xml(path: Path, *, series_group: str) -> list[dict[str, str]]:
    """Read an `angle_dep_ahc.xml` file and return normalized CSV rows."""
    tree = ET.parse(path)
    root = tree.getroot()
    rows: list[dict[str, str]] = []
    for method in root.findall("method"):
        label = method.attrib["label"]
        for angle in method.findall("angle"):
            row = {
                "plane": "103",
                "series_group": series_group,
                "method": label,
                "phi_deg": angle.attrib["phi"],
            }
            for component in COMPONENTS:
                value = angle.findtext(component)
                row[f"{component}_s_cm"] = "nan" if value is None else value
            rows.append(row)
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--single-rank-xml",
        type=Path,
        required=True,
        help="XML containing w_rank1, w_rank3, w_rank4, and w_rank5 single-rank AHC data.",
    )
    parser.add_argument(
        "--reference-xml",
        type=Path,
        required=True,
        help="XML containing the all-component SW+ED reference curve.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/processed/rank_resolved_103/single_rank_ahc.csv"),
    )
    args = parser.parse_args()

    rows = parse_angle_dep_xml(args.single_rank_xml, series_group="single_rank")
    reference_rows = [
        row
        for row in parse_angle_dep_xml(args.reference_xml, series_group="reference")
        if row["method"] == "SW+ED"
    ]
    rows.extend(reference_rows)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "plane",
        "series_group",
        "method",
        "phi_deg",
        "sigma_xy_s_cm",
        "sigma_yz_s_cm",
        "sigma_zx_s_cm",
        "sigma_para_s_cm",
        "sigma_perp_s_cm",
        "sigma_axis_s_cm",
    ]
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
