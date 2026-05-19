"""Validate the public workflow input manifests.

These checks keep `inputs/` useful as a reader-facing reproduction map without
requiring DFT, Wannier90, SymWannier, MultiPie, or WannierBerri to be
installed during the lightweight test suite.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INPUTS = ROOT / "inputs"


def test_expected_input_groups_have_readmes() -> None:
    """Every curated input group should explain its purpose and run context."""
    groups = [
        "dft/fe_bcc_unstrained",
        "dft/fe_bcc_strain_103",
        "wannier/fe_bcc_unstrained",
        "symwannier/fe_bcc",
        "multipie/fe_bcc",
        "wannierberri/fe_bcc_rotation",
    ]
    for group in groups:
        readme = INPUTS / group / "README.md"
        assert readme.is_file(), f"Missing README for {group}"
        assert len(readme.read_text(encoding="utf-8").split()) >= 30


def test_input_manifests_capture_rotation_and_ahc_settings() -> None:
    """The JSON manifests should preserve the key angle-grid and AHC settings."""
    rotation = json.loads(
        (INPUTS / "wannierberri/fe_bcc_rotation/rotation_grid.json").read_text(
            encoding="utf-8"
        )
    )
    planes = {plane["label"]: plane for plane in rotation["rotation_planes"]}
    assert planes["103"]["axis2"] == [1.0, 0.0, 3.0]
    assert planes["111"]["axis2"] == [1.0, 1.0, 1.0]
    assert rotation["wannierberri"]["grid_NK"] == [100, 100, 100]
    assert rotation["wannierberri"]["adpt_num_iter"] == 20
    assert rotation["fermi_energy_ev"] == 17.4112

    symwannier = json.loads(
        (INPUTS / "symwannier/fe_bcc/symwannier_settings.json").read_text(
            encoding="utf-8"
        )
    )
    assert symwannier["wannier_functions"]["count"] == 36
    assert symwannier["component_filter"]["irreps"] == ["T1g"]
    assert {
        variant["generated_file"] for variant in symwannier["hamiltonian_variants"]
    } == {
        "pwscf_py_ed_tb.hdf5",
        "pwscf_py_pd_tb.hdf5",
        "trs_py_ed_tb.hdf5",
        "pwscf_tb.hdf5",
    }

    samb_manifest = json.loads(
        (INPUTS / "multipie/fe_bcc/samb_manifest.json").read_text(encoding="utf-8")
    )
    assert samb_manifest["workflow_scripts"]["matrix_to_hdf5"] == (
        "scripts/workflow/build_multipole_hdf5.py"
    )
    assert samb_manifest["bar_plot_inputs"]["decomposition_hdf5"] == (
        "trs_py_ed_tb.hdf5"
    )


def test_soc_templates_and_multipie_inputs_are_present() -> None:
    """The public input layer should include the recovered SOC and SAMB files."""
    nscf_text = (INPUTS / "dft/fe_bcc_unstrained/nscf.in").read_text(
        encoding="utf-8"
    )
    assert "noncolin = .true." in nscf_text
    assert "lspinorb = .true." in nscf_text
    assert "Fe.rel-pbe-spn-rrkjus_psl.0.2.1.UPF" in nscf_text

    wannier_text = (INPUTS / "wannier/fe_bcc_unstrained/pwscf.win").read_text(
        encoding="utf-8"
    )
    assert "begin projections" in wannier_text
    assert "Fe: s,p,d  [0,0,1]" in wannier_text
    assert "spinors = .true." in wannier_text

    for relative_path in [
        "multipie/fe_bcc/Fe.py",
        "multipie/fe_bcc/Fe_model.py",
        "multipie/fe_bcc/submit_samb.sh",
    ]:
        assert (INPUTS / relative_path).is_file(), f"Missing {relative_path}"

    for relative_path in [
        "symwannier/fe_bcc/write_trs_ham.py",
        "symwannier/fe_bcc/decompose_ham.py",
        "symwannier/fe_bcc/energy_diff_fe.py",
        "symwannier/fe_bcc/submit_energy_diff.sh",
    ]:
        assert (INPUTS / relative_path).is_file(), f"Missing {relative_path}"

    for relative_path in [
        "wannierberri/fe_bcc_rotation/rotate_mag.py",
        "wannierberri/fe_bcc_rotation/calc_energy.py",
        "wannierberri/fe_bcc_rotation/submit_ahc_all.py",
    ]:
        assert (INPUTS / relative_path).is_file(), f"Missing {relative_path}"


def test_qe_patch_artifacts_are_present() -> None:
    """The public docs should include the recorded QE pw2wannier90 patch."""
    patch_dir = ROOT / "docs" / "qe_patch"
    readme = patch_dir / "README.md"
    patch_file = patch_dir / "pw2wannier90.patch"

    assert readme.is_file()
    assert patch_file.is_file()
    patch_text = patch_file.read_text(encoding="utf-8")
    assert patch_text.startswith("--- PP/src/pw2wannier90.f90")
    assert "spin_eig" in patch_text
    assert "proj_sign" in patch_text


def test_inputs_do_not_embed_private_absolute_paths() -> None:
    """Public inputs should not depend on a private workstation directory."""
    forbidden = ["/Users/", "/home/", "CloudStorage", "Dropbox"]
    text_suffixes = {".in", ".win", ".py", ".json", ".md"}
    for path in INPUTS.rglob("*"):
        if not path.is_file() or path.suffix not in text_suffixes:
            continue
        text = path.read_text(encoding="utf-8")
        for needle in forbidden:
            assert needle not in text, f"{path} contains private path token {needle}"
