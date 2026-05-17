from __future__ import annotations

import csv
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]


def manuscript_figure_files() -> list[str]:
    text = (ROOT / "main_all.tex").read_text(encoding="utf-8")
    return re.findall(r"\\includegraphics(?:\[[^\]]+\])?\{([^}]+\.pdf)\}", text)


def test_all_manuscript_figures_are_committed() -> None:
    figures = manuscript_figure_files()
    assert len(figures) == 35
    missing = [name for name in figures if not (ROOT / "figures" / "paper" / name).is_file()]
    assert missing == []


def test_figure_inventory_matches_manuscript() -> None:
    figures = set(manuscript_figure_files())
    with (ROOT / "data" / "processed" / "figure_inventory.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert {row["figure_file"] for row in rows} == figures
    assert len(rows) == len(figures)
    for row in rows:
        assert (ROOT / row["included_pdf"]).is_file()
        assert (ROOT / row["processed_data"]).exists()
        assert (ROOT / row["plotting_script"]).exists()
        assert row["reproducibility_level"] in {"1", "2", "3"}


def test_committed_paper_figures_are_small() -> None:
    limit = 100 * 1024 * 1024
    oversized = [
        path
        for path in (ROOT / "figures" / "paper").glob("*.pdf")
        if path.stat().st_size > limit
    ]
    assert oversized == []
