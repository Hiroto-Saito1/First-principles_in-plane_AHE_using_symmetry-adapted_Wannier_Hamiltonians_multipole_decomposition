#!/usr/bin/env python3
"""Replot compact rank-cumulative and single-rank Fe (103) AHC data."""

from __future__ import annotations

import argparse
from pathlib import Path

from _common import (
    DEFAULT_OUTPUT_DIAGNOSTICS,
    DEFAULT_OUTPUT_PAPER,
    PROCESSED,
    get_pyplot,
    read_csv,
    require_file,
    sorted_xy,
)


GROUPS = [
    ["w_rank1", "w_rank1_2"],
    ["w_rank1_2_3", "w_rank1_2_3_4"],
    ["w_rank1_2_3_4_5", "w_rank1_2_3_4_5_6"],
]
SINGLE_RANK_METHODS = ["w_rank1", "w_rank3", "w_rank4", "w_rank5"]

PAPER_COMPONENT_LABELS = {
    "para": r"$\sigma_{\parallel}\ [\mathrm{S/cm}]$",
    "perp": r"$\sigma_{\perp}\ [\mathrm{S/cm}]$",
    "axis": r"$\sigma_{n}\ [\mathrm{S/cm}]$",
}

PAPER_CUMULATIVE_LABELS = {
    "w_rank1": "w/ rank 1",
    "w_rank1_2": "w/ rank 1,2",
    "w_rank1_2_3": "w/ rank 1,2,3",
    "w_rank1_2_3_4": "w/ rank 1,2,3,4",
    "w_rank1_2_3_4_5": "w/ rank 1,2,3,4,5",
    "w_rank1_2_3_4_5_6": "w/ rank 1,2,3,4,5,6",
}

PAPER_SINGLE_RANK_LABELS = {
    "w_rank1": "w/ rank 1",
    "w_rank3": "w/ rank 3",
    "w_rank4": "w/ rank 4",
    "w_rank5": "w/ rank 5",
}

PAPER_STYLE_MAP = {
    "w_rank1": {"marker": "s", "linestyle": "-", "color": "tab:blue"},
    "w_rank1_2": {"marker": "P", "linestyle": "--", "color": "tab:orange"},
    "w_rank1_2_3": {"marker": "s", "linestyle": "-", "color": "tab:blue"},
    "w_rank1_2_3_4": {"marker": "P", "linestyle": "--", "color": "tab:orange"},
    "w_rank1_2_3_4_5": {"marker": "s", "linestyle": "-", "color": "tab:blue"},
    "w_rank1_2_3_4_5_6": {"marker": "P", "linestyle": "--", "color": "tab:orange"},
    "w_rank3": {"marker": "^", "linestyle": "-.", "color": "tab:green"},
    "w_rank4": {"marker": "D", "linestyle": ":", "color": "tab:purple"},
    "w_rank5": {"marker": "v", "linestyle": "-", "color": "tab:brown"},
}

PAPER_REFERENCE_STYLE = {
    "color": "tab:red",
    "marker": "*",
    "linestyle": "-",
    "alpha": 0.7,
    "markersize": 8,
    "linewidth": 2.5,
}


def output_dir_for(style: str) -> Path:
    if style == "paper":
        return DEFAULT_OUTPUT_PAPER / "rank_resolved_103"
    if style == "diagnostic":
        return DEFAULT_OUTPUT_DIAGNOSTICS / "rank_resolved_103"
    raise ValueError(style)


def display_label(method: str, *, style: str, single_rank: bool) -> str:
    if style == "paper":
        if single_rank:
            return PAPER_SINGLE_RANK_LABELS.get(method, method)
        return PAPER_CUMULATIVE_LABELS.get(method, method)
    if single_rank:
        return method.replace("_", " ")
    return method.replace("_", ",")


def component_ylabel(component: str, *, style: str) -> str:
    if style == "paper":
        return PAPER_COMPONENT_LABELS[component]
    return f"sigma_{component} at E_F [S/cm]"


def reference_label(style: str) -> str:
    return "all" if style == "paper" else "all"


