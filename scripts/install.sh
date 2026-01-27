#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

if [[ -d .venv ]]; then
  echo "[installer] .venv already exists. Skipping venv creation."
else
  python3 -m venv .venv
fi

# shellcheck disable=SC1091
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt

echo
echo "[installer] Done."
echo "Activate:   source .venv/bin/activate"
echo "Run:        python validator.py --project-name \"Demo\" --input samples/demo_spec.md --outdir reports"
echo "Deactivate: deactivate"
