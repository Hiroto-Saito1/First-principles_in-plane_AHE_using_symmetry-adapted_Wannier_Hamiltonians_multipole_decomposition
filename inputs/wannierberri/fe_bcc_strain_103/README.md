# Fe [103] Strain WannierBerri Workflow Snapshot

This directory records the manuscript-specific `[103]` strain workflow that
fed the strain-dependent anomalous Hall conductivity panels. The public repo
already carries the compact strain CSV files and plotting script, while the
generic per-angle AHC machinery lives under `inputs/wannierberri/fe_bcc_rotation/`.
What was still missing was a reader-facing manifest that says how the private
`FM_sqa_103_strained_along_103/` archive fit into that public workflow.

## Files

- `strain_manifest.json`: archived source location, strain axis, strain grid,
  and the public replacements for the original private workflow pieces.

## How This Fits The Public Workflow

1. Generate the strained bcc Fe cells with
   `scripts/workflow/strain_103_cell.py`.
2. Run the DFT templates in `inputs/dft/fe_bcc_strain_103/`.
3. Reuse the generic SymWannier and WannierBerri drivers from
   `inputs/symwannier/fe_bcc/` and `inputs/wannierberri/fe_bcc_rotation/`.
4. Compare or rebuild the compact outputs in
   `data/processed/strain_103/`.

The original archive kept only a lightweight `strain_103.py` helper beside
the manuscript PDFs. Its deformation logic is now preserved in the public
cell-generator script and summarized by the JSON manifest here.
