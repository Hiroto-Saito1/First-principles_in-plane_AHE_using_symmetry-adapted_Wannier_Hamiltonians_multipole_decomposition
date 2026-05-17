#!/usr/bin/env python3
"""Print volume-preserving bcc Fe cell parameters strained along [103]."""

from __future__ import annotations

import argparse

import numpy as np


def strained_cell(percent: float) -> tuple[np.ndarray, float, float, float]:
    a1 = np.array([-1.4340702353, 1.4340702353, 1.4340702353])
    a2 = np.array([1.4340702353, -1.4340702353, 1.4340702353])
    a3 = np.array([1.4340702353, 1.4340702353, -1.4340702353])
    cell = np.vstack([a1, a2, a3])

    direction = np.array([1.0, 0.0, 3.0])
    direction = direction / np.linalg.norm(direction)
    lam = 1.0 + percent / 100.0
    if lam <= 0.0:
        raise ValueError("The stretch ratio must be positive.")
    mu = lam ** -0.5
    deformation = mu * np.eye(3) + (lam - mu) * np.outer(direction, direction)
    strained = (deformation @ cell.T).T

    volume0 = float(np.dot(cell[0], np.cross(cell[1], cell[2])))
    volume1 = float(np.dot(strained[0], np.cross(strained[1], strained[2])))
    return strained, float(np.linalg.det(deformation)), volume0, volume1


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--percent", "-p", type=float, required=True)
    args = parser.parse_args()

    strained, det_f, volume0, volume1 = strained_cell(args.percent)
    print(f"! percent = {args.percent:.6f}")
    print(f"! det(F)  = {det_f:.12f}")
    print(f"! V0, V1  = {volume0:.10f}  {volume1:.10f}  (angstrom^3)")
    print("CELL_PARAMETERS angstrom")
    for vec in strained:
        print(f"  {vec[0]: .10f}    {vec[1]: .10f}    {vec[2]: .10f}")


if __name__ == "__main__":
    main()
