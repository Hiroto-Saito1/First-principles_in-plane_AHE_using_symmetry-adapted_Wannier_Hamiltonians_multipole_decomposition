# Plane Definition Figures

This directory stores compact configuration data for the manuscript plane
definition figures:

- `bcc_111.pdf`
- `bcc_103.pdf`

The source JSON captures the plane normal, in-plane reference directions,
default magnetization angle, and output filename. The repository plotting
script `scripts/reproduce_figures/plot_bcc_planes.py` uses this JSON to
generate the committed reference PDFs under `figures/paper/` and equivalent
repository-local manuscript-style outputs under
`results/figures_paper/definitions/`.
