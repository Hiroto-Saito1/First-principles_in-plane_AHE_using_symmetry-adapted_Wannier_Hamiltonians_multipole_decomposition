#!/usr/bin/env python3
"""Generate the `(111)` and `(103)` bcc plane-definition figures."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
PROCESSED = ROOT / "data" / "processed"
DEFAULT_OUTPUT = ROOT / "results" / "figures_paper" / "definitions"
REQUIRED_CONFIG_KEYS = [
    "id",
    "title",
    "output_file",
    "psi_deg",
    "plane_normal",
    "reference_vector",
    "reference_label",
    "perpendicular_vector",
    "perpendicular_label",
]


def get_pyplot():
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    return plt


def load_configs(path: Path) -> list[dict[str, object]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    configs = list(data["planes"])
    for config in configs:
        missing = [key for key in REQUIRED_CONFIG_KEYS if key not in config]
        if missing:
            raise KeyError(f"Missing plane-definition keys for {config.get('id', '?')}: {missing}")
    return configs


def unit(vector: np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(vector)
    return vector / norm if norm else vector


def arrow3d_class():
    from matplotlib.patches import FancyArrowPatch
    from mpl_toolkits.mplot3d import proj3d

    class Arrow3D(FancyArrowPatch):
        def __init__(self, xs, ys, zs, *args, **kwargs):
            super().__init__((0, 0), (0, 0), *args, **kwargs)
            self._verts3d = xs, ys, zs

        def do_3d_projection(self, renderer=None):
            xs3d, ys3d, zs3d = self._verts3d
            xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, self.axes.get_proj())
            self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
            return float(np.min(zs))

        def draw(self, renderer):
            self.do_3d_projection(renderer)
            super().draw(renderer)

    return Arrow3D


def draw_plane(config: dict[str, object], output: Path) -> None:
    plt = get_pyplot()
    Arrow3D = arrow3d_class()

    plane_normal = unit(np.array(config["plane_normal"], dtype=float))
    reference_vector = unit(np.array(config["reference_vector"], dtype=float))
    perpendicular_vector = unit(np.array(config["perpendicular_vector"], dtype=float))
    psi = np.deg2rad(float(config["psi_deg"]))

    plt.rcParams.update({"font.size": 20, "axes.labelsize": 20, "axes.titlesize": 20})
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111, projection="3d")

    a = 1.0
    corners = np.array(
        [
            [0, 0, 0],
            [a, 0, 0],
            [0, a, 0],
            [0, 0, a],
            [a, a, 0],
            [a, 0, a],
            [0, a, a],
            [a, a, a],
        ]
    )
    center = np.array([[a / 2, a / 2, a / 2]])

    ax.scatter(corners[:, 0], corners[:, 1], corners[:, 2], s=200, color="k")
    ax.scatter(center[:, 0], center[:, 1], center[:, 2], s=200, color="k")

    edges = [
        (0, 1),
        (0, 2),
        (0, 3),
        (1, 4),
        (1, 5),
        (2, 4),
        (2, 6),
        (3, 5),
        (3, 6),
        (4, 7),
        (5, 7),
        (6, 7),
    ]
    for i, j in edges:
        ax.plot(
            [corners[i, 0], corners[j, 0]],
            [corners[i, 1], corners[j, 1]],
            [corners[i, 2], corners[j, 2]],
            "k-",
            linewidth=1,
        )

    world_up = np.array([0.0, 1.0, 0.0])
    if abs(np.dot(plane_normal, world_up)) > 0.95:
        world_up = np.array([0.0, 0.0, 1.0])
    screen_right = unit(np.cross(plane_normal, world_up))
    screen_up = unit(np.cross(screen_right, plane_normal))

    def place_label_along(
        vec_u: np.ndarray,
        text: str,
        color: str,
        along: float = 0.95,
        off_r: float = 0.08,
        off_u: float = 0.05,
    ) -> None:
        position = (
            center.flatten()
            + vec_u * along
            + screen_right * off_r
            + screen_up * off_u
        )
        ax.text(
            *position,
            text,
            color=color,
            ha="center",
            va="center",
            bbox=dict(facecolor="white", alpha=0.7, edgecolor="none", pad=0.2),
        )

    s = np.linspace(-0.8, 1.2, 15)
    t = np.linspace(-0.8, 1.2, 15)
    ss, tt = np.meshgrid(s, t)
    plane = (
        np.outer(ss.flatten(), reference_vector)
        + np.outer(tt.flatten(), perpendicular_vector)
        + center
    )
    xx = plane[:, 0].reshape(ss.shape)
    yy = plane[:, 1].reshape(ss.shape)
    zz = plane[:, 2].reshape(ss.shape)
    ax.plot_surface(xx, yy, zz, alpha=0.3, color="gray")

    def draw_arrow(vec_u: np.ndarray, color: str, length: float = 0.8) -> np.ndarray:
        start = center.flatten()
        end = start + vec_u * length
        arrow = Arrow3D(
            [start[0], end[0]],
            [start[1], end[1]],
            [start[2], end[2]],
            arrowstyle="-|>",
            mutation_scale=18,
            lw=2.2,
            color=color,
            shrinkA=0,
            shrinkB=0,
        )
        ax.add_artist(arrow)
        return vec_u

    reference_vector = draw_arrow(reference_vector, "r")
    perpendicular_vector = draw_arrow(perpendicular_vector, "b")
    place_label_along(
        reference_vector,
        str(config["reference_label"]),
        color="r",
        along=1.0,
        off_r=0.14,
        off_u=0.06,
    )
    place_label_along(
        perpendicular_vector,
        str(config["perpendicular_label"]),
        color="b",
        along=1.0,
        off_r=-0.14,
        off_u=0.06,
    )

    magnetization = unit(
        np.cos(psi) * reference_vector + np.sin(psi) * perpendicular_vector
    )
    start = center.flatten()
    end = start + magnetization * 0.9
    ax.add_artist(
        Arrow3D(
            [start[0], end[0]],
            [start[1], end[1]],
            [start[2], end[2]],
            arrowstyle="-|>",
            mutation_scale=18,
            lw=2.2,
            color="g",
            shrinkA=0,
            shrinkB=0,
        )
    )
    place_label_along(
        magnetization,
        r"$\mathbf{M}(\psi)$",
        color="g",
        along=1.18,
        off_r=0.0,
        off_u=0.10,
    )

    ts = np.linspace(0, psi, 60)
    arc = np.array(
        [np.cos(theta) * reference_vector + np.sin(theta) * perpendicular_vector for theta in ts]
    )
    arc_centered = center + 0.6 * arc
    ax.plot(arc_centered[:, 0], arc_centered[:, 1], arc_centered[:, 2], color="g")
    mid = unit(
        np.cos(psi / 2) * reference_vector + np.sin(psi / 2) * perpendicular_vector
    )
    ax.text(
        *(center.flatten() + mid * 0.72 + screen_right * 0.03 + screen_up * 0.07),
        r"$\psi$",
        color="g",
        ha="center",
        va="center",
        bbox=dict(facecolor="white", alpha=0.7, edgecolor="none", pad=0.2),
    )

    ax.set_xlabel("$x$", fontsize=18)
    ax.set_ylabel("$y$", fontsize=18)
    ax.set_zlabel("$z$", fontsize=18)
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_zticklabels([])
    ax.xaxis._axinfo["grid"]["linewidth"] = 0
    ax.yaxis._axinfo["grid"]["linewidth"] = 0
    ax.zaxis._axinfo["grid"]["linewidth"] = 0
    ax.set_xlim(-0.5, 1.5)
    ax.set_ylim(-0.5, 1.5)
    ax.set_zlim(-0.5, 1.5)

    azim = np.degrees(np.arctan2(plane_normal[1], plane_normal[0]))
    elev = np.degrees(np.arctan2(plane_normal[2], np.hypot(plane_normal[0], plane_normal[1])))
    ax.view_init(elev=elev, azim=azim, roll=-90)

    try:
        ax.set_box_aspect([1, 1, 1])
    except AttributeError:
        pass

    fig.subplots_adjust(left=0.02, right=0.98, bottom=0.02, top=0.98)
    output.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output, dpi=300)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=PROCESSED / "definitions" / "bcc_planes.json",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT / "definitions",
    )
    args = parser.parse_args()

    if not args.input.is_file():
        raise SystemExit(f"Missing plane-definition JSON: {args.input}")

    for config in load_configs(args.input):
        draw_plane(config, args.output_dir / str(config["output_file"]))


if __name__ == "__main__":
    main()
