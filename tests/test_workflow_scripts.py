"""Regression tests for lightweight workflow helper scripts."""

from __future__ import annotations

import csv
from pathlib import Path
import subprocess
import sys

import h5py

from symwan_multipie import Multipole, MultipoleDecomposition


ROOT = Path(__file__).resolve().parents[1]


def test_build_multipole_hdf5_script_creates_expected_basis(
    tmp_path: Path, multipie_pickle: Path
) -> None:
    """The matrix-to-HDF5 helper should emit the expected sparse basis layout."""
    output = tmp_path / "multi_matrix.hdf5"
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "workflow" / "build_multipole_hdf5.py"),
            "--matrix-path",
            str(multipie_pickle),
            "--output",
            str(output),
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    assert output.is_file()
    assert "num_multipole=4" in result.stdout
    with h5py.File(output, "r") as h5:
        grp = h5["multipole_matrix"]
        assert tuple(int(x) for x in grp["shape"][:]) == (4, 1, 2, 2)
        assert tuple(int(x) for x in grp["irvec"][0]) == (0, 0, 0)
        names = [
            name.decode("utf-8") if isinstance(name, bytes) else str(name)
            for name in grp["names"][:]
        ]
        assert names == ["z_000", "z_001", "z_002", "z_003"]


def test_export_multipole_coefficients_script_creates_bar_snapshot(
    tmp_path: Path,
    multipie_pickle: Path,
    samb_path: Path,
    fixture_ham,
) -> None:
    """The coefficient exporter should turn decomposition HDF5 into a compact CSV."""
    basis_hdf5 = tmp_path / "multi_matrix.hdf5"
    Multipole(multipie_pickle).write_hdf5(basis_hdf5)

    decomposition = MultipoleDecomposition(
        ham_r=fixture_ham,
        multipole_path=basis_hdf5,
    )
    decomp_hdf5 = tmp_path / "trs_py_ed_tb.hdf5"
    decomposition.write_hdf5(decomp_hdf5)

    output = tmp_path / "multipole_coefficients.csv"
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "workflow" / "export_multipole_coefficients.py"),
            "--multi-path",
            str(decomp_hdf5),
            "--samb-path",
            str(samb_path),
            "--output",
            str(output),
            "--mode",
            "bar-merged",
            "--top",
            "2",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    assert output.is_file()
    assert "Wrote" in result.stdout
    with output.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    assert len(rows) == 3
    by_index = {row["index"]: row for row in rows}
    assert set(by_index) == {"000", "001", "003"}
    assert by_index["000"]["selection"] == "all_top2"
    assert by_index["001"]["selection"] == "all_top2;non_q_top2"
    assert by_index["003"]["selection"] == "non_q_top2"
    assert by_index["001"]["source_hdf5"] == "trs_py_ed_tb.hdf5"
    assert by_index["001"]["source_samb"] == "fixture_samb.py"
    assert abs(float(by_index["001"]["coefficient_ev"]) + 0.5) < 1e-8


def test_export_minimal_model_source_script_collects_sigma_axis_rows(
    tmp_path: Path,
) -> None:
    """The minimal-model export helper should condense archived AHC text outputs."""
    source_root = tmp_path / "bcc_model"
    layouts = [
        ("1st_nn_t2_0", "t_T_0.0", "psi_0", 0.0),
        ("1st_nn_t2_0", "t_T_0.0", "psi_90", 1.0),
        ("2nd_nn_t1_0.2", "t_T_0.1", "psi_0", 2.0),
        ("2nd_nn_t1_0.2", "t_T_0.1", "psi_90", 3.0),
    ]
    for tree, parameter, angle, yz_value in layouts:
        target = source_root / tree / parameter / angle / "sigma_ahc_eta1.00meV.txt"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(
            "# header\n"
            "-1.0 0.0 0.0 0.0\n"
            f"0.0 4.0 {yz_value:.1f} 2.0\n"
            "1.0 0.0 0.0 0.0\n",
            encoding="utf-8",
        )

    output = tmp_path / "model_sigma_axis.csv"
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "workflow" / "export_minimal_model_source.py"),
            "--source-root",
            str(source_root),
            "--output",
            str(output),
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    assert output.is_file()
    assert "Wrote 4 rows" in result.stdout
    with output.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    assert len(rows) == 4
    row = next(
        item
        for item in rows
        if item["scan"] == "second_nn"
        and item["parameter_value"] == "0.1"
        and item["phi_deg"] == "90"
    )
    assert row["source_tree"] == "2nd_nn_t1_0.2"
    assert row["source_file"] == "t_T_0.1/psi_90/sigma_ahc_eta1.00meV.txt"
    expected = (3.0 + 12.0) / (10.0 ** 0.5)
    assert abs(float(row["sigma_axis"]) - expected) < 1e-8
