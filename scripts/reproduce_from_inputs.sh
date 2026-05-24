#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="${PYTHON:-python}"
PAPER_OUTPUT_ROOT="$ROOT/results/figures_paper"
DIAGNOSTIC_OUTPUT_ROOT="$ROOT/results/figures_diagnostics"
EXECUTE_EXPENSIVE=0
STAGES=()
WITH_CONTACT_SHEET=0
CONTACT_SHEET_OUTPUT=""

usage() {
  cat <<EOF
Usage: scripts/reproduce_from_inputs.sh [options]

Default:
  Run the lightweight public reproduction path:
    --stage extract --stage figures

Options:
  --stage NAME          Run one stage. May be repeated.
                        Known stages: dft, wannier, symwannier, multipie,
                        rotate, ahc, extract, figures
  --output-root PATH    Backward-compatible alias for --paper-output-root.
  --paper-output-root PATH
                        Manuscript-style figure output directory for the
                        figures stage.
  --diagnostic-output-root PATH
                        Diagnostic figure output directory for the figures
                        stage.
  --with-contact-sheet  Generate a paper-vs-reference contact sheet during
                        the figures stage.
  --contact-sheet-output PATH
                        Explicit output path for the contact sheet PDF.
  --python PATH         Python executable.
  --execute-expensive   Reserved for future cleaned HPC launch wrappers.
                        The current public driver still prints HPC recipes
                        instead of launching cluster jobs.
  -h, --help            Show this help.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --stage)
      if [[ $# -lt 2 ]]; then
        echo "--stage requires a value" >&2
        exit 2
      fi
      STAGES+=("$2")
      shift 2
      ;;
    --output-root)
      if [[ $# -lt 2 ]]; then
        echo "--output-root requires a value" >&2
        exit 2
      fi
      PAPER_OUTPUT_ROOT="$2"
      shift 2
      ;;
    --paper-output-root)
      if [[ $# -lt 2 ]]; then
        echo "--paper-output-root requires a value" >&2
        exit 2
      fi
      PAPER_OUTPUT_ROOT="$2"
      shift 2
      ;;
    --diagnostic-output-root)
      if [[ $# -lt 2 ]]; then
        echo "--diagnostic-output-root requires a value" >&2
        exit 2
      fi
      DIAGNOSTIC_OUTPUT_ROOT="$2"
      shift 2
      ;;
    --with-contact-sheet)
      WITH_CONTACT_SHEET=1
      shift
      ;;
    --contact-sheet-output)
      if [[ $# -lt 2 ]]; then
        echo "--contact-sheet-output requires a value" >&2
        exit 2
      fi
      CONTACT_SHEET_OUTPUT="$2"
      shift 2
      ;;
    --python)
      if [[ $# -lt 2 ]]; then
        echo "--python requires a value" >&2
        exit 2
      fi
      PYTHON_BIN="$2"
      shift 2
      ;;
    --execute-expensive)
      EXECUTE_EXPENSIVE=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if [[ "${#STAGES[@]}" -eq 0 ]]; then
  STAGES=(extract figures)
fi

note_stage() {
  local stage="$1"
  local readme="$2"
  local summary="$3"
  local extra_note="${4:-}"
  if [[ ! -e "$ROOT/$readme" ]]; then
    echo "Missing recipe file for $stage: $readme" >&2
    exit 1
  fi
  cat <<EOF
[$stage] $summary
Recipe: $readme

This stage depends on external first-principles/HPC software and is not run
by the default public workflow. Use the documented inputs, pseudopotentials,
software versions, and cluster commands in the recipe file.
EOF
  if [[ -n "$extra_note" ]]; then
    printf '%s\n' "$extra_note"
  fi
}

run_stage() {
  local stage="$1"
  case "$stage" in
    dft)
      note_stage "dft" "inputs/dft/README.md" \
        "Prepare Quantum ESPRESSO SCF/NSCF calculations for unstrained, (111), (103), and [103]-strain workflows."
      ;;
    wannier)
      note_stage "wannier" "inputs/wannier/fe_bcc_unstrained/README.md" \
        "Prepare Wannier90 and pw2wannier90 spinor Hamiltonian inputs."
      ;;
    symwannier)
      note_stage "symwannier" "inputs/symwannier/fe_bcc/README.md" \
        "Build symmetry-adapted/TRS-Wannier Hamiltonian branches and rank filters."
      ;;
    multipie)
      note_stage "multipie" "inputs/multipie/fe_bcc/README.md" \
        "Generate the Fe SAMB/MultiPie basis and coefficient labels." \
        "Fe_all_35 pickle/HDF5 recipe: data/source/workflow_manifests/multipole_coefficients/Fe_all_35_recipe.md"
      ;;
    rotate)
      note_stage "rotate" "inputs/wannierberri/fe_bcc_rotation/README.md" \
        "Generate magnetization-rotated Hamiltonian branches for AHC calculations."
      ;;
    ahc)
      note_stage "ahc" "inputs/wannierberri/fe_bcc_rotation/README.md" \
        "Generate WannierBerri anomalous-Hall-conductivity jobs and summaries."
      ;;
    extract)
      "$PYTHON_BIN" "$ROOT/scripts/workflow/rebuild_processed_data.py"
      ;;
    figures)
      local -a figure_args=(
        --paper-root "$PAPER_OUTPUT_ROOT"
        --diagnostics-root "$DIAGNOSTIC_OUTPUT_ROOT"
      )
      if [[ "$WITH_CONTACT_SHEET" -eq 1 ]]; then
        figure_args+=(--with-contact-sheet)
      fi
      if [[ -n "$CONTACT_SHEET_OUTPUT" ]]; then
        figure_args+=(--contact-sheet-output "$CONTACT_SHEET_OUTPUT")
      fi
      PYTHON="$PYTHON_BIN" bash "$ROOT/scripts/reproduce_all_figures.sh" \
        "${figure_args[@]}"
      ;;
    *)
      echo "Unknown stage: $stage" >&2
      usage >&2
      exit 2
      ;;
  esac
}

if [[ "$EXECUTE_EXPENSIVE" -eq 1 ]]; then
  cat <<EOF
The current public repository does not execute full HPC stages automatically.
It provides exact input manifests and command recipes, while the lightweight
extract/figures stages are executable on a normal workstation.

EOF
fi

for stage in "${STAGES[@]}"; do
  run_stage "$stage"
done
