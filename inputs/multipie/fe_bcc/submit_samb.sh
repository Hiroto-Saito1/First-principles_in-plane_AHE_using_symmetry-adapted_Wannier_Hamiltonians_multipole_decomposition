#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
SAMB2TEX="${SAMB2TEX:-$ROOT/src/samb2tex.py}"
OUTPUT_FILE="${OUTPUT_FILE:-out_trs_ed}"

if [[ ! -f "$SAMB2TEX" ]]; then
  cat <<EOF >&2
Missing samb2tex.py: $SAMB2TEX

Set SAMB2TEX to the path of the MultiPie post-processing helper before running
this template. The public repository tracks the Fe SAMB inputs here, but the
historical samb2tex.py helper is not yet vendored into src/.
EOF
  exit 1
fi

python "$SAMB2TEX" Fe z_86479 > "$OUTPUT_FILE"
python "$SAMB2TEX" Fe z_86449 >> "$OUTPUT_FILE"
python "$SAMB2TEX" Fe z_86428 >> "$OUTPUT_FILE"
python "$SAMB2TEX" Fe z_86701 >> "$OUTPUT_FILE"
python "$SAMB2TEX" Fe z_86691 >> "$OUTPUT_FILE"
python "$SAMB2TEX" Fe z_87132 >> "$OUTPUT_FILE"
python "$SAMB2TEX" Fe z_86672 >> "$OUTPUT_FILE"
python "$SAMB2TEX" Fe z_87119 >> "$OUTPUT_FILE"
python "$SAMB2TEX" Fe z_86714 >> "$OUTPUT_FILE"
python "$SAMB2TEX" Fe z_87149 >> "$OUTPUT_FILE"
