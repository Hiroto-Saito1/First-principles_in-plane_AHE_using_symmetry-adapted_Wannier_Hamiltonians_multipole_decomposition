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


def test_recovered_band_bond_curves_cover_expected_cutoffs_and_series() -> None:
    """Check recovered band/bond curve rows and key convergence signatures."""
    data = rows(PROCESSED / "band_bond" / "band_bond_curves.csv")
    assert len(data) == 20099
    assert sorted({int(row["cutoff_shell"]) for row in data}) == [1, 2, 3, 4, 5, 10, 20, 35]
    assert sorted({row["series"] for row in data}) == ["DFT", "model"]
    assert {row["source_pdf"] for row in data} == {
        "band_1.pdf",
        "band_2.pdf",
        "band_3.pdf",
        "band_4.pdf",
        "band_5.pdf",
        "band_10.pdf",
        "band_20.pdf",
        "band_35.pdf",
    }
    assert min(as_float(row["k_path_fraction"]) for row in data) == 0.0
    assert max(as_float(row["k_path_fraction"]) for row in data) == 1.0

    dft_35 = [
        row for row in data if row["cutoff_shell"] == "35" and row["series"] == "DFT"
    ]
    model_1 = [
        row for row in data if row["cutoff_shell"] == "1" and row["series"] == "model"
    ]
    assert len({row["curve_index"] for row in dft_35}) == 16
    assert len({row["curve_index"] for row in model_1}) == 14

    dft_gamma = select(
        data,
        cutoff_shell="35",
        series="DFT",
        curve_index="0",
        point_index="0",
    )
    model_gamma = select(
        data,
        cutoff_shell="1",
        series="model",
        curve_index="0",
        point_index="0",
    )
    assert abs(as_float(dft_gamma["energy_ev"]) + 8.50769996) < 1e-8
    assert abs(as_float(model_gamma["energy_ev"]) + 2.86485967) < 1e-8


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


def test_recovered_multipole_coefficients_cover_paper_bar_inputs() -> None:
    """Check recovered multipole coefficient rows used by the bar plots."""
    data = rows(PROCESSED / "multipole_coefficients" / "multipole_coefficients.csv")
    assert len(data) == 39
    assert {"bar_ed_all_35.pdf", "bar_ed_wo_q_35.pdf"} == {
        row["source_pdf"] for row in data
    }
    strongest = max(data, key=lambda row: as_float(row["abs_coefficient_ev"]))
    assert strongest["index"] == "2"
    assert strongest["name"].startswith("Q(")
    assert abs(as_float(strongest["coefficient_ev"]) - 80.0) < 1e-8
    assert any(row["name"].startswith("T(") for row in data)


def test_recovered_minimal_model_scans_cover_expected_parameters() -> None:
    """Check recovered minimal-model scans and their manuscript angle grid."""
    data = rows(PROCESSED / "minimal_model" / "model_sigma_axis.csv")
    assert len(data) == 143
    assert sorted({row["scan"] for row in data}) == ["first_nn", "second_nn"]
    assert sorted({as_float(row["phi_deg"]) for row in data}) == list(range(0, 181, 15))
    assert sorted(
        {as_float(row["parameter_value"]) for row in data if row["scan"] == "first_nn"}
    ) == [0.0, 0.05, 0.1, 0.15, 0.2]
    assert sorted(
        {as_float(row["parameter_value"]) for row in data if row["scan"] == "second_nn"}
    ) == [0.0, 0.1, 0.11, 0.12, 0.13, 0.14]
    row = select(data, scan="first_nn", parameter_value="0.2", phi_deg="90")
    assert 23.0 < as_float(row["sigma_axis"]) < 24.0
