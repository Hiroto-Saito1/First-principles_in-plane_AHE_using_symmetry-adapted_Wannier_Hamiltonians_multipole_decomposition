#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="${PYTHON:-python}"
PAPER_OUTPUT_ROOT="$ROOT/results/figures_paper"
DIAGNOSTIC_OUTPUT_ROOT="$ROOT/results/figures_diagnostics"
check_only=0
generate_paper=1
generate_diagnostics=1

usage() {
  cat <<EOF
Usage: scripts/reproduce_all_figures.sh [options] [legacy-paper-output-root]

Options:
  --check                   Verify inputs and scripts only; do not plot.
  --paper-root PATH         Output root for manuscript-style plots.
  --diagnostics-root PATH   Output root for diagnostic plots.
  --paper-only              Generate only manuscript-style plots.
  --diagnostics-only        Generate only diagnostic plots.
  -h, --help                Show this help.

With no options, the script writes manuscript-style outputs under
results/figures_paper/ and diagnostic AHC comparison plots under
results/figures_diagnostics/.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --check)
      check_only=1
      shift
      ;;
    --paper-root)
      PAPER_OUTPUT_ROOT="$2"
      shift 2
      ;;
    --diagnostics-root)
      DIAGNOSTIC_OUTPUT_ROOT="$2"
      shift 2
      ;;
    --paper-only)
      generate_diagnostics=0
      shift
      ;;
    --diagnostics-only)
      generate_paper=0
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      if [[ "${1:0:1}" != "-" ]]; then
        PAPER_OUTPUT_ROOT="$1"
        generate_diagnostics=0
        shift
      else
        echo "Unknown argument: $1" >&2
        usage >&2
        exit 2
      fi
      ;;
  esac
done

if [[ "$generate_paper" -eq 0 && "$generate_diagnostics" -eq 0 ]]; then
  echo "Nothing to do: both paper and diagnostics outputs are disabled." >&2
  exit 2
fi

required_inputs=(
  "$ROOT/data/processed/definitions/bcc_planes.json"
  "$ROOT/data/processed/band_bond/band_bond_curves.csv"
  "$ROOT/data/processed/ahc_111/ahc_angle_dependence.csv"
  "$ROOT/data/processed/ahc_103/ahc_angle_dependence.csv"
  "$ROOT/data/processed/rank_resolved_103/rank_resolved_ahc.csv"
  "$ROOT/data/processed/rank_resolved_103/single_rank_ahc.csv"
  "$ROOT/data/processed/strain_103/strain_plus_ahc.csv"
  "$ROOT/data/processed/strain_103/strain_minus_ahc.csv"
  "$ROOT/data/processed/multipole_coefficients/multipole_coefficients.csv"
  "$ROOT/data/processed/minimal_model/model_sigma_axis.csv"
)

required_sources=(
  "$ROOT/data/source/README.md"
  "$ROOT/data/source/production_exports/README.md"
  "$ROOT/data/source/production_exports/ahc_111/ahc_angle_dependence.csv"
  "$ROOT/data/source/production_exports/ahc_111/energy_angle_dependence.csv"
  "$ROOT/data/source/production_exports/ahc_103/ahc_angle_dependence.csv"
  "$ROOT/data/source/production_exports/ahc_103/energy_angle_dependence.csv"
  "$ROOT/data/source/production_exports/rank_resolved_103/rank_resolved_ahc.csv"
  "$ROOT/data/source/production_exports/rank_resolved_103/rank_cumulative_energy.csv"
  "$ROOT/data/source/production_exports/rank_resolved_103/single_rank_ahc.csv"
  "$ROOT/data/source/production_exports/strain_103/strain_plus_ahc.csv"
  "$ROOT/data/source/production_exports/strain_103/strain_minus_ahc.csv"
  "$ROOT/data/source/pdf_vector/README.md"
  "$ROOT/data/source/pdf_vector/band_bond/README.md"
  "$ROOT/data/source/pdf_vector/band_bond/band_1.pdf"
  "$ROOT/data/source/pdf_vector/band_bond/band_2.pdf"
  "$ROOT/data/source/pdf_vector/band_bond/band_3.pdf"
  "$ROOT/data/source/pdf_vector/band_bond/band_4.pdf"
  "$ROOT/data/source/pdf_vector/band_bond/band_5.pdf"
  "$ROOT/data/source/pdf_vector/band_bond/band_10.pdf"
  "$ROOT/data/source/pdf_vector/band_bond/band_20.pdf"
  "$ROOT/data/source/pdf_vector/band_bond/band_35.pdf"
  "$ROOT/figures/paper/bcc_111.pdf"
  "$ROOT/figures/paper/bcc_103.pdf"
  "$ROOT/figures/paper/band_bond.pdf"
  "$ROOT/figures/paper/bar_ed_all_35.pdf"
  "$ROOT/figures/paper/bar_ed_wo_q_35.pdf"
  "$ROOT/figures/paper/sigma_axis_model_1st_nn.pdf"
  "$ROOT/figures/paper/sigma_axis_model_2nd_nn.pdf"
)

