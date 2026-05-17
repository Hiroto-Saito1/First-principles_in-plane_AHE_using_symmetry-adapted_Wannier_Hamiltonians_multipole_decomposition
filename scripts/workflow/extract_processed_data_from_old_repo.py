#!/usr/bin/env python3
"""Extract compact manuscript figure data from the old working repository.

This script intentionally reads only small XML summaries. Large DFT,
Wannier, HDF5, and WannierBerri intermediate files are not copied.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
import xml.etree.ElementTree as ET


DEFAULT_OLD_REPO = Path(
    "/Users/hirotosaito/Library/CloudStorage/Dropbox/AnacondaProjects/"
    "是常研究室/2024/github_projects/symwan_multipie"
)

AHC_FIELDS = [
    "sigma_xy",
    "sigma_yz",
    "sigma_zx",
    "sigma_para",
    "sigma_perp",
    "sigma_axis",
]


def parse_float(text: str | None) -> float:
    if text is None:
        return math.nan
    text = text.strip()
    if text.lower() == "nan":
        return math.nan
    return float(text)


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")


def read_ahc_xml(path: Path, *, plane: str, series_group: str) -> list[dict[str, object]]:
    root = ET.parse(path).getroot()
    rows: list[dict[str, object]] = []
    for method in root.findall("method"):
        label = method.attrib["label"]
        for angle in method.findall("angle"):
            row: dict[str, object] = {
                "plane": plane,
                "series_group": series_group,
                "method": label,
                "phi_deg": parse_float(angle.attrib.get("phi")),
            }
            for field in AHC_FIELDS:
                row[f"{field}_s_cm"] = parse_float(angle.findtext(field))
            rows.append(row)
    return rows


def read_energy_xml(path: Path, *, plane: str, series: str) -> list[dict[str, object]]:
    root = ET.parse(path).getroot()
    raw: list[tuple[float, float]] = []
    for angle in root.findall("angle"):
        angle_value = angle.attrib.get("phi", angle.attrib.get("theta"))
        raw.append((parse_float(angle_value), parse_float(angle.findtext("energy"))))
    baseline = raw[0][1] if raw else math.nan
    return [
        {
            "plane": plane,
            "series": series,
            "angle_deg": angle,
            "total_energy_ev": energy,
            "relative_energy_microev": (energy - baseline) * 1.0e6,
        }
        for angle, energy in raw
    ]


def extract_primary_ahc(old_repo: Path, output: Path) -> None:
    sources = {
        "111": old_repo / "tests/Fe/FM_sqa_111",
        "103": old_repo / "tests/Fe/FM_sqa_103",
    }
    for plane, source in sources.items():
        target = output / f"ahc_{plane}"
        ahc_rows = read_ahc_xml(
            source / "angle_dep_ahc_dft.xml",
            plane=plane,
            series_group="primary_ahc",
        )
        write_csv(
            target / "ahc_angle_dependence.csv",
            ["plane", "series_group", "method", "phi_deg"]
            + [f"{field}_s_cm" for field in AHC_FIELDS],
            ahc_rows,
        )
        energy_rows = read_energy_xml(
            source / "angle_dep_ed.xml",
            plane=plane,
            series="SW+ED",
        )
        write_csv(
            target / "energy_angle_dependence.csv",
            [
                "plane",
                "series",
                "angle_deg",
                "total_energy_ev",
                "relative_energy_microev",
            ],
            energy_rows,
        )
        write_json(
            target / "metadata.json",
            {
                "description": f"Processed bcc Fe ({plane}) angular data.",
                "source_directory": str(source),
                "source_files": [
                    "angle_dep_ahc_dft.xml",
                    "angle_dep_ed.xml",
                ],
                "fermi_level_ev": 17.4112,
                "units": {
                    "angle": "degree",
                    "ahc": "S/cm",
                    "energy": "eV",
                    "relative_energy": "micro-eV",
                },
                "large_file_policy": "No raw DFT, Wannier, or AHC intermediate files were copied.",
            },
        )


def extract_rank_resolved(old_repo: Path, output: Path) -> None:
    base = (
        old_repo
        / "tests/Fe/FM_sqa_103/theta0_qe-7.2/hamiltonian_hdf5_trs"
    )
    source = base / "anisotropy_w_rank3"
    target = output / "rank_resolved_103"
    rows = read_ahc_xml(
        source / "angle_dep_ahc.xml",
        plane="103",
        series_group="rank_cumulative",
    )
    rows.extend(
        read_ahc_xml(
            base / "anisotropy/angle_dep_ahc.xml",
            plane="103",
            series_group="reference",
        )
    )
    write_csv(
        target / "rank_resolved_ahc.csv",
        ["plane", "series_group", "method", "phi_deg"]
        + [f"{field}_s_cm" for field in AHC_FIELDS],
        rows,
    )

    energy_rows: list[dict[str, object]] = []
    for xml_path in sorted(source.glob("angle_dep_w_rank*.xml")):
        label = xml_path.stem.removeprefix("angle_dep_")
        energy_rows.extend(read_energy_xml(xml_path, plane="103", series=label))
    energy_rows.extend(
        read_energy_xml(
            base / "anisotropy/angle_dep_ed_90.xml",
            plane="103",
            series="SW+ED_reference",
        )
    )
    write_csv(
        target / "rank_cumulative_energy.csv",
        [
            "plane",
            "series",
            "angle_deg",
            "total_energy_ev",
            "relative_energy_microev",
        ],
        energy_rows,
    )
    write_json(
        target / "metadata.json",
        {
            "description": "Rank-cumulative AHC and energy data for bcc Fe in the (103) rotation plane.",
            "source_directory": str(source),
            "reference_source_directory": str(base / "anisotropy"),
            "source_files": [
                "angle_dep_ahc.xml",
                "angle_dep_w_rank*.xml",
                "../anisotropy/angle_dep_ahc.xml",
                "../anisotropy/angle_dep_ed_90.xml",
            ],
            "rank_series": [
                "w_rank1",
                "w_rank1_2",
                "w_rank1_2_3",
                "w_rank1_2_3_4",
                "w_rank1_2_3_4_5",
                "w_rank1_2_3_4_5_6",
                "w_rank1_2_3_4_5_6_7",
                "w_rank1_2_3_4_5_6_7_8",
            ],
            "units": {
                "angle": "degree",
                "ahc": "S/cm",
                "energy": "eV",
                "relative_energy": "micro-eV",
            },
            "large_file_policy": "Rotated Hamiltonians and WannierBerri work directories are regenerated by workflow documentation, not stored.",
        },
    )


def strain_percent_from_dir(name: str) -> float:
    if name == "0percent":
        return 0.0
    if name.startswith("m") and name.endswith("percent"):
        return -float(name[1:-7])
    if name.endswith("percent"):
        return float(name[:-7])
    raise ValueError(f"Cannot parse strain directory name: {name}")


def extract_strain(old_repo: Path, output: Path) -> None:
    source = old_repo / "tests/Fe/FM_sqa_103_strained_along_103"
    target = output / "strain_103"
    plus_dirs = ["0percent", "0.2percent", "0.4percent", "0.6percent", "0.8percent", "1percent"]
    minus_dirs = ["0percent", "m0.2percent", "m0.4percent", "m0.6percent", "m0.8percent", "m1percent"]

    def build_rows(branch: str, dirs: list[str]) -> list[dict[str, object]]:
        rows: list[dict[str, object]] = []
        for dirname in dirs:
            xml_path = source / dirname / "angle_dep_ahc_dft.xml"
            for row in read_ahc_xml(xml_path, plane="103", series_group="strain"):
                row["strain_branch"] = branch
                row["strain_percent"] = strain_percent_from_dir(dirname)
                row["source_directory"] = dirname
                rows.append(row)
        return rows

    fieldnames = [
        "strain_branch",
        "strain_percent",
        "source_directory",
        "plane",
        "series_group",
        "method",
        "phi_deg",
    ] + [f"{field}_s_cm" for field in AHC_FIELDS]
    write_csv(target / "strain_plus_ahc.csv", fieldnames, build_rows("tensile", plus_dirs))
    write_csv(target / "strain_minus_ahc.csv", fieldnames, build_rows("compressive", minus_dirs))
    write_json(
        target / "metadata.json",
        {
            "description": "Volume-preserving uniaxial strain along [103] for bcc Fe.",
            "source_directory": str(source),
            "source_files": ["*/angle_dep_ahc_dft.xml"],
            "strain_percent_values": [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
            "fermi_level_ev": 17.4112,
            "units": {
                "strain": "percent",
                "angle": "degree",
                "ahc": "S/cm",
            },
            "large_file_policy": "Strained DFT and Wannier directories are regenerated from documented CELL_PARAMETERS, not stored.",
        },
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--old-repo", type=Path, default=DEFAULT_OLD_REPO)
    parser.add_argument("--output", type=Path, default=Path("data/processed"))
    args = parser.parse_args()

    extract_primary_ahc(args.old_repo, args.output)
    extract_rank_resolved(args.old_repo, args.output)
    extract_strain(args.old_repo, args.output)


if __name__ == "__main__":
    main()
