#!/usr/bin/env python3
"""Plot multipole coefficient bars from a compact coefficient CSV."""

from __future__ import annotations

import argparse
from pathlib import Path
import re

from matplotlib.patches import Patch

from _common import (
    DEFAULT_OUTPUT_DIAGNOSTICS,
    DEFAULT_OUTPUT_PAPER,
    PROCESSED,
    get_pyplot,
    parse_float,
    read_csv,
)


FAMILY_COLORS = {
    "Q": "#d97706",
    "M": "#2563eb",
    "T": "#db2777",
    "G": "#059669",
}

FAMILY_LABELS = {
    "Q": "Q electric",
    "M": "M magnetic",
    "T": "T magnetic-toroidal",
    "G": "G electric-toroidal",
}

NAME_RE = re.compile(r"(?P<family>[QMTG])\((?P<rank>[^,]+),(?P<irrep>[^,]+),")


def select_rows(rows, exclude_q: bool) -> list[dict[str, str]]:
    if exclude_q:
        rows = [row for row in rows if not row["name"].startswith("Q")]
    return sorted(rows, key=lambda row: abs(parse_float(row["coefficient_ev"])), reverse=True)[:20]


def output_dir_for(style: str) -> Path:
    if style == "paper":
        return DEFAULT_OUTPUT_PAPER / "multipole_coefficients"
    if style == "diagnostic":
        return DEFAULT_OUTPUT_DIAGNOSTICS / "multipole_coefficients"
    raise ValueError(style)


def family_code(name: str) -> str:
    return name[:1]


def parse_name(name: str) -> tuple[str, str, str]:
    match = NAME_RE.match(name)
    if not match:
        return family_code(name), "?", name
    return match.group("family"), match.group("rank"), match.group("irrep")


def paper_label(row: dict[str, str]) -> str:
    family, rank, irrep = parse_name(row["name"])
    return f"z_{row['index']}\n{family}{rank} {irrep}"


def diagnostic_label(row: dict[str, str]) -> str:
    return f"z_{row['index']} {row['name']}"


def plot(rows, output: Path, title: str | None, *, style: str) -> None:
    plt = get_pyplot()
    output.parent.mkdir(parents=True, exist_ok=True)
    colors = [FAMILY_COLORS.get(family_code(row["name"]), "gray") for row in rows]
    if style == "paper":
        labels = [paper_label(row) for row in rows]
    else:
        labels = [diagnostic_label(row) for row in rows]
    values = [parse_float(row["coefficient_ev"]) for row in rows]
    positions = list(range(len(rows)))
    plt.figure(figsize=(7.4, 4.6) if style == "paper" else (7.8, 4.8))
    plt.bar(positions, values, color=colors, edgecolor="black", linewidth=0.35)
    plt.axhline(0.0, color="black", linewidth=0.8)
    plt.xticks(positions, labels, rotation=70 if style == "paper" else 90, ha="right", fontsize=7)
    plt.ylabel("coefficient [eV]" if style == "paper" else "z_i [eV]")
    if title:
        plt.title(title)
    plt.grid(axis="y", linewidth=0.4)
    if style == "paper":
        families = []
        for row in rows:
            code = family_code(row["name"])
            if code not in families:
                families.append(code)
        handles = [
            Patch(facecolor=FAMILY_COLORS[code], edgecolor="black", label=FAMILY_LABELS[code])
            for code in families
        ]
        plt.legend(handles=handles, ncols=min(2, len(handles)), fontsize=7, frameon=False, loc="upper right")
    plt.tight_layout()
    plt.savefig(output)
    plt.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--style", choices=("paper", "diagnostic"), default="paper")
    parser.add_argument("--input", type=Path, default=PROCESSED / "multipole_coefficients" / "multipole_coefficients.csv")
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()

    if not args.input.is_file():
        raise SystemExit(
            "Missing compact coefficient CSV. See "
            "data/processed/multipole_coefficients/README.md and "
            "scripts/workflow/generate_large_files.md."
        )
    output_dir = args.output_dir or output_dir_for(args.style)
    rows = read_csv(args.input)
    plot(
        select_rows(rows, exclude_q=False),
        output_dir / "bar_ed_all_35.pdf",
        None if args.style == "paper" else "Top multipole coefficients",
        style=args.style,
    )
    plot(
        select_rows(rows, exclude_q=True),
        output_dir / "bar_ed_wo_q_35.pdf",
        None if args.style == "paper" else "Top non-electric multipole coefficients",
        style=args.style,
    )


if __name__ == "__main__":
    main()
