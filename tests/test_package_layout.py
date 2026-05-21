"""Checks for the expanded public Python package layout."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from symwan_multipie.symwannier import io_utils, timedata
from symwan_multipie.wannier_utils.hamiltonian import HamK
from symwan_multipie.wannier_utils.logger import get_logger


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "symwan_multipie"


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
