#!/usr/bin/env python3
"""Plot multipole coefficient bars from a compact coefficient CSV."""

from __future__ import annotations

import argparse
from pathlib import Path

from _common import DEFAULT_OUTPUT, PROCESSED, get_pyplot, parse_float, read_csv


def select_rows(rows, exclude_q: bool) -> list[dict[str, str]]:
    if exclude_q:
        rows = [row for row in rows if not row["name"].startswith("Q")]
    return sorted(rows, key=lambda row: abs(parse_float(row["coefficient_ev"])), reverse=True)[:20]


def plot(rows, output: Path, title: str) -> None:
    plt = get_pyplot()
    output.parent.mkdir(parents=True, exist_ok=True)
    colors = []
    for row in rows:
        name = row["name"]
        colors.append({"Q": "orange", "M": "tab:blue", "T": "tab:pink", "G": "tab:green"}.get(name[:1], "gray"))
    labels = [f"z_{row['index']} {row['name']}" for row in rows]
    values = [parse_float(row["coefficient_ev"]) for row in rows]
    plt.figure(figsize=(7.0, 4.0))
    plt.bar(range(len(rows)), values, color=colors)
    plt.xticks(range(len(rows)), labels, rotation=90, fontsize=7)
    plt.ylabel("z_i [eV]")
    plt.title(title)
    plt.grid(axis="y", linewidth=0.4)
    plt.tight_layout()
    plt.savefig(output)
    plt.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=PROCESSED / "multipole_coefficients" / "multipole_coefficients.csv")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT / "multipole_coefficients")
    args = parser.parse_args()

    if not args.input.is_file():
        raise SystemExit(
            "Missing compact coefficient CSV. See "
            "data/processed/multipole_coefficients/README.md and "
            "scripts/workflow/generate_large_files.md."
        )
    rows = read_csv(args.input)
    plot(select_rows(rows, exclude_q=False), args.output_dir / "bar_ed_all_35.pdf", "Top multipole coefficients")
    plot(select_rows(rows, exclude_q=True), args.output_dir / "bar_ed_wo_q_35.pdf", "Top non-electric multipole coefficients")


if __name__ == "__main__":
    main()
