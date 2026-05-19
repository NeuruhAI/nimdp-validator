cd ~/neuruh/nimdp-validato![NIMDP Gate](https://github.com/NeuruhAI/nimdp-validator/actions/workflows/validate.yml/badge.svg)
# NIMDP Validator (Neuruh)
Gate every launch against the Neuruh Integrated Market Domination Protocol.

## Quick Start
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python validator.py --project-name "Demo" --input samples/demo_spec.md --outdir reports

## Token Packs (Optional)
Use a custom token map:
python validator.py --project-name "Demo" --input samples/demo_spec.md --outdir reports --token-map packs/token_map_rei.yaml

## Notion (Optional)
export NOTION_API_KEY="..."
export NOTION_DATABASE_ID="..."
python validator.py --project-name "Demo" --input samples/demo_spec.md --outdir reports --push-notion

## CI
A GitHub Actions workflow validates on every push/PR.

## Packaging
pyinstaller --onefile validator.py

## Token Packs
Private repo: https://github.com/NeuruhAI/nimdp-packs
