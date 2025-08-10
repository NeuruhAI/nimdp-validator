# NIMDP Validator (Neuruh)
Gate every launch against the Neuruh Integrated Market Domination Protocol.

## Quick Start
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python validator.py --project-name "Demo" --input samples/demo_spec.md --outdir reports

## Notion (optional)
export NOTION_API_KEY="..."
export NOTION_DATABASE_ID="..."
python validator.py --project-name "Demo" --input samples/demo_spec.md --outdir reports --push-notion