required_scripts=(
  "$ROOT/scripts/reproduce_figures/plot_bcc_planes.py"
  "$ROOT/scripts/reproduce_figures/plot_band_bond.py"
  "$ROOT/scripts/reproduce_figures/plot_ahc_111.py"
  "$ROOT/scripts/reproduce_figures/plot_ahc_103.py"
  "$ROOT/scripts/reproduce_figures/plot_rank_resolved_103.py"
  "$ROOT/scripts/reproduce_figures/plot_strain_103.py"
  "$ROOT/scripts/reproduce_figures/plot_multipole_coefficients.py"
  "$ROOT/scripts/reproduce_figures/plot_minimal_model.py"
)

missing=0
for path in "${required_inputs[@]}" "${required_sources[@]}" "${required_scripts[@]}"; do
  if [[ ! -e "$path" ]]; then
    echo "Missing required file: $path" >&2
    missing=1
  fi
done

if [[ "$missing" -ne 0 ]]; then
  exit 1
fi

if [[ "$check_only" -eq 1 ]]; then
  echo "Figure reproduction processed and source inputs and scripts are present."
  exit 0
fi

if [[ "$generate_paper" -eq 1 ]]; then
  mkdir -p "$PAPER_OUTPUT_ROOT"
  "$PYTHON_BIN" "$ROOT/scripts/reproduce_figures/plot_bcc_planes.py" \
    --output-dir "$PAPER_OUTPUT_ROOT/definitions"
  "$PYTHON_BIN" "$ROOT/scripts/reproduce_figures/plot_ahc_111.py" \
    --style paper \
    --output-dir "$PAPER_OUTPUT_ROOT/ahc_111"
  "$PYTHON_BIN" "$ROOT/scripts/reproduce_figures/plot_band_bond.py" \
    --output-dir "$PAPER_OUTPUT_ROOT/band_bond"
  "$PYTHON_BIN" "$ROOT/scripts/reproduce_figures/plot_ahc_103.py" \
    --style paper \
    --output-dir "$PAPER_OUTPUT_ROOT/ahc_103"
  "$PYTHON_BIN" "$ROOT/scripts/reproduce_figures/plot_rank_resolved_103.py" \
    --output-dir "$PAPER_OUTPUT_ROOT/rank_resolved_103"
  "$PYTHON_BIN" "$ROOT/scripts/reproduce_figures/plot_strain_103.py" \
    --output-dir "$PAPER_OUTPUT_ROOT/strain_103"
  "$PYTHON_BIN" "$ROOT/scripts/reproduce_figures/plot_multipole_coefficients.py" \
    --style paper \
    --output-dir "$PAPER_OUTPUT_ROOT/multipole_coefficients"
  "$PYTHON_BIN" "$ROOT/scripts/reproduce_figures/plot_minimal_model.py" \
    --output-dir "$PAPER_OUTPUT_ROOT/minimal_model"
fi

if [[ "$generate_diagnostics" -eq 1 ]]; then
  mkdir -p "$DIAGNOSTIC_OUTPUT_ROOT"
  "$PYTHON_BIN" "$ROOT/scripts/reproduce_figures/plot_ahc_111.py" \
    --style diagnostic \
    --output-dir "$DIAGNOSTIC_OUTPUT_ROOT/ahc_111"
  "$PYTHON_BIN" "$ROOT/scripts/reproduce_figures/plot_ahc_103.py" \
    --style diagnostic \
    --output-dir "$DIAGNOSTIC_OUTPUT_ROOT/ahc_103"
  "$PYTHON_BIN" "$ROOT/scripts/reproduce_figures/plot_rank_resolved_103.py" \
    --style diagnostic \
    --output-dir "$DIAGNOSTIC_OUTPUT_ROOT/rank_resolved_103"
  "$PYTHON_BIN" "$ROOT/scripts/reproduce_figures/plot_multipole_coefficients.py" \
    --style diagnostic \
    --output-dir "$DIAGNOSTIC_OUTPUT_ROOT/multipole_coefficients"
fi

if [[ "$generate_paper" -eq 1 && "$generate_diagnostics" -eq 1 ]]; then
  cat <<EOF
Generated repository-local figures under:
  paper:       $PAPER_OUTPUT_ROOT
  diagnostics: $DIAGNOSTIC_OUTPUT_ROOT
EOF
elif [[ "$generate_paper" -eq 1 ]]; then
  cat <<EOF
Generated repository-local manuscript-style figures under:
  $PAPER_OUTPUT_ROOT
EOF
else
  cat <<EOF
Generated repository-local diagnostic figures under:
  $DIAGNOSTIC_OUTPUT_ROOT
EOF
fi
