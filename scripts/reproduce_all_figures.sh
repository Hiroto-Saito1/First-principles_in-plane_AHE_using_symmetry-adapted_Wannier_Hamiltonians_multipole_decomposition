#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="${PYTHON:-python}"
PAPER_OUTPUT_ROOT="$ROOT/results/figures_paper"
DIAGNOSTIC_OUTPUT_ROOT="$ROOT/results/figures_diagnostics"
check_only=0
generate_paper=1
generate_diagnostics=1
generate_contact_sheet=0
CONTACT_SHEET_OUTPUT=""

usage() {
  cat <<EOF
Usage: scripts/reproduce_all_figures.sh [options] [legacy-paper-output-root]

Options:
  --check                   Verify inputs and scripts only; do not plot.
  --paper-root PATH         Output root for manuscript-style plots.
  --diagnostics-root PATH   Output root for diagnostic plots.
  --paper-only              Generate only manuscript-style plots.
  --diagnostics-only        Generate only diagnostic plots.
  --with-contact-sheet      Build a reference-vs-generated contact sheet PDF.
  --contact-sheet-output PATH
                            Explicit output path for the contact sheet PDF.
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
    --with-contact-sheet)
      generate_contact_sheet=1
      shift
      ;;
    --contact-sheet-output)
      CONTACT_SHEET_OUTPUT="$2"
      shift 2
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

if [[ "$generate_contact_sheet" -eq 1 && "$generate_paper" -eq 0 ]]; then
  echo "Contact sheets require manuscript-style figure output. Remove --diagnostics-only." >&2
  exit 2
fi

if [[ -z "$CONTACT_SHEET_OUTPUT" ]]; then
  CONTACT_SHEET_OUTPUT="$DIAGNOSTIC_OUTPUT_ROOT/contact_sheets/paper_vs_reference.pdf"
fi

dependency_query=(
  "$PYTHON_BIN"
  "$ROOT/scripts/workflow/figure_dependencies.py"
  --root
  "$ROOT"
)

if [[ "$generate_paper" -eq 1 ]]; then
  dependency_query+=(--paper)
fi

if [[ "$generate_diagnostics" -eq 1 ]]; then
  dependency_query+=(--diagnostics)
fi

if [[ "$generate_contact_sheet" -eq 1 ]]; then
  dependency_query+=(--contact-sheet)
fi

required_paths=()
while IFS= read -r line; do
  if [[ -n "$line" ]]; then
    required_paths+=("$line")
  fi
done < <("${dependency_query[@]}")

missing=0
for path in "${required_paths[@]}"; do
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

if [[ "$generate_contact_sheet" -eq 1 ]]; then
  "$PYTHON_BIN" "$ROOT/scripts/reproduce_figures/make_paper_contact_sheet.py" \
    --paper-root "$PAPER_OUTPUT_ROOT" \
    --output "$CONTACT_SHEET_OUTPUT"
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

if [[ "$generate_contact_sheet" -eq 1 ]]; then
  cat <<EOF
Generated paper-figure contact sheet:
  $CONTACT_SHEET_OUTPUT
EOF
fi
