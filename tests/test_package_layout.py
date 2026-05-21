"""Checks for the expanded public Python package layout."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import textwrap

import numpy as np

from symwan_multipie.symwannier import io_utils, timedata
from symwan_multipie.wannier_utils.hamiltonian import HamK
from symwan_multipie.wannier_utils.logger import get_logger


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "symwan_multipie"
WORKFLOW_OPTIONAL_IMPORTS = (
    "pymatgen",
    "scipy",
    "seekpath",
    "sparse_ir",
    "tomli",
    "tomli_w",
    "wannierberri",
)


def run_with_blocked_optional_imports(code: str) -> subprocess.CompletedProcess[str]:
    """Run Python in a subprocess that refuses workflow-only dependency imports."""

    script = "\n".join(
        [
            "import importlib.abc",
            "import sys",
            f"blocked = {WORKFLOW_OPTIONAL_IMPORTS!r}",
            "",
            "class Blocker(importlib.abc.MetaPathFinder):",
            "    def find_spec(self, fullname, path=None, target=None):",
            "        for name in blocked:",
            '            if fullname == name or fullname.startswith(name + "."):',
            '                raise ImportError(f"blocked optional dependency: {fullname}")',
            "        return None",
            "",
            "sys.meta_path.insert(0, Blocker())",
            textwrap.dedent(code).strip(),
            "",
        ]
    )
    return subprocess.run(
        [sys.executable, "-c", script],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )


def test_expanded_module_sets_are_present() -> None:
    """The public package should now ship the archived SymWannier module sets."""

    symwannier_modules = {
        path.name for path in (SRC / "symwannier").glob("*.py")
    }
    assert symwannier_modules == {
        "__init__.py",
        "amn.py",
        "cli.py",
        "eig.py",
        "expand_wannier_inputs.py",
        "io_utils.py",
        "mmn.py",
        "nnkp.py",
        "sym.py",
        "timedata.py",
        "wannierize.py",
        "win.py",
    }

    wannier_utils_modules = {
        path.name for path in (SRC / "wannier_utils").glob("*.py")
    }
    assert wannier_utils_modules == {
        "__init__.py",
        "band.py",
        "berry.py",
        "boltz.py",
        "cpa.py",
        "dos.py",
        "exchange.py",
        "exchange_input.py",
        "fourier.py",
        "green.py",
        "hamiltonian.py",
        "logger.py",
        "mag_sym.py",
        "mp_points.py",
        "mymodule.py",
        "nnkp.py",
        "parallel.py",
        "phys_matrix.py",
        "temperature_spir.py",
        "wannier_kmesh.py",
        "wannier_system.py",
        "wannier_system_main.py",
        "win.py",
    }


def test_expanded_modules_no_longer_reference_old_package_names() -> None:
    """Copied source files should use repo-local imports rather than old package names."""

    for path in list((SRC / "symwannier").glob("*.py")) + list(
        (SRC / "wannier_utils").glob("*.py")
    ):
        text = path.read_text(encoding="utf-8")
        assert "from symwannier." not in text
        assert "import symwannier" not in text
        assert "from wannier_utils." not in text
        assert "import wannier_utils" not in text
        assert "from mymodule import" not in text


def test_lightweight_imports_and_hamk_still_work(fixture_ham) -> None:
    """The expanded package should preserve the lightweight public API."""

    assert io_utils.open_text_or_gz is not None
    assert timedata.TimeData is not None
    assert type(get_logger(__name__)).__name__ == "Logger"

    ham_k = HamK(fixture_ham, np.zeros(3), diagonalize=True)
    assert np.allclose(ham_k.hk, fixture_ham.hrs[0])
    assert np.allclose(ham_k.ek, np.linalg.eigvalsh(fixture_ham.hrs[0]))


def test_hamk_minus_d_fermi_uses_eigenvalues_when_not_pre_diagonalized(fixture_ham) -> None:
    """The Fermi-derivative helper should populate eigenvalues without storing tuples."""

    ham_k = HamK(fixture_ham, np.zeros(3), diagonalize=False)
    mu_range = np.array([0.0, 0.2])
    tmpr_range = np.array([300.0])

    minus_df = ham_k.get_minus_d_fermi(mu_range, tmpr_range)

    eigenvalues = np.linalg.eigvalsh(fixture_ham.hrs[0])
    kbt = tmpr_range * 8.617333262145e-5
    x = (eigenvalues[:, None, None] - mu_range[None, :, None]) / kbt[None, None, :]
    expected = 1.0 / (np.exp(x) + 2.0 + np.exp(-x)) / kbt[None, None, :]

    assert np.allclose(ham_k.ek, eigenvalues)
    assert minus_df.shape == (2, 2, 1)
    assert np.allclose(minus_df, expected)


def test_base_public_imports_do_not_require_workflow_optional_dependencies() -> None:
    """The lightweight public import surface should work without workflow extras."""

    result = run_with_blocked_optional_imports(
        """
from symwan_multipie import EnergyDiff, MagRotation, Multipole, MultipoleDecomposition
from symwan_multipie.wannier_utils import BandStructure, HamK, HamR, WanBand
print("base-ok")
"""
    )

    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "base-ok"


def test_workflow_only_module_still_requires_optional_dependencies() -> None:
    """A workflow-facing module should fail cleanly when blocked extras are absent."""

    result = run_with_blocked_optional_imports(
        """
import symwan_multipie.wannier_utils.win
"""
    )

    assert result.returncode != 0
    assert "blocked optional dependency" in result.stderr
