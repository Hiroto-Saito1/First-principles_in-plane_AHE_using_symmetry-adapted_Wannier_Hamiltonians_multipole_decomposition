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
SOURCE = ROOT / "data" / "source"
PDF_VECTOR = SOURCE / "pdf_vector"
BAND_BOND_SOURCE = PDF_VECTOR / "band_bond"
PROCESSED = ROOT / "data" / "processed"

BAND_BOND_XMIN = 92.16
BAND_BOND_XMAX = 414.72
BAND_BOND_TICK_X = [92.16, 169.95466, 224.963265, 279.971869, 347.342045, 414.72]
BAND_BOND_Y_ZERO = 206.798109
BAND_BOND_Y_PER_EV = (240.554531 - BAND_BOND_Y_ZERO) / 2.0


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


def tokenize_pdf_stream(stream: str):
    """Yield coarse PDF content-stream tokens while skipping text payloads."""
    index = 0
    while index < len(stream):
        char = stream[index]
        if char.isspace():
            index += 1
            continue
        if char in "[]":
            yield char
            index += 1
            continue
        if char == "(":
            depth = 1
            index += 1
            while index < len(stream) and depth:
                char = stream[index]
                if char == "\\":
                    index += 2
                    continue
                if char == "(":
                    depth += 1
                elif char == ")":
                    depth -= 1
                index += 1
            yield "STRING"
            continue
        end = index
        while end < len(stream) and not stream[end].isspace() and stream[end] not in "[]()":
            end += 1
        yield stream[index:end]
        index = end


def stroked_subpaths(path: Path) -> list[dict[str, object]]:
    """Extract stroked polyline subpaths with their stroke style."""
    stream = decompress_pdf(path)
    operators = {
        "m",
        "l",
        "c",
        "S",
        "s",
        "f",
        "B",
        "BT",
        "ET",
        "q",
        "Q",
        "cm",
        "w",
        "RG",
        "G",
        "d",
        "J",
        "j",
        "gs",
        "Do",
        "re",
        "n",
        "W",
        "cs",
        "CS",
        "Tf",
        "Td",
        "Tj",
        "TJ",
        "h",
    }
    stack: list[str] = []
    state = {"width": 1.0, "stroke": ("gray", 0.0), "dash": ()}
    subpaths: list[list[tuple[float, float]]] = []
    current: list[tuple[float, float]] = []
    extracted: list[dict[str, object]] = []

    def flush_subpath() -> None:
        nonlocal current
        if current:
            subpaths.append(current)
            current = []

    def flush_stroke() -> None:
        flush_subpath()
        for points in subpaths:
            xs = [point[0] for point in points]
            ys = [point[1] for point in points]
            extracted.append(
                {
                    "points": points,
                    "style": (state["stroke"], state["width"], state["dash"]),
                    "xmin": min(xs),
                    "xmax": max(xs),
                    "ymin": min(ys),
                    "ymax": max(ys),
                }
            )
        subpaths.clear()

    for token in tokenize_pdf_stream(stream):
        if token == "STRING":
            continue
        if token == "]":
            stack.append(token)
            continue
        if token not in operators:
            stack.append(token)
            continue

        if token == "w":
            while stack and stack[-1] in {"[", "]"}:
                stack.pop()
            state["width"] = float(stack.pop())
            continue
        if token == "RG":
            blue = float(stack.pop())
            green = float(stack.pop())
            red = float(stack.pop())
            state["stroke"] = (red, green, blue)
            continue
        if token == "G":
            state["stroke"] = ("gray", float(stack.pop()))
            continue
        if token == "d":
            if stack:
                stack.pop()
            dash = []
            while stack:
                item = stack.pop()
                if item == "[":
                    break
                if item == "]":
                    continue
                dash.append(float(item))
            dash.reverse()
            state["dash"] = tuple(dash)
            continue
        if token == "m":
            flush_subpath()
            y = float(stack.pop())
            x = float(stack.pop())
            current = [(x, y)]
            continue
        if token == "l":
            y = float(stack.pop())
            x = float(stack.pop())
            current.append((x, y))
            continue
        if token == "c":
            y3 = float(stack.pop())
            x3 = float(stack.pop())
            for _ in range(4):
                stack.pop()
            current.append((x3, y3))
            continue
        if token == "S":
            flush_stroke()
            continue
        if token in {"s", "f", "B", "n"}:
            current = []
            subpaths.clear()

    return extracted


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


def write_band_bond() -> None:
    """Write compact band-curve CSV rows recovered from per-cutoff vector PDFs."""
    output = PROCESSED / "band_bond" / "band_bond_curves.csv"
    output.parent.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, str]] = []
    for path in sorted(BAND_BOND_SOURCE.glob("band_*.pdf")):
        cutoff = int(path.stem.split("_")[1])
        counters = {"DFT": 0, "model": 0}
        for item in stroked_subpaths(path):
            stroke, width, dash = item["style"]
            x_span = item["xmax"] - item["xmin"]
            if width != 1.5 or x_span < 40.0:
                continue
            if stroke == (1.0, 0.0, 0.0) and dash:
                series = "model"
            elif stroke == ("gray", 0.0) and not dash:
                series = "DFT"
            else:
                continue
            curve_index = counters[series]
            counters[series] += 1
            points = item["points"]
            for point_index, (x_coord, y_coord) in enumerate(points):
                rows.append(
                    {
                        "cutoff_shell": str(cutoff),
                        "series": series,
                        "curve_index": str(curve_index),
                        "point_index": str(point_index),
                        "k_path_fraction": f"{(x_coord - BAND_BOND_XMIN) / (BAND_BOND_XMAX - BAND_BOND_XMIN):.8f}",
                        "energy_ev": f"{(y_coord - BAND_BOND_Y_ZERO) / BAND_BOND_Y_PER_EV:.8f}",
                        "source_pdf": path.name,
                    }
                )

    rows.sort(
        key=lambda row: (
            int(row["cutoff_shell"]),
            row["series"],
            int(row["curve_index"]),
            int(row["point_index"]),
        )
    )
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "cutoff_shell",
                "series",
                "curve_index",
                "point_index",
                "k_path_fraction",
                "energy_ev",
                "source_pdf",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    """Run the requested PDF-vector extraction steps."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--target",
        choices=["all", "multipole", "minimal-model", "band-bond"],
        default="all",
    )
    args = parser.parse_args()
    if args.target in {"all", "multipole"}:
        write_multipole_coefficients()
    if args.target in {"all", "minimal-model"}:
        write_minimal_model()
    if args.target in {"all", "band-bond"}:
        write_band_bond()


if __name__ == "__main__":
    main()
