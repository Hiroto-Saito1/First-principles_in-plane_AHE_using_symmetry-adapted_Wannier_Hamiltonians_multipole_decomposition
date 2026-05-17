#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="${PYTHON:-python}"
OUTPUT_ROOT="${1:-"$ROOT/results/figures"}"

check_only=0
if [[ "${1:-}" == "--check" ]]; then
  check_only=1
  OUTPUT_ROOT="$ROOT/results/figures"
fi

required_inputs=(
  "$ROOT/data/processed/ahc_111/ahc_angle_dependence.csv"
  "$ROOT/data/processed/ahc_103/ahc_angle_dependence.csv"
  "$ROOT/data/processed/rank_resolved_103/rank_resolved_ahc.csv"
  "$ROOT/data/processed/strain_103/strain_plus_ahc.csv"
  "$ROOT/data/processed/strain_103/strain_minus_ahc.csv"
)

required_scripts=(
  "$ROOT/scripts/reproduce_figures/plot_ahc_111.py"
  "$ROOT/scripts/reproduce_figures/plot_ahc_103.py"
  "$ROOT/scripts/reproduce_figures/plot_rank_resolved_103.py"
  "$ROOT/scripts/reproduce_figures/plot_strain_103.py"
)

missing=0
for path in "${required_inputs[@]}" "${required_scripts[@]}"; do
  if [[ ! -e "$path" ]]; then
    echo "Missing required file: $path" >&2
    missing=1
  fi
done

if [[ "$missing" -ne 0 ]]; then
  exit 1
fi

if [[ "$check_only" -eq 1 ]]; then
  echo "Figure reproduction inputs and scripts are present."
  exit 0
fi

mkdir -p "$OUTPUT_ROOT"

"$PYTHON_BIN" "$ROOT/scripts/reproduce_figures/plot_ahc_111.py" \
  --output-dir "$OUTPUT_ROOT/ahc_111"
"$PYTHON_BIN" "$ROOT/scripts/reproduce_figures/plot_ahc_103.py" \
  --output-dir "$OUTPUT_ROOT/ahc_103"
"$PYTHON_BIN" "$ROOT/scripts/reproduce_figures/plot_rank_resolved_103.py" \
  --output-dir "$OUTPUT_ROOT/rank_resolved_103"
"$PYTHON_BIN" "$ROOT/scripts/reproduce_figures/plot_strain_103.py" \
  --output-dir "$OUTPUT_ROOT/strain_103"

cat <<EOF
Generated repository-local figures under:
  $OUTPUT_ROOT

Skipped workflow-required figures until compact data are added:
  multipole coefficient bar plots
  single-rank (103) AHC comparison plots
  minimal-model sigma_axis scans
  band/bond convergence plot
EOF
