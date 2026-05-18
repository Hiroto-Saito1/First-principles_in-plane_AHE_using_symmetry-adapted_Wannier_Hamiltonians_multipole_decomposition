#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BIN="${PYTHON:-python}"
SAMB_PATH="${SAMB_PATH:-Fe_samb.py}"

"$PYTHON_BIN" "$SCRIPT_DIR/energy_diff_fe.py" --samb-path "$SAMB_PATH" > "$SCRIPT_DIR/energy_diff_35_all.out"
"$PYTHON_BIN" "$SCRIPT_DIR/energy_diff_fe.py" A1g T1g --samb-path "$SAMB_PATH" > "$SCRIPT_DIR/energy_diff_35_a1g_t1g.out"
"$PYTHON_BIN" "$SCRIPT_DIR/energy_diff_fe.py" A1g T1g Eg --samb-path "$SAMB_PATH" > "$SCRIPT_DIR/energy_diff_35_a1g_t1g_eg.out"
"$PYTHON_BIN" "$SCRIPT_DIR/energy_diff_fe.py" A1g T1g Eg T2g --samb-path "$SAMB_PATH" > "$SCRIPT_DIR/energy_diff_35_a1g_t1g_eg_t2g.out"