def plot_component(rows, methods, component: str, output: Path, *, style: str) -> None:
    plt = get_pyplot()
    output.parent.mkdir(parents=True, exist_ok=True)
    by_key = {(row["series_group"], row["method"]): [] for row in rows}
    for row in rows:
        by_key[(row["series_group"], row["method"])].append(row)

    plt.figure(figsize=(5.2, 3.8))
    for method in methods:
        series = by_key.get(("rank_cumulative", method), [])
        if not series:
            continue
        x, y = sorted_xy(series, component)
        kwargs = {"marker": "o", "markersize": 3, "linewidth": 1.2}
        kwargs.update(PAPER_STYLE_MAP.get(method, {}) if style == "paper" else {})
        plt.plot(x, y, label=display_label(method, style=style, single_rank=False), **kwargs)
    reference = by_key.get(("reference", "SW+ED"), [])
    if reference:
        x, y = sorted_xy(reference, component)
        ref_kwargs = {
            "color": "black",
            "marker": "*",
            "markersize": 5,
            "linewidth": 1.5,
        }
        if style == "paper":
            ref_kwargs.update(PAPER_REFERENCE_STYLE)
        plt.plot(x, y, label=reference_label(style), **ref_kwargs)
    plt.xlabel(r"$\psi\ [\mathrm{deg}]$" if style == "paper" else "psi [deg]")
    plt.ylabel(component_ylabel(component, style=style))
    plt.xlim(0, 180)
    plt.xticks(range(0, 181, 30))
    plt.grid(True, linewidth=0.4)
    plt.legend(fontsize=7)
    plt.tight_layout()
    plt.savefig(output)
    plt.close()


def plot_single_rank(rows, component: str, output: Path, *, style: str) -> None:
    plt = get_pyplot()
    output.parent.mkdir(parents=True, exist_ok=True)
    by_key = {(row["series_group"], row["method"]): [] for row in rows}
    for row in rows:
        by_key[(row["series_group"], row["method"])].append(row)

    plt.figure(figsize=(5.2, 3.8))
    for method in SINGLE_RANK_METHODS:
        series = by_key.get(("single_rank", method), [])
        if not series:
            continue
        x, y = sorted_xy(series, component)
        kwargs = {"marker": "o", "markersize": 3, "linewidth": 1.2}
        kwargs.update(PAPER_STYLE_MAP.get(method, {}) if style == "paper" else {})
        plt.plot(x, y, label=display_label(method, style=style, single_rank=True), **kwargs)
    reference = by_key.get(("reference", "SW+ED"), [])
    if reference:
        x, y = sorted_xy(reference, component)
        ref_kwargs = {
            "color": "black",
            "marker": "*",
            "markersize": 5,
            "linewidth": 1.5,
        }
        if style == "paper":
            ref_kwargs.update(PAPER_REFERENCE_STYLE)
        plt.plot(x, y, label=reference_label(style), **ref_kwargs)
    plt.xlabel(r"$\psi\ [\mathrm{deg}]$" if style == "paper" else "psi [deg]")
    plt.ylabel(component_ylabel(component, style=style))
    plt.xlim(0, 180)
    plt.xticks(range(0, 181, 30))
    plt.grid(True, linewidth=0.4)
    plt.legend(fontsize=7)
    plt.tight_layout()
    plt.savefig(output)
    plt.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--style", choices=("paper", "diagnostic"), default="paper")
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()

    output_dir = args.output_dir or output_dir_for(args.style)
    rows = read_csv(require_file(PROCESSED / "rank_resolved_103" / "rank_resolved_ahc.csv"))
    components = ["para", "perp", "axis"]
    for idx, methods in enumerate(GROUPS, start=1):
        for component in components:
            plot_component(
                rows,
                methods,
                component,
                output_dir / f"sigma_{component}_group{idx}.pdf",
                style=args.style,
            )

    single_rank_path = PROCESSED / "rank_resolved_103" / "single_rank_ahc.csv"
    if single_rank_path.is_file():
        single_rank_rows = read_csv(single_rank_path)
        for component in components:
            plot_single_rank(
                single_rank_rows,
                component,
                output_dir / f"sigma_{component}.pdf",
                style=args.style,
            )


if __name__ == "__main__":
    main()
