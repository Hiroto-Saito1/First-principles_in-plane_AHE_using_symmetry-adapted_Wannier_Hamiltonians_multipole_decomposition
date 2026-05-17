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

