#!/usr/bin/env python3
"""Export a compact fit_ahc CSV from archived XML or compact CSV sources."""

from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path
import xml.etree.ElementTree as ET


AHC_FIELDS = [
    "sigma_xy",
    "sigma_yz",
    "sigma_zx",
    "sigma_para",
    "sigma_perp",
    "sigma_axis",
]


def parse_float(text: str | None) -> float:
    if text is None:
        return math.nan
    text = text.strip()
    if text.lower() == "nan":
        return math.nan
    return float(text)


def format_float(value: float) -> str:
    if math.isnan(value):
        return "nan"
    return f"{value:.10f}"


def read_ahc_xml(path: Path, *, plane: str, series_group: str) -> list[dict[str, str]]:
    root = ET.parse(path).getroot()
    rows: list[dict[str, str]] = []
    for method in root.findall("method"):
        label = method.attrib["label"]
        for angle in method.findall("angle"):
            row = {
                "plane": plane,
                "series_group": series_group,
                "method": label,
                "phi_deg": format_float(parse_float(angle.attrib.get("phi"))),
            }
            for field in AHC_FIELDS:
                row[f"{field}_s_cm"] = format_float(parse_float(angle.findtext(field)))
            rows.append(row)
    return rows


def read_ahc_csv(
    path: Path,
    *,
    plane: str,
    series_group: str,
    select_method: str,
    rename_method: str | None = None,
) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    exported: list[dict[str, str]] = []
    for row in rows:
        if row["method"] != select_method:
            continue
        exported.append(
            {
                "plane": plane,
                "series_group": series_group,
                "method": rename_method or row["method"],
                "phi_deg": row["phi_deg"],
                **{f"{field}_s_cm": row[f"{field}_s_cm"] for field in AHC_FIELDS},
            }
        )
    return exported


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["plane", "series_group", "method", "phi_deg"] + [
        f"{field}_s_cm" for field in AHC_FIELDS
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--xml", type=Path, help="Archived angle_dep_ahc.xml input.")
    source.add_argument(
        "--csv",
        type=Path,
        help="Committed compact AHC CSV input used to derive a fit_ahc overlay source.",
    )
    parser.add_argument("--plane", required=True, help="Rotation plane label, e.g. 103.")
    parser.add_argument(
        "--series-group",
        default="fit_ahc_model",
        help="series_group value stored in the compact CSV.",
    )
    parser.add_argument(
        "--select-method",
        help="Method label to keep when exporting from --csv (for example SW+ED).",
    )
    parser.add_argument(
        "--rename-method",
        help="Optional replacement method label written to the compact CSV.",
    )
    parser.add_argument("--output", type=Path, required=True, help="Output CSV path.")
    args = parser.parse_args()

    if args.xml is not None:
        rows = read_ahc_xml(args.xml, plane=args.plane, series_group=args.series_group)
    else:
        if not args.select_method:
            raise SystemExit("--select-method is required when exporting from --csv")
        rows = read_ahc_csv(
            args.csv,
            plane=args.plane,
            series_group=args.series_group,
            select_method=args.select_method,
            rename_method=args.rename_method,
        )
    write_csv(args.output, rows)
    print(f"Wrote {len(rows)} rows to {args.output}")


if __name__ == "__main__":
    main()
