#!/usr/bin/env python3
"""Extract compact CSV data from vector manuscript PDFs.

This is a recovery utility for manuscript figures whose original compact CSV
files were not preserved. It reads the Matplotlib vector paths in the committed
paper PDFs and writes small CSV tables consumed by the repository plotting
scripts. The resulting CSVs are not a substitute for the original HDF5
workflows, but they preserve the numerical data embedded in the final plotted
figures.
"""

from __future__ import annotations

import argparse
import csv
import re
import zlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "figures" / "paper"
PROCESSED = ROOT / "data" / "processed"


def decompress_pdf(path: Path) -> str:
    """Return concatenated Flate-decoded PDF streams as Latin-1 text."""
    data = path.read_bytes()
    chunks: list[str] = []
    for match in re.finditer(rb"stream\r?\n(.*?)\r?\nendstream", data, re.S):
        try:
            chunks.append(zlib.decompress(match.group(1)).decode("latin1"))
        except zlib.error:
            continue
    return "\n".join(chunks)


def text_groups(stream: str) -> list[str]:
    """Extract simple text groups from PDF text objects."""
    groups: list[str] = []
    current: list[str] | None = None
    for line in stream.splitlines():
        if line == "BT":
            current = []
            continue
        if line == "ET":
            if current:
                groups.append("".join(current))
            current = None
            continue
        if current is None:
            continue
        for item in re.findall(r"\((.*?)\) Tj", line):
            current.append(item.replace(r"\(", "(").replace(r"\)", ")"))
        for item in re.findall(r"\[ \((.*?)\) \] TJ", line):
            current.append(item)
    return groups


def parse_bar_pdf(path: Path, value_scale: float, zero_y: float) -> list[dict[str, str]]:
    """Extract multipole coefficient bars and tick labels from one bar PDF."""
    stream = decompress_pdf(path)
    labels = [
        group
        for group in text_groups(stream)
        if group.startswith("z") and " " in group and "[" not in group
    ]
    rect_pattern = re.compile(
        r"(?P<x1>[0-9.]+) (?P<y1>[0-9.]+) m\n"
        r"(?P<x2>[0-9.]+) (?P=y1) l\n"
        r"(?P=x2) (?P<y2>[0-9.]+) l\n"
        r"(?P=x1) (?P=y2) l\nh\n\nf"
    )
    rects: list[tuple[float, float, float]] = []
    for match in rect_pattern.finditer(stream):
        x1 = float(match.group("x1"))
        y1 = float(match.group("y1"))
        y2 = float(match.group("y2"))
        if 50.0 < x1 < 450.0 and abs(y1 - zero_y) < 1.0:
            rects.append((x1, y1, y2))
    rects.sort(key=lambda item: item[0])
    if len(rects) != len(labels):
        raise ValueError(f"{path}: found {len(rects)} bars but {len(labels)} labels")

    rows: list[dict[str, str]] = []
    for label, (_, y1, y2) in zip(labels, rects, strict=True):
        index_text, name = label.split(" ", 1)
        y_tip = y2 if abs(y2 - zero_y) > abs(y1 - zero_y) else y1
        coefficient = (y_tip - zero_y) / value_scale
        rows.append(
            {
                "index": index_text.removeprefix("z"),
                "name": name,
                "coefficient_ev": f"{coefficient:.8f}",
                "abs_coefficient_ev": f"{abs(coefficient):.8f}",
                "source_pdf": path.name,
            }
        )
    return rows


def write_multipole_coefficients() -> None:
    """Write the recovered multipole coefficient CSV."""
    all_rows = parse_bar_pdf(PAPER / "bar_ed_all_35.pdf", 1.6032142625, 195.308501)
    non_q_rows = parse_bar_pdf(PAPER / "bar_ed_wo_q_35.pdf", 29.255477, 310.803114)
    merged: dict[str, dict[str, str]] = {row["index"]: row for row in all_rows}
    for row in non_q_rows:
        merged.setdefault(row["index"], row)

    out = PROCESSED / "multipole_coefficients" / "multipole_coefficients.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "index",
                "name",
                "coefficient_ev",
                "abs_coefficient_ev",
                "source_pdf",
            ],
        )
        writer.writeheader()
        writer.writerows(sorted(merged.values(), key=lambda row: int(row["index"])))


def line_paths(path: Path) -> list[list[tuple[float, float]]]:
    """Extract data line paths with 13 points from a minimal-model PDF."""
    stream = decompress_pdf(path)
    paths: list[list[tuple[float, float]]] = []
    point_line = re.compile(r"^([0-9.]+) ([0-9.]+) ([ml])$")
    for block in stream.split("\n\nS"):
        points: list[tuple[float, float]] = []
        for line in reversed(block.splitlines()):
            match = point_line.match(line)
            if match is None:
                if points:
                    break
                continue
            points.append((float(match.group(1)), float(match.group(2))))
        points.reverse()
        if len(points) == 13 and min(x for x, _ in points) >= 59.0:
            paths.append(points)
    return paths


def write_minimal_model() -> None:
    """Write compact minimal-model angular scans recovered from vector PDFs."""
    output = PROCESSED / "minimal_model" / "model_sigma_axis.csv"
    output.parent.mkdir(parents=True, exist_ok=True)
    angle_grid = list(range(0, 181, 15))
    rows: list[dict[str, str]] = []
    specs = [
        ("first_nn", PAPER / "sigma_axis_model_1st_nn.pdf", [0.0, 0.05, 0.1, 0.15, 0.2]),
        ("second_nn", PAPER / "sigma_axis_model_2nd_nn.pdf", [0.0, 0.1, 0.11, 0.12, 0.13, 0.14]),
    ]
    y_zero = 68.82
    y_scale = 10.745545
    for scan, path, parameters in specs:
        paths = line_paths(path)
        if len(paths) != len(parameters):
            raise ValueError(f"{path}: found {len(paths)} data paths")
        for parameter, points in zip(parameters, paths, strict=True):
            for phi, (_, y) in zip(angle_grid, points, strict=True):
                rows.append(
                    {
                        "scan": scan,
                        "parameter_value": f"{parameter:g}",
                        "phi_deg": str(phi),
                        "sigma_axis": f"{(y - y_zero) / y_scale:.8f}",
                        "source_pdf": path.name,
                    }
                )
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["scan", "parameter_value", "phi_deg", "sigma_axis", "source_pdf"],
        )
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    """Run the requested PDF-vector extraction steps."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--target",
        choices=["all", "multipole", "minimal-model"],
        default="all",
    )
    args = parser.parse_args()
    if args.target in {"all", "multipole"}:
        write_multipole_coefficients()
    if args.target in {"all", "minimal-model"}:
        write_minimal_model()


if __name__ == "__main__":
    main()
