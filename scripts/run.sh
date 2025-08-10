#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
if [[ ! -d .venv ]]; then
  python3 -m venv .venv
  .venv/bin/pip install --upgrade pip
  .venv/bin/pip install -r requirements.txt || true
fi
mkdir -p reports
.venv/bin/python validator.py --project-name "${1:-Local}" --input "${2:-samples/demo_spec.md}" --outdir reports ${3:-}
