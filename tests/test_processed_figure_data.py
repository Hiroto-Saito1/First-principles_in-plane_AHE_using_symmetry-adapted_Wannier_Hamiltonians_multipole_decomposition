"""Regression tests for compact processed data behind manuscript figures."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"


def rows(path: Path) -> list[dict[str, str]]:
    """Read a processed CSV file as dictionaries keyed by column name."""
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def as_float(value: str) -> float:
    """Convert a CSV field to float for numerical regression checks."""
    return float(value)


def select(rows_: list[dict[str, str]], **matches: str) -> dict[str, str]:
    """Select exactly one processed-data row matching the requested field values."""
    hits = [
        row
        for row in rows_
        if all(row[key] == value for key, value in matches.items())
    ]
    assert len(hits) == 1
    return hits[0]


def test_primary_ahc_csv_shapes_and_reference_values() -> None:
    """Check primary `(111)` and `(103)` AHC CSV sizes, labels, and reference values."""
    ahc_111 = rows(PROCESSED / "ahc_111" / "ahc_angle_dependence.csv")
    ahc_103 = rows(PROCESSED / "ahc_103" / "ahc_angle_dependence.csv")
    assert len(ahc_111) == 39
    assert len(ahc_103) == 39
    assert {row["method"] for row in ahc_111} == {"Wan90", "SW+ED", "SW+PD"}
    assert {row["method"] for row in ahc_103} == {"Wan90", "SW+ED", "SW+PD"}

    row_111 = select(ahc_111, method="SW+ED", phi_deg="0.0")
    assert abs(as_float(row_111["sigma_axis_s_cm"]) - 46.9439462426) < 1e-9
    row_103 = select(ahc_103, method="SW+ED", phi_deg="0.0")
    assert abs(as_float(row_103["sigma_zx_s_cm"]) - 785.6033) < 1e-9


def test_rank_resolved_data_cover_expected_cumulative_series() -> None:
    """Verify that rank-cumulative `(103)` data include all expected cumulative series."""
    data = rows(PROCESSED / "rank_resolved_103" / "rank_resolved_ahc.csv")
    cumulative = [row for row in data if row["series_group"] == "rank_cumulative"]
    assert len(cumulative) == 117
    assert {
        row["method"]
        for row in cumulative
    } == {
        "w_rank1",
        "w_rank1_2",
        "w_rank1_2_3",
        "w_rank1_2_3_4",
        "w_rank1_2_3_4_5",
        "w_rank1_2_3_4_5_6",
        "w_rank1_2_3_4_5_6_7",
        "w_rank1_2_3_4_5_6_7_8",
        "w_rankNone",
    }
    row = select(cumulative, method="w_rank1", phi_deg="90.0")
    assert abs(as_float(row["sigma_axis_s_cm"]) - 207.3349877712) < 1e-9


def test_single_rank_data_cover_expected_rank_series() -> None:
    """Verify that single-rank `(103)` AHC data include rank-only and reference series."""
    data = rows(PROCESSED / "rank_resolved_103" / "single_rank_ahc.csv")
    single_rank = [row for row in data if row["series_group"] == "single_rank"]
    reference = [row for row in data if row["series_group"] == "reference"]
    assert len(single_rank) == 65
    assert len(reference) == 37
    assert {row["method"] for row in single_rank} == {
        "w_rank1",
        "w_rank3",
        "w_rank4",
        "w_rank5",
        "w_rankNone",
    }
    assert {row["method"] for row in reference} == {"SW+ED"}
    row = select(single_rank, method="w_rank4", phi_deg="90")
    assert abs(as_float(row["sigma_axis_s_cm"]) + 97.7569471188) < 1e-9


def test_strain_csvs_cover_tensile_and_compressive_series() -> None:
    """Check that strain data cover tensile and compressive branches with expected grids."""
    plus = rows(PROCESSED / "strain_103" / "strain_plus_ahc.csv")
    minus = rows(PROCESSED / "strain_103" / "strain_minus_ahc.csv")
    assert len(plus) == 234
    assert len(minus) == 234
    assert sorted({as_float(row["strain_percent"]) for row in plus}) == [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    assert sorted({as_float(row["strain_percent"]) for row in minus}) == [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0]
    assert {row["strain_branch"] for row in plus} == {"tensile"}
    assert {row["strain_branch"] for row in minus} == {"compressive"}
