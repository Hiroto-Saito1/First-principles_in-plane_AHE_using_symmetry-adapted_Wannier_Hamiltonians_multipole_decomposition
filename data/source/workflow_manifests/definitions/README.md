# Geometric Definition Reference-Information Contracts

This directory records the minimum information content required for the
paper-facing geometric definition plots:

- `bcc_111.pdf`
- `bcc_103.pdf`

Unlike curve or bar plots, the contract here focuses on semantic geometry
rather than point counts. The paper-facing outputs must preserve:

- the plane identifier and output file;
- the rotation angle `psi`;
- the plane normal used for the viewing geometry;
- the reference and perpendicular in-plane vectors; and
- the manuscript-facing crystallographic labels attached to those vectors.

The committed JSON under `data/processed/definitions/bcc_planes.json` remains
the source of truth for these semantics, and the paper-facing script reads it
directly.
